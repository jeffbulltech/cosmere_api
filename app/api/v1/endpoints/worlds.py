from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.core.database import get_db
from app.models.world import World
from app.models.character import Character
from app.models.magic_system import MagicSystem
from app.schemas.world import (
    WorldCreate, WorldUpdate, WorldResponse, WorldList, WorldPaginatedResponse, WorldFilters
)
from app.schemas.character import CharacterList
from app.schemas.magic_system import MagicSystemList
from app.services.cache_service import cache_response

router = APIRouter(prefix="/worlds", tags=["Worlds"])


@router.get("/", response_model=WorldPaginatedResponse)
@cache_response(ttl=300, key_prefix="worlds:list")  # Cache for 5 minutes
def list_worlds(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    system: Optional[str] = None,
    technology_level: Optional[str] = None,
    has_shard: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    query = db.query(World)
    if system:
        query = query.filter(World.system == system)
    if technology_level:
        query = query.filter(World.technology_level == technology_level)
    if has_shard is not None:
        if has_shard:
            query = query.filter(World.shard_id.isnot(None))
        else:
            query = query.filter(World.shard_id.is_(None))
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {
        "items": [WorldList.model_validate(w.to_dict()) for w in items],
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_next": skip + limit < total,
        "has_prev": skip > 0,
    }


@router.post("/", response_model=WorldResponse, status_code=status.HTTP_201_CREATED)
def create_world(world_in: WorldCreate, db: Session = Depends(get_db)):
    world = World(**world_in.model_dump())
    db.add(world)
    db.commit()
    db.refresh(world)
    return WorldResponse.model_validate(world.to_dict())


@router.get("/{world_id}", response_model=WorldResponse)
def get_world(world_id: str, db: Session = Depends(get_db)):
    world = db.query(World).filter(World.id == world_id).first()
    if not world:
        raise HTTPException(status_code=404, detail="World not found")
    return WorldResponse.model_validate(world.to_dict())


@router.put("/{world_id}", response_model=WorldResponse)
def update_world(world_id: str, world_in: WorldUpdate, db: Session = Depends(get_db)):
    world = db.query(World).filter(World.id == world_id).first()
    if not world:
        raise HTTPException(status_code=404, detail="World not found")
    for field, value in world_in.model_dump(exclude_unset=True).items():
        setattr(world, field, value)
    db.commit()
    db.refresh(world)
    return WorldResponse.model_validate(world.to_dict())


@router.delete("/{world_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_world(world_id: str, db: Session = Depends(get_db)):
    world = db.query(World).filter(World.id == world_id).first()
    if not world:
        raise HTTPException(status_code=404, detail="World not found")
    db.delete(world)
    db.commit()
    return


@router.get("/{world_id}/characters", response_model=List[CharacterList])
def get_world_characters(world_id: str, db: Session = Depends(get_db)):
    world = db.query(World).filter(World.id == world_id).first()
    if not world:
        raise HTTPException(status_code=404, detail="World not found")
    characters = db.query(Character).filter(Character.world_of_origin_id == world_id).all()
    return [CharacterList.model_validate(c.to_dict()) for c in characters]


@router.get("/{world_id}/magic-systems", response_model=List[MagicSystemList])
def get_world_magic_systems(world_id: str, db: Session = Depends(get_db)):
    world = db.query(World).filter(World.id == world_id).first()
    if not world:
        raise HTTPException(status_code=404, detail="World not found")
    magic_systems = db.query(MagicSystem).filter(MagicSystem.world_id == world_id).all()
    return [MagicSystemList.model_validate(ms.to_dict()) for ms in magic_systems] 