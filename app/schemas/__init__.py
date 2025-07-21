from .base import BaseSchema, PaginatedResponse
from .world import WorldCreate, WorldUpdate, WorldResponse, WorldList
from .series import SeriesCreate, SeriesUpdate, SeriesResponse, SeriesList
from .book import BookCreate, BookUpdate, BookResponse, BookList
from .character import CharacterCreate, CharacterUpdate, CharacterResponse, CharacterList
from .magic_system import MagicSystemCreate, MagicSystemUpdate, MagicSystemResponse, MagicSystemList
from .shard import ShardCreate, ShardUpdate, ShardResponse, ShardList
from .character_relationship import CharacterRelationshipCreate, CharacterRelationshipUpdate, CharacterRelationshipResponse

__all__ = [
    "BaseSchema",
    "PaginatedResponse",
    "WorldCreate",
    "WorldUpdate", 
    "WorldResponse",
    "WorldList",
    "SeriesCreate",
    "SeriesUpdate",
    "SeriesResponse",
    "SeriesList",
    "BookCreate",
    "BookUpdate",
    "BookResponse",
    "BookList",
    "CharacterCreate",
    "CharacterUpdate",
    "CharacterResponse",
    "CharacterList",
    "MagicSystemCreate",
    "MagicSystemUpdate",
    "MagicSystemResponse",
    "MagicSystemList",
    "ShardCreate",
    "ShardUpdate",
    "ShardResponse",
    "ShardList",
    "CharacterRelationshipCreate",
    "CharacterRelationshipUpdate",
    "CharacterRelationshipResponse",
] 