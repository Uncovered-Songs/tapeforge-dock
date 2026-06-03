from fastapi import APIRouter, Depends
from sqlmodel import Session as DBSession, select

from app.core.db import get_session
from app.models import dock as m

router = APIRouter(tags=["knowledge"])


@router.get("/knowledge", response_model=list[m.KnowledgeRead])
def list_knowledge(session: DBSession = Depends(get_session)) -> list[m.KnowledgeEntry]:
    return list(session.exec(select(m.KnowledgeEntry).order_by(m.KnowledgeEntry.id)).all())
