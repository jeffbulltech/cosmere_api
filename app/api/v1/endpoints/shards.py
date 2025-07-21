from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.core.database import get_db
from app.models.shard import Shard
from app.models.world import World
from app.schemas.shard import (
    ShardCreate, ShardUpdate, ShardResponse, ShardList, ShardPaginatedResponse, ShardFilters
)
from app.schemas.world import WorldList

router = APIRouter(prefix="/shards", tags=["Shards"])


@router.get("/", response_model=List[ShardList])
def list_shards(
    intent: Optional[str] = None,
    vessel_status: Optional[str] = None,
    has_world_location: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Shard)
    if intent:
        query = query.filter(Shard.intent == intent)
    if vessel_status:
        query = query.filter(Shard.vessel_status == vessel_status)
    if has_world_location is not None:
        if has_world_location:
            query = query.filter(Shard.world_location_id.isnot(None))
        else:
            query = query.filter(Shard.world_location_id.is_(None))
    if search:
        query = query.filter(Shard.name.ilike(f"%{search}%"))
    items = query.all()
    return [ShardList.model_validate(s.to_dict()) for s in items]


@router.post("/", response_model=ShardResponse, status_code=status.HTTP_201_CREATED)
def create_shard(shard_in: ShardCreate, db: Session = Depends(get_db)):
    shard = Shard(**shard_in.model_dump())
    db.add(shard)
    db.commit()
    db.refresh(shard)
    return ShardResponse.model_validate(shard.to_dict())


@router.get("/{shard_id}", response_model=ShardResponse)
def get_shard(shard_id: str, db: Session = Depends(get_db)):
    shard = db.query(Shard).filter(Shard.id == shard_id).first()
    if not shard:
        raise HTTPException(status_code=404, detail="Shard not found")
    return ShardResponse.model_validate(shard.to_dict())


@router.put("/{shard_id}", response_model=ShardResponse)
def update_shard(shard_id: str, shard_in: ShardUpdate, db: Session = Depends(get_db)):
    shard = db.query(Shard).filter(Shard.id == shard_id).first()
    if not shard:
        raise HTTPException(status_code=404, detail="Shard not found")
    for field, value in shard_in.model_dump(exclude_unset=True).items():
        setattr(shard, field, value)
    db.commit()
    db.refresh(shard)
    return ShardResponse.model_validate(shard.to_dict())


@router.delete("/{shard_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shard(shard_id: str, db: Session = Depends(get_db)):
    shard = db.query(Shard).filter(Shard.id == shard_id).first()
    if not shard:
        raise HTTPException(status_code=404, detail="Shard not found")
    db.delete(shard)
    db.commit()
    return


@router.get("/{shard_id}/worlds", response_model=List[WorldList])
def get_shard_worlds(shard_id: str, db: Session = Depends(get_db)):
    shard = db.query(Shard).filter(Shard.id == shard_id).first()
    if not shard:
        raise HTTPException(status_code=404, detail="Shard not found")
    worlds = shard.worlds
    return [WorldList.model_validate(w.to_dict()) for w in worlds]


@router.get("/{shard_id}/world-location", response_model=WorldList)
def get_shard_world_location(shard_id: str, db: Session = Depends(get_db)):
    shard = db.query(Shard).filter(Shard.id == shard_id).first()
    if not shard:
        raise HTTPException(status_code=404, detail="Shard not found")
    if not shard.world_location_id:
        raise HTTPException(status_code=404, detail="Shard does not have a world location")
    world = db.query(World).filter(World.id == shard.world_location_id).first()
    if not world:
        raise HTTPException(status_code=404, detail="World not found")
    return WorldList.model_validate(world.to_dict()) 