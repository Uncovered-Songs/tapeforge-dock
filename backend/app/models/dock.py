"""SQLModel tables + read schemas for TapeForge Dock.

Tables are seeded (see app.seed) and served read-only. Read schemas define the
exact JSON shape the Dock frontend expects (mirroring src/dock/data.ts).
"""

from pydantic import ConfigDict, Field as PydField
from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

# --------------------------------------------------------------------------- #
# Tables
# --------------------------------------------------------------------------- #


class System(SQLModel, table=True):
    __tablename__ = "systems"

    id: str = Field(primary_key=True)
    kind: str
    name: str
    loc: str
    ver: str
    status: str
    uptime: str
    cpu: int
    sessions: int
    note: str


class Session(SQLModel, table=True):
    __tablename__ = "sessions"

    id: str = Field(primary_key=True)
    name: str
    type: str
    loc: str
    date: str
    start: str
    dur: str
    status: str
    systems: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    events: int
    issues: int
    engineer: str


class SessionEvent(SQLModel, table=True):
    __tablename__ = "session_events"

    id: int | None = Field(default=None, primary_key=True)
    session_id: str = Field(foreign_key="sessions.id", index=True)
    idx: int
    t: str
    tone: str
    src: str
    msg: str


class ConfigChange(SQLModel, table=True):
    __tablename__ = "config_changes"

    id: int | None = Field(default=None, primary_key=True)
    session_id: str = Field(foreign_key="sessions.id", index=True)
    idx: int
    t: str
    who: str
    what: str
    from_: str
    to_: str


class KnowledgeEntry(SQLModel, table=True):
    __tablename__ = "knowledge"

    id: str = Field(primary_key=True)
    kind: str
    title: str
    tags: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    by: str
    updated: str
    cites: int


class CrewRec(SQLModel, table=True):
    __tablename__ = "crew_recs"

    id: int | None = Field(default=None, primary_key=True)
    idx: int
    tone: str
    title: str
    body: str
    action: str


class CrewTurn(SQLModel, table=True):
    __tablename__ = "crew_turns"

    id: int | None = Field(default=None, primary_key=True)
    idx: int
    role: str
    text: str
    cites: list[dict] = Field(default_factory=list, sa_column=Column(JSON))
    agents: list[str] = Field(default_factory=list, sa_column=Column(JSON))


class Incident(SQLModel, table=True):
    __tablename__ = "incidents"

    id: int | None = Field(default=None, primary_key=True)
    idx: int
    tone: str
    sys: str
    issue: str
    when: str
    dur: str


class DocSection(SQLModel, table=True):
    __tablename__ = "doc_sections"

    id: int | None = Field(default=None, primary_key=True)
    idx: int
    group: str
    items: list[str] = Field(default_factory=list, sa_column=Column(JSON))


class MetricsRow(SQLModel, table=True):
    """Single-row time-series snapshot for the diagnostics charts."""

    __tablename__ = "metrics"

    id: int | None = Field(default=None, primary_key=True)
    clock_offset: list[float] = Field(default_factory=list, sa_column=Column(JSON))
    jitter: list[float] = Field(default_factory=list, sa_column=Column(JSON))
    latency: list[float] = Field(default_factory=list, sa_column=Column(JSON))
    packet_loss: list[float] = Field(default_factory=list, sa_column=Column(JSON))


# --------------------------------------------------------------------------- #
# Read schemas (exact frontend JSON)
# --------------------------------------------------------------------------- #


class SystemRead(SQLModel):
    id: str
    kind: str
    name: str
    loc: str
    ver: str
    status: str
    uptime: str
    cpu: int
    sessions: int
    note: str


class SessionRead(SQLModel):
    id: str
    name: str
    type: str
    loc: str
    date: str
    start: str
    dur: str
    status: str
    systems: list[str]
    events: int
    issues: int
    engineer: str


class EventRead(SQLModel):
    t: str
    tone: str
    src: str
    msg: str


class ConfigChangeRead(SQLModel):
    # `from`/`to` are reserved words, so store as from_/to_ and serialize aliased.
    model_config = ConfigDict(populate_by_name=True)  # type: ignore[assignment]

    t: str
    who: str
    what: str
    from_: str = PydField(serialization_alias="from")
    to_: str = PydField(serialization_alias="to")


class SessionDetailRead(SessionRead):
    eventStream: list[EventRead] = []
    configChanges: list[ConfigChangeRead] = []


class KnowledgeRead(SQLModel):
    id: str
    kind: str
    title: str
    tags: list[str]
    by: str
    updated: str
    cites: int


class CrewRecRead(SQLModel):
    tone: str
    title: str
    body: str
    action: str


class CrewTurnRead(SQLModel):
    role: str
    text: str
    cites: list[dict] = []
    agents: list[str] = []


class IncidentRead(SQLModel):
    tone: str
    sys: str
    issue: str
    when: str
    dur: str


class DiagnosticsRead(SQLModel):
    clockOffset: list[float]
    jitter: list[float]
    latency: list[float]
    packetLoss: list[float]
    incidents: list[IncidentRead]


class DocGroupRead(SQLModel):
    group: str
    items: list[str]


class BootstrapRead(SQLModel):
    """Everything the Dock frontend needs to populate its store in one call."""

    systems: list[SystemRead]
    sessions: list[SessionRead]
    eventStream: list[EventRead]
    configChanges: list[ConfigChangeRead]
    crewRecs: list[CrewRecRead]
    knowledge: list[KnowledgeRead]
    docTree: list[DocGroupRead]
    crewThread: list[CrewTurnRead]
    diagnostics: DiagnosticsRead
