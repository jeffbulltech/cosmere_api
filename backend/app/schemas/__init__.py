"""
API schemas for request/response models.
"""
from app.schemas.base import BaseSchema, PaginatedResponse
from app.schemas.world import WorldCreate, WorldUpdate, WorldResponse, WorldSummary
from app.schemas.book import BookCreate, BookUpdate, BookResponse, BookSummary
from app.schemas.character import CharacterCreate, CharacterUpdate, CharacterResponse, CharacterSummary
from app.schemas.series import SeriesCreate, SeriesUpdate, SeriesResponse, SeriesSummary
from app.schemas.magic_system import MagicSystemCreate, MagicSystemUpdate, MagicSystemResponse, MagicSystemSummary
from app.schemas.shard import ShardCreate, ShardUpdate, ShardResponse, ShardSummary
from app.schemas.search import SearchRequest, SearchResponse, SearchSuggestion

__all__ = [
    "BaseSchema",
    "PaginatedResponse",
    "WorldCreate",
    "WorldUpdate", 
    "WorldResponse",
    "WorldSummary",
    "BookCreate",
    "BookUpdate",
    "BookResponse", 
    "BookSummary",
    "CharacterCreate",
    "CharacterUpdate",
    "CharacterResponse",
    "CharacterSummary",
    "SeriesCreate",
    "SeriesUpdate",
    "SeriesResponse",
    "SeriesSummary",
    "MagicSystemCreate",
    "MagicSystemUpdate",
    "MagicSystemResponse",
    "MagicSystemSummary",
    "ShardCreate",
    "ShardUpdate",
    "ShardResponse",
    "ShardSummary",
    "SearchRequest",
    "SearchResponse",
    "SearchSuggestion",
]
