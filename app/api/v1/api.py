from fastapi import APIRouter
from app.api.v1.endpoints import (
    worlds, characters, books, series, magic_systems, shards, character_relationships, search
)

api_router = APIRouter()

api_router.include_router(worlds.router)
api_router.include_router(characters.router)
api_router.include_router(books.router)
api_router.include_router(series.router)
api_router.include_router(magic_systems.router)
api_router.include_router(shards.router)
api_router.include_router(character_relationships.router)
api_router.include_router(search.router) 