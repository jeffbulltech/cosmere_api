"""
Repository layer for data access.
"""
from app.repositories.base import BaseRepository
from app.repositories.world_repository import WorldRepository
from app.repositories.series_repository import SeriesRepository
from app.repositories.book_repository import BookRepository
from app.repositories.character_repository import CharacterRepository
from app.repositories.magic_system_repository import MagicSystemRepository
from app.repositories.shard_repository import ShardRepository

__all__ = [
    "BaseRepository",
    "WorldRepository",
    "SeriesRepository",
    "BookRepository",
    "CharacterRepository",
    "MagicSystemRepository",
    "ShardRepository",
] 