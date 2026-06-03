# TapeForge Dock — backend

FastAPI + SQLModel API for TapeForge Dock. Serves the operational data the Dock
console reads (systems, sessions, knowledge, diagnostics, crew). Read-only and
seeded from sample data on first start; a real ingestion path comes later.

```bash
uv run fastapi dev --port 8001    # dev server at http://localhost:8001 (docs at /docs)
uv run pytest                     # tests
```

Key endpoints (under `/api/v1`):

- `GET /health`
- `GET /systems`, `GET /systems/{id}`
- `GET /sessions`, `GET /sessions/{id}` (detail includes events + config changes)
- `GET /knowledge`
- `GET /diagnostics`
- `GET /bootstrap` — the whole dataset in one payload (the frontend store loads this)

Configuration is read from environment / a `.env` file — copy `.env.example` to
`.env` and adjust. CORS defaults allow the Dock dev server (`:5174`).
