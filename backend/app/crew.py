"""Crew — the operational AI assistant, backed by the Claude API.

A grounded, streaming agent: the operator's live operational data is fed as a
(prompt-cached) system context, and Crew can call tools to pull specifics and to
navigate the operator's view. Server-Sent Events stream text + navigation to the
frontend.
"""

import json
from collections.abc import Iterator

import anthropic
from sqlmodel import Session, select

from app.core.config import settings
from app.core import db
from app.models import dock as m

MAX_TOOL_ITERATIONS = 6
MAX_TOKENS = 2048

PERSONA = """You are Crew, the operational assistant inside TapeForge Dock — the operating platform for professional audio infrastructure (CORE control plane, PORT network audio, DESK mixing, RIG processing, CAPSTAN recording, SCOPE observability).

You help the operator run their environment: sessions, systems, diagnostics, knowledge. Speak like a seasoned audio-infrastructure engineer — concise, concrete, calm. Use the AES67 / PTP / loudness vocabulary naturally.

Ground every answer ONLY in the operational data provided below and what you retrieve via tools. If something isn't in the data, say so plainly — never invent systems, sessions, metrics, or events.

When seeing a specific place in the app would help the operator, call the `navigate` tool to open it for them, and say briefly what you opened. Use `get_session_detail` / `get_system_detail` to pull specifics (event timelines, config changes, per-system fields) before answering when the question needs them.

Keep replies short by default — a few sentences. Expand only when the operator asks for depth."""


def _data_context(session: Session) -> str:
    """A compact, deterministic snapshot of the environment for grounding."""
    systems = session.exec(select(m.System)).all()
    sessions = session.exec(select(m.Session).order_by(m.Session.id.desc())).all()
    knowledge = session.exec(select(m.KnowledgeEntry).order_by(m.KnowledgeEntry.id)).all()
    incidents = session.exec(select(m.Incident).order_by(m.Incident.idx)).all()

    lines: list[str] = ["# Current environment (Northgate Audio · 4 locations)", "", "## Systems"]
    for s in systems:
        lines.append(
            f"- {s.id}: {s.name} ({s.kind}) @ {s.loc} · v{s.ver} · status={s.status} · "
            f"cpu={s.cpu}% · uptime={s.uptime} · sessions={s.sessions} · {s.note}"
        )
    lines += ["", "## Sessions"]
    for s in sessions:
        lines.append(
            f"- {s.id}: {s.name} · {s.type} @ {s.loc} · {s.date} {s.start} · {s.dur} · "
            f"status={s.status} · events={s.events} · issues={s.issues} · engineer={s.engineer} · "
            f"systems={','.join(s.systems)}"
        )
    lines += ["", "## Open incidents (diagnostics)"]
    for i in incidents:
        lines.append(f"- [{i.tone}] {i.sys}: {i.issue} · {i.when} · {i.dur}")
    lines += ["", "## Knowledge base"]
    for k in knowledge:
        lines.append(f"- {k.id}: {k.title} ({k.kind}, by {k.by}, {k.cites} cites)")
    return "\n".join(lines)


def _system_blocks(session: Session, route: dict | None) -> list[dict]:
    blocks: list[dict] = [
        {"type": "text", "text": PERSONA},
        # The data context is stable per process → cache it (prefix match).
        {"type": "text", "text": _data_context(session), "cache_control": {"type": "ephemeral"}},
    ]
    if route and route.get("section"):
        where = route["section"]
        if route.get("sub"):
            where += f" ({route['sub']})"
        blocks.append({"type": "text", "text": f"The operator is currently viewing: {where}."})
    return blocks


TOOLS = [
    {
        "name": "get_session_detail",
        "description": "Get full detail for one session by id: its event timeline and configuration changes.",
        "input_schema": {
            "type": "object",
            "properties": {"session_id": {"type": "string", "description": "e.g. S-2040"}},
            "required": ["session_id"],
        },
    },
    {
        "name": "get_system_detail",
        "description": "Get full detail for one system by id.",
        "input_schema": {
            "type": "object",
            "properties": {"system_id": {"type": "string", "description": "e.g. scope-bc"}},
            "required": ["system_id"],
        },
    },
    {
        "name": "navigate",
        "description": "Open a section of the operator's Dock view (optionally a specific session or system). Use when seeing it would help them.",
        "input_schema": {
            "type": "object",
            "properties": {
                "section": {
                    "type": "string",
                    "enum": ["overview", "sessions", "systems", "crew", "knowledge", "docs", "diagnostics"],
                },
                "session_id": {"type": "string", "description": "When section=sessions, open this session."},
                "system_id": {"type": "string", "description": "When section=systems, open this system."},
            },
            "required": ["section"],
        },
    },
]


def _sse(obj: dict) -> str:
    return f"data: {json.dumps(obj)}\n\n"


def _fetch_session_detail(session_id: str) -> dict | None:
    with Session(db.engine) as s:
        row = s.get(m.Session, session_id)
        if not row:
            return None
        events = s.exec(
            select(m.SessionEvent).where(m.SessionEvent.session_id == session_id).order_by(m.SessionEvent.idx)
        ).all()
        configs = s.exec(
            select(m.ConfigChange).where(m.ConfigChange.session_id == session_id).order_by(m.ConfigChange.idx)
        ).all()
        return {
            **row.model_dump(),
            "events": [{"t": e.t, "tone": e.tone, "src": e.src, "msg": e.msg} for e in events],
            "configChanges": [{"t": c.t, "who": c.who, "what": c.what, "from": c.from_, "to": c.to_} for c in configs],
        }


def _fetch_system_detail(system_id: str) -> dict | None:
    with Session(db.engine) as s:
        row = s.get(m.System, system_id)
        return row.model_dump() if row else None


def stream_crew(messages: list[dict], route: dict | None) -> Iterator[str]:
    """Run the streaming agent loop, yielding SSE event strings."""
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    with Session(db.engine) as ctx_session:
        system = _system_blocks(ctx_session, route)

    convo: list[dict] = [{"role": msg["role"], "content": msg["content"]} for msg in messages]

    try:
        for _ in range(MAX_TOOL_ITERATIONS):
            with client.messages.stream(
                model=settings.crew_model,
                max_tokens=MAX_TOKENS,
                system=system,
                tools=TOOLS,
                messages=convo,
            ) as stream:
                for event in stream:
                    if event.type == "content_block_delta" and event.delta.type == "text_delta":
                        yield _sse({"type": "text", "text": event.delta.text})
                final = stream.get_final_message()

            convo.append({"role": "assistant", "content": final.content})

            if final.stop_reason != "tool_use":
                break

            tool_results = []
            for block in final.content:
                if block.type != "tool_use":
                    continue
                if block.name == "navigate":
                    yield _sse(
                        {
                            "type": "navigate",
                            "section": block.input.get("section"),
                            "sub": block.input.get("session_id") or block.input.get("system_id"),
                        }
                    )
                    tool_results.append(
                        {"type": "tool_result", "tool_use_id": block.id, "content": "Opened it for the operator."}
                    )
                elif block.name == "get_session_detail":
                    data = _fetch_session_detail(block.input.get("session_id", ""))
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(data) if data else "No such session.",
                            "is_error": data is None,
                        }
                    )
                elif block.name == "get_system_detail":
                    data = _fetch_system_detail(block.input.get("system_id", ""))
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(data) if data else "No such system.",
                            "is_error": data is None,
                        }
                    )
            convo.append({"role": "user", "content": tool_results})

        yield _sse({"type": "done"})
    except anthropic.APIError as exc:
        yield _sse({"type": "error", "message": f"Crew error: {exc.__class__.__name__}"})
