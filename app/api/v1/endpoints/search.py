from fastapi import APIRouter, Query, Depends, HTTPException
from typing import Optional, Dict, Any
from app.services.search_service import SearchService
from app.schemas.character import CharacterSearchResult
from app.schemas.base import SearchResult

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/characters", response_model=SearchResult[CharacterSearchResult])
async def search_characters(
    q: str = Query(..., min_length=1, description="Search query"),
    world: Optional[str] = Query(None, description="Filter by world name"),
    status: Optional[str] = Query(None, description="Filter by status"),
    size: int = Query(20, ge=1, le=100),
):
    search_service = SearchService()
    filters = {}
    if world:
        filters["world_name"] = world
    if status:
        filters["status"] = status
    results = await search_service.search_characters(q, filters, size)
    hits = results["hits"]["hits"]
    return {
        "items": [CharacterSearchResult.model_validate(hit["_source"]) for hit in hits],
        "total": results["hits"]["total"]["value"],
        "query": q,
        "took": results["took"] / 1000.0,
        "has_next": len(hits) == size,
        "has_prev": False,
    }

@router.get("/global", response_model=SearchResult[Any])
async def global_search(
    q: str = Query(..., min_length=1, description="Search across all content"),
    size: int = Query(20, ge=1, le=100),
):
    search_service = SearchService()
    results = await search_service.global_search(q, size)
    hits = results["hits"]["hits"]
    return {
        "items": [hit["_source"] for hit in hits],
        "total": results["hits"]["total"]["value"],
        "query": q,
        "took": results["took"] / 1000.0,
        "has_next": len(hits) == size,
        "has_prev": False,
    } 