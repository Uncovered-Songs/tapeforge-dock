from fastapi import APIRouter

from app.api.routes import bootstrap, crew, diagnostics, health, knowledge, sessions, systems

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(systems.router)
api_router.include_router(sessions.router)
api_router.include_router(knowledge.router)
api_router.include_router(diagnostics.router)
api_router.include_router(bootstrap.router)
api_router.include_router(crew.router)
