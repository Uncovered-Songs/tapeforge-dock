"""Seed the Dock database with sample operational data.

This mirrors the frontend's former mock data (src/dock/data.ts). The global
event stream / config changes belong to the centerpiece broadcast session
(S-2040). Seeding is idempotent: it no-ops if the systems table is populated.
"""

from sqlmodel import Session, select

from app.core import db
from app.models import dock as m

CENTERPIECE = "S-2040"

SYSTEMS = [
    {"id": "core-main", "kind": "core", "name": "CORE-Main", "loc": "Northgate HQ", "ver": "0.9.4", "status": "ok", "uptime": "34d 6h", "cpu": 22, "sessions": 3, "note": "Graph resolver · 7 endpoints"},
    {"id": "dock-stage", "kind": "port", "name": "PORT-Stage", "loc": "Riverside Arena", "ver": "0.9.4", "status": "warn", "uptime": "2d 11h", "cpu": 61, "sessions": 1, "note": "AES67 · 64 streams · clock drift"},
    {"id": "dock-foh", "kind": "port", "name": "PORT-FOH", "loc": "Riverside Arena", "ver": "0.9.4", "status": "ok", "uptime": "2d 11h", "cpu": 38, "sessions": 1, "note": "AES67 · 48 streams"},
    {"id": "desk-a", "kind": "desk", "name": "DESK-Studio-A", "loc": "Northgate HQ", "ver": "0.9.3", "status": "ok", "uptime": "9d 2h", "cpu": 27, "sessions": 1, "note": "32 ch · 8 grp · 8 mtx"},
    {"id": "rig-fest", "kind": "rig", "name": "RIG-Festival", "loc": "Meadow Park", "ver": "0.9.4", "status": "ok", "uptime": "18h", "cpu": 44, "sessions": 1, "note": "12 DSP chains · 38% load"},
    {"id": "capstan-a", "kind": "capstan", "name": "CAPSTAN-Studio", "loc": "Northgate HQ", "ver": "0.5.0", "status": "ok", "uptime": "9d 2h", "cpu": 19, "sessions": 1, "note": "24 tracks · RAID-0"},
    {"id": "scope-bc", "kind": "scope", "name": "SCOPE-Broadcast", "loc": "Civic Theatre", "ver": "0.9.4", "status": "crit", "uptime": "4h", "cpu": 12, "sessions": 0, "note": "Node offline · no PTP"},
    {"id": "core-bc", "kind": "core", "name": "CORE-Broadcast", "loc": "Civic Theatre", "ver": "0.9.4", "status": "ok", "uptime": "4h", "cpu": 30, "sessions": 1, "note": "Graph resolver · 5 endpoints"},
]

SESSIONS = [
    {"id": "S-2041", "name": "Riverside Arena — FOH", "type": "Live Sound", "loc": "Riverside Arena", "date": "2026-06-03", "start": "18:40", "dur": "live", "status": "live", "systems": ["core-main", "dock-stage", "dock-foh", "rig-fest"], "events": 142, "issues": 2, "engineer": "J. Castell"},
    {"id": "S-2040", "name": "Civic Theatre — Broadcast", "type": "Broadcast", "loc": "Civic Theatre", "date": "2026-06-02", "start": "19:00", "dur": "3h 12m", "status": "review", "systems": ["core-bc", "scope-bc"], "events": 318, "issues": 5, "engineer": "M. Ndlovu"},
    {"id": "S-2039", "name": "Studio A — Tracking Day 4", "type": "Studio", "loc": "Northgate HQ", "date": "2026-06-02", "start": "10:15", "dur": "6h 48m", "status": "done", "systems": ["core-main", "desk-a", "capstan-a"], "events": 96, "issues": 0, "engineer": "L. Park"},
    {"id": "S-2038", "name": "Meadow Park — Headline Set", "type": "Live Sound", "loc": "Meadow Park", "date": "2026-06-01", "start": "21:30", "dur": "1h 50m", "status": "done", "systems": ["rig-fest", "dock-stage"], "events": 211, "issues": 1, "engineer": "J. Castell"},
    {"id": "S-2037", "name": "Studio A — Mix Review", "type": "Studio", "loc": "Northgate HQ", "date": "2026-05-30", "start": "14:00", "dur": "2h 05m", "status": "done", "systems": ["desk-a", "capstan-a"], "events": 54, "issues": 0, "engineer": "L. Park"},
    {"id": "S-2036", "name": "Civic Theatre — Rehearsal", "type": "Rehearsal", "loc": "Civic Theatre", "date": "2026-05-29", "start": "16:30", "dur": "4h 20m", "status": "done", "systems": ["core-bc", "scope-bc"], "events": 173, "issues": 3, "engineer": "M. Ndlovu"},
]

EVENT_STREAM = [
    {"t": "19:00:02", "tone": "info", "src": "CORE-Broadcast", "msg": "Session started · graph resolved (5 endpoints)"},
    {"t": "19:00:04", "tone": "ok", "src": "PORT", "msg": "AES67 streams established · 32 in / 16 out"},
    {"t": "19:04:18", "tone": "ok", "src": "SCOPE", "msg": "Loudness target locked · -23 LUFS (EBU R128)"},
    {"t": "19:42:51", "tone": "warn", "src": "PORT-Stage", "msg": "PTP clock offset rising · 18µs → 41µs"},
    {"t": "20:11:09", "tone": "warn", "src": "PORT-Stage", "msg": "Packet jitter spike · 0.9ms on stream 12"},
    {"t": "20:11:14", "tone": "crit", "src": "PORT-Stage", "msg": "Clock domain desync · failover to grandmaster B"},
    {"t": "20:11:15", "tone": "info", "src": "CORE-Broadcast", "msg": "Topology snapshot captured (auto)"},
    {"t": "20:12:02", "tone": "ok", "src": "PORT-Stage", "msg": "PTP re-locked · offset 6µs · streams stable"},
    {"t": "21:48:30", "tone": "info", "src": "CAPSTAN", "msg": "Archive write complete · 318 GB · RAID verified"},
    {"t": "22:12:40", "tone": "ok", "src": "CORE-Broadcast", "msg": "Session ended cleanly · summary generated"},
]

CONFIG_CHANGES = [
    {"t": "19:00", "who": "M. Ndlovu", "what": "Set master bus loudness target", "from_": "—", "to_": "-23 LUFS"},
    {"t": "20:11", "who": "auto · CORE", "what": "PTP grandmaster", "from_": "GM-A (stage)", "to_": "GM-B (FOH)"},
    {"t": "20:34", "who": "M. Ndlovu", "what": "RIG · de-esser threshold (Lead Vox)", "from_": "-18 dB", "to_": "-22 dB"},
    {"t": "21:05", "who": "auto · CORE", "what": "Buffer size (PORT-Stage)", "from_": "64", "to_": "128"},
]

CREW_RECS = [
    {"tone": "warn", "title": "Recurring clock drift on PORT-Stage", "body": "PTP offset has exceeded 40µs in 3 of the last 5 sessions at Riverside Arena. Likely a grandmaster priority conflict.", "action": "Investigate clock topology"},
    {"tone": "info", "title": "SCOPE-Broadcast offline 4h", "body": "No PTP lock since 18:02. Node may need a manual restart or network check at Civic Theatre.", "action": "Open diagnostics"},
    {"tone": "ok", "title": "Studio A tracking stable", "body": "3 sessions, 0 issues this week. Configuration unchanged since v0.9.3.", "action": "View systems"},
]

KNOWLEDGE = [
    {"id": "k1", "kind": "Generated", "title": "Riverside Arena — clock topology playbook", "tags": ["AES67", "PTP", "clock"], "by": "Crew", "updated": "2h ago", "cites": 4},
    {"id": "k2", "kind": "Note", "title": "Festival rig deployment checklist", "tags": ["deployment", "RIG"], "by": "J. Castell", "updated": "1d ago", "cites": 0},
    {"id": "k3", "kind": "Troubleshooting", "title": "Resolving PTP grandmaster failover loops", "tags": ["PTP", "network"], "by": "Crew", "updated": "2d ago", "cites": 6},
    {"id": "k4", "kind": "Imported", "title": "AES67 interop matrix — RME / Dante / SoundGrid", "tags": ["AES67", "interop"], "by": "Docs", "updated": "5d ago", "cites": 0},
    {"id": "k5", "kind": "Generated", "title": "Studio A signal flow reference", "tags": ["DESK", "routing"], "by": "Crew", "updated": "6d ago", "cites": 2},
    {"id": "k6", "kind": "Note", "title": "Broadcast loudness compliance (EBU R128)", "tags": ["SCOPE", "loudness"], "by": "M. Ndlovu", "updated": "1w ago", "cites": 1},
]

DOC_TREE = [
    {"group": "Getting Started", "items": ["Introduction", "Deploying CORE", "Connecting PORT nodes", "First session"]},
    {"group": "Network Audio", "items": ["AES67 setup", "PTP & clocking", "Stream management", "Troubleshooting jitter"]},
    {"group": "Products", "items": ["CORE — control plane", "DESK — mixing", "RIG — processing", "CAPSTAN — recording", "SCOPE — observability"]},
    {"group": "Operations", "items": ["Sessions & snapshots", "Topology management", "Diagnostics", "Crew & knowledge"]},
]

CREW_THREAD = [
    {"role": "user", "text": "Why did PORT-Stage disconnect during the Civic Theatre broadcast yesterday?", "cites": [], "agents": []},
    {"role": "crew", "text": "PORT-Stage didn't fully disconnect — it triggered a PTP clock failover at 20:11:14. The grandmaster offset climbed from 18µs to 41µs over ~30 min, then a 0.9ms jitter spike on stream 12 pushed the clock domain out of sync. CORE failed over to grandmaster B (FOH) and PTP re-locked within 48 seconds at 6µs.", "cites": [{"t": "Session S-2040 · event 20:11:14", "to": "session"}, {"t": "Doc · PTP & clocking", "to": "docs"}], "agents": ["Networking", "Topology"]},
    {"role": "user", "text": "Has this happened before at Riverside Arena?", "cites": [], "agents": []},
    {"role": "crew", "text": "Yes — 3 of the last 5 sessions at Riverside Arena (S-2041, S-2038, and one rehearsal) show PTP offset exceeding 40µs. The common factor is two grandmaster-capable PORT nodes with equal priority. I drafted a playbook recommending a fixed priority hierarchy.", "cites": [{"t": "Knowledge · clock topology playbook", "to": "knowledge"}, {"t": "3 related sessions", "to": "sessions"}], "agents": ["Deployment History", "Troubleshooting"]},
]

INCIDENTS = [
    {"tone": "crit", "sys": "SCOPE-Broadcast", "issue": "Node offline — no PTP lock", "when": "Today 18:02", "dur": "ongoing"},
    {"tone": "warn", "sys": "PORT-Stage", "issue": "Clock drift > 40µs", "when": "Today 20:11", "dur": "48s"},
    {"tone": "warn", "sys": "PORT-Stage", "issue": "Jitter spike (stream 12)", "when": "Jun 1 21:44", "dur": "2m"},
    {"tone": "ok", "sys": "CORE-Main", "issue": "Auto-recovered buffer underrun", "when": "May 30 14:22", "dur": "3s"},
]

METRICS = {
    "clock_offset": [12, 14, 13, 18, 22, 31, 41, 38, 9, 6, 7, 6],
    "jitter": [0.2, 0.3, 0.25, 0.4, 0.5, 0.7, 0.9, 0.6, 0.3, 0.2, 0.2, 0.25],
    "latency": [2.1, 2.0, 2.2, 2.1, 2.4, 2.3, 2.2, 2.1, 2.0, 2.1, 2.2, 2.1],
    "packet_loss": [0, 0, 0, 0, 0.01, 0.03, 0.08, 0.02, 0, 0, 0, 0],
}


def seed_db() -> None:
    """Populate the database from the sample data, if not already seeded."""
    with Session(db.engine) as session:
        if session.exec(select(m.System).limit(1)).first():
            return  # already seeded

        session.add_all(m.System(**s) for s in SYSTEMS)
        session.add_all(m.Session(**s) for s in SESSIONS)
        session.add_all(m.KnowledgeEntry(**k) for k in KNOWLEDGE)

        for i, e in enumerate(EVENT_STREAM):
            session.add(m.SessionEvent(session_id=CENTERPIECE, idx=i, **e))
        for i, c in enumerate(CONFIG_CHANGES):
            session.add(m.ConfigChange(session_id=CENTERPIECE, idx=i, **c))
        for i, r in enumerate(CREW_RECS):
            session.add(m.CrewRec(idx=i, **r))
        for i, t in enumerate(CREW_THREAD):
            session.add(m.CrewTurn(idx=i, **t))
        for i, inc in enumerate(INCIDENTS):
            session.add(m.Incident(idx=i, **inc))
        for i, d in enumerate(DOC_TREE):
            session.add(m.DocSection(idx=i, **d))
        session.add(m.MetricsRow(**METRICS))

        session.commit()
