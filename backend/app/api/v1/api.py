"""
Main API router for v1 endpoints.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import books, characters, worlds, series, magic_systems, shards, search, health

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(characters.router, prefix="/characters", tags=["characters"])
api_router.include_router(worlds.router, prefix="/worlds", tags=["worlds"])
api_router.include_router(series.router, prefix="/series", tags=["series"])
api_router.include_router(magic_systems.router, prefix="/magic-systems", tags=["magic-systems"])
api_router.include_router(shards.router, prefix="/shards", tags=["shards"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
