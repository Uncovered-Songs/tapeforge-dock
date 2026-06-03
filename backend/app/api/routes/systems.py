from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session as DBSession, select

from app.core.db import get_session
from app.models import dock as m

router = APIRouter(tags=["systems"])


@router.get("/systems", response_model=list[m.SystemRead])
def list_systems(session: DBSession = Depends(get_session)) -> list[m.System]:
    return list(session.exec(select(m.System)).all())


@router.get("/systems/{system_id}", response_model=m.SystemRead)
def get_system(system_id: str, session: DBSession = Depends(get_session)) -> m.System:
    system = session.get(m.System, system_id)
    if not system:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="System not found")
    return system
