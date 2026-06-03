from fastapi import APIRouter, Depends
from sqlmodel import Session as DBSession, select

from app.api.routes.diagnostics import build_diagnostics
from app.core.db import get_session
from app.models import dock as m
from app.seed import CENTERPIECE

router = APIRouter(tags=["bootstrap"])


def _read(schema: type[m.SQLModel], rows) -> list:
    return [schema.model_validate(r, from_attributes=True) for r in rows]


@router.get("/bootstrap", response_model=m.BootstrapRead)
def bootstrap(session: DBSession = Depends(get_session)) -> m.BootstrapRead:
    """Everything the Dock frontend needs to populate its store in one call."""
    systems = session.exec(select(m.System)).all()
    sessions = session.exec(select(m.Session).order_by(m.Session.id.desc())).all()
    knowledge = session.exec(select(m.KnowledgeEntry).order_by(m.KnowledgeEntry.id)).all()
    crew_recs = session.exec(select(m.CrewRec).order_by(m.CrewRec.idx)).all()
    crew_thread = session.exec(select(m.CrewTurn).order_by(m.CrewTurn.idx)).all()
    doc_sections = session.exec(select(m.DocSection).order_by(m.DocSection.idx)).all()

    # The global recent-event feed and config changes belong to the centerpiece.
    events = session.exec(
        select(m.SessionEvent).where(m.SessionEvent.session_id == CENTERPIECE).order_by(m.SessionEvent.idx)
    ).all()
    configs = session.exec(
        select(m.ConfigChange).where(m.ConfigChange.session_id == CENTERPIECE).order_by(m.ConfigChange.idx)
    ).all()

    return m.BootstrapRead(
        systems=_read(m.SystemRead, systems),
        sessions=_read(m.SessionRead, sessions),
        eventStream=_read(m.EventRead, events),
        configChanges=_read(m.ConfigChangeRead, configs),
        crewRecs=_read(m.CrewRecRead, crew_recs),
        knowledge=_read(m.KnowledgeRead, knowledge),
        docTree=_read(m.DocGroupRead, doc_sections),
        crewThread=_read(m.CrewTurnRead, crew_thread),
        diagnostics=build_diagnostics(session),
    )
