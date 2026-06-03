from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

import app.core.db as db
from app.core.db import get_session
from app.main import app
from app.seed import seed_db


@pytest.fixture(name="client")
def client_fixture(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    engine: Engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    # Point both the seed and the request dependency at the in-memory engine.
    monkeypatch.setattr(db, "engine", engine)
    seed_db()

    def get_session_override() -> Generator[Session, None, None]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_health(client: TestClient) -> None:
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_list_systems(client: TestClient) -> None:
    r = client.get("/api/v1/systems")
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 8
    assert {"id", "kind", "name", "status", "cpu", "note"} <= body[0].keys()


def test_get_system_404(client: TestClient) -> None:
    assert client.get("/api/v1/systems/nope").status_code == 404
    assert client.get("/api/v1/systems/scope-bc").json()["status"] == "crit"


def test_sessions_newest_first(client: TestClient) -> None:
    r = client.get("/api/v1/sessions")
    assert r.status_code == 200
    ids = [s["id"] for s in r.json()]
    assert ids == sorted(ids, reverse=True)
    assert ids[0] == "S-2041"


def test_session_detail_has_events_and_config(client: TestClient) -> None:
    r = client.get("/api/v1/sessions/S-2040")
    assert r.status_code == 200
    body = r.json()
    assert len(body["eventStream"]) == 10
    # `from`/`to` are serialized with their reserved-word keys.
    cfg = body["configChanges"][0]
    assert "from" in cfg and "to" in cfg
    assert isinstance(body["systems"], list)


def test_session_detail_404(client: TestClient) -> None:
    assert client.get("/api/v1/sessions/S-9999").status_code == 404


def test_knowledge(client: TestClient) -> None:
    r = client.get("/api/v1/knowledge")
    assert r.status_code == 200
    assert len(r.json()) == 6
    assert isinstance(r.json()[0]["tags"], list)


def test_diagnostics(client: TestClient) -> None:
    r = client.get("/api/v1/diagnostics")
    assert r.status_code == 200
    body = r.json()
    assert len(body["clockOffset"]) == 12
    assert len(body["incidents"]) == 4


def test_bootstrap_has_everything(client: TestClient) -> None:
    r = client.get("/api/v1/bootstrap")
    assert r.status_code == 200
    body = r.json()
    for key in ("systems", "sessions", "eventStream", "configChanges", "crewRecs", "knowledge", "docTree", "crewThread", "diagnostics"):
        assert key in body, key
    assert len(body["systems"]) == 8
    assert len(body["eventStream"]) == 10
    assert len(body["docTree"]) == 4
    assert len(body["crewThread"]) == 4
    assert body["diagnostics"]["incidents"][0]["tone"] == "crit"
