"""
Shards API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db

router = APIRouter()


@router.get("/")
async def get_shards(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """Get all shards with pagination."""
    # TODO: Implement in Phase 4
    return {"message": "Shards endpoint - to be implemented"}


@router.get("/{shard_id}")
async def get_shard(shard_id: str, db: Session = Depends(get_db)):
    """Get a specific shard by ID."""
    # TODO: Implement in Phase 4
    return {"message": f"Shard {shard_id} - to be implemented"}


@router.get("/{shard_id}/vessels")
async def get_shard_vessels(shard_id: str, db: Session = Depends(get_db)):
    """Get vessels of a specific shard."""
    # TODO: Implement in Phase 4
    return {"message": f"Vessels of shard {shard_id} - to be implemented"} 