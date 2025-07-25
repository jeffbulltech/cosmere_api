"""
Database models for the Cosmere API.
"""
from app.models.base import Base
from app.models.world import World
from app.models.series import Series
from app.models.book import Book
from app.models.character import Character
from app.models.magic_system import MagicSystem
from app.models.shard import Shard
from app.models.character_relationship import CharacterRelationship
from app.models.book_character import BookCharacter
from app.models.character_magic_system import CharacterMagicSystem

__all__ = [
    "Base",
    "World",
    "Series", 
    "Book",
    "Character",
    "MagicSystem",
    "Shard",
    "CharacterRelationship",
    "BookCharacter",
    "CharacterMagicSystem",
]
