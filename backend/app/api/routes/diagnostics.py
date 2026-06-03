from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session as DBSession, select

from app.core.db import get_session
from app.models import dock as m

router = APIRouter(tags=["diagnostics"])


def build_diagnostics(session: DBSession) -> m.DiagnosticsRead:
    metrics = session.exec(select(m.MetricsRow)).first()
    if not metrics:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Diagnostics not seeded"
        )
    incidents = session.exec(select(m.Incident).order_by(m.Incident.idx)).all()
    return m.DiagnosticsRead(
        clockOffset=metrics.clock_offset,
        jitter=metrics.jitter,
        latency=metrics.latency,
        packetLoss=metrics.packet_loss,
        incidents=[m.IncidentRead.model_validate(i, from_attributes=True) for i in incidents],
    )


@router.get("/diagnostics", response_model=m.DiagnosticsRead)
def get_diagnostics(session: DBSession = Depends(get_session)) -> m.DiagnosticsRead:
    return build_diagnostics(session)
