from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.core.config import settings
from app.crew import stream_crew

router = APIRouter(tags=["crew"])


class CrewMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class CrewRoute(BaseModel):
    section: str | None = None
    sub: str | None = None


class CrewChatRequest(BaseModel):
    messages: list[CrewMessage]
    route: CrewRoute | None = None


@router.post("/crew/chat")
def crew_chat(payload: CrewChatRequest) -> StreamingResponse:
    """Stream a Crew reply (Server-Sent Events). Requires ANTHROPIC_API_KEY."""
    if not settings.anthropic_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Crew is not configured. Set ANTHROPIC_API_KEY on the backend.",
        )

    messages = [{"role": msg.role, "content": msg.content} for msg in payload.messages]
    route = payload.route.model_dump() if payload.route else None

    return StreamingResponse(
        stream_crew(messages, route),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
