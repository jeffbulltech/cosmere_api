from fastapi import APIRouter
from app.api.v1.endpoints import books, characters, worlds, magic_systems

api_router = APIRouter()

api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(characters.router, prefix="/characters", tags=["characters"])
api_router.include_router(worlds.router, prefix="/worlds", tags=["worlds"])
api_router.include_router(magic_systems.router, prefix="/magic-systems", tags=["magic-systems"])
