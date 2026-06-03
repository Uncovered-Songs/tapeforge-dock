from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session as DBSession, select

from app.core.db import get_session
from app.models import dock as m

router = APIRouter(tags=["sessions"])


@router.get("/sessions", response_model=list[m.SessionRead])
def list_sessions(session: DBSession = Depends(get_session)) -> list[m.Session]:
    # Newest first (ids are monotonically increasing, e.g. S-2041 > S-2040).
    return list(session.exec(select(m.Session).order_by(m.Session.id.desc())).all())


@router.get("/sessions/{session_id}", response_model=m.SessionDetailRead)
def get_session_detail(
    session_id: str, session: DBSession = Depends(get_session)
) -> m.SessionDetailRead:
    row = session.get(m.Session, session_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    events = session.exec(
        select(m.SessionEvent).where(m.SessionEvent.session_id == session_id).order_by(m.SessionEvent.idx)
    ).all()
    configs = session.exec(
        select(m.ConfigChange).where(m.ConfigChange.session_id == session_id).order_by(m.ConfigChange.idx)
    ).all()

    return m.SessionDetailRead(
        **row.model_dump(),
        eventStream=[m.EventRead.model_validate(e, from_attributes=True) for e in events],
        configChanges=[m.ConfigChangeRead.model_validate(c, from_attributes=True) for c in configs],
    )
