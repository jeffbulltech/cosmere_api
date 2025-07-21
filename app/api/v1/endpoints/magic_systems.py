from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.core.database import get_db
from app.models.magic_system import MagicSystem
from app.models.world import World
from app.schemas.magic_system import (
    MagicSystemCreate, MagicSystemUpdate, MagicSystemResponse, MagicSystemList, MagicSystemPaginatedResponse, MagicSystemFilters
)
from app.schemas.world import WorldList

router = APIRouter(prefix="/magic-systems", tags=["Magic Systems"])


@router.get("/", response_model=MagicSystemPaginatedResponse)
def list_magic_systems(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    world_id: Optional[str] = None,
    type: Optional[str] = None,
    power_source: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(MagicSystem)
    if world_id:
        query = query.filter(MagicSystem.world_id == world_id)
    if type:
        query = query.filter(MagicSystem.type == type)
    if power_source:
        query = query.filter(MagicSystem.power_source == power_source)
    if search:
        query = query.filter(MagicSystem.name.ilike(f"%{search}%"))
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {
        "items": [MagicSystemList.model_validate(ms.to_dict()) for ms in items],
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_next": skip + limit < total,
        "has_prev": skip > 0,
    }


@router.post("/", response_model=MagicSystemResponse, status_code=status.HTTP_201_CREATED)
def create_magic_system(magic_system_in: MagicSystemCreate, db: Session = Depends(get_db)):
    magic_system = MagicSystem(**magic_system_in.model_dump())
    db.add(magic_system)
    db.commit()
    db.refresh(magic_system)
    return MagicSystemResponse.model_validate(magic_system.to_dict())


@router.get("/{magic_system_id}", response_model=MagicSystemResponse)
def get_magic_system(magic_system_id: str, db: Session = Depends(get_db)):
    magic_system = db.query(MagicSystem).filter(MagicSystem.id == magic_system_id).first()
    if not magic_system:
        raise HTTPException(status_code=404, detail="Magic system not found")
    return MagicSystemResponse.model_validate(magic_system.to_dict())


@router.put("/{magic_system_id}", response_model=MagicSystemResponse)
def update_magic_system(magic_system_id: str, magic_system_in: MagicSystemUpdate, db: Session = Depends(get_db)):
    magic_system = db.query(MagicSystem).filter(MagicSystem.id == magic_system_id).first()
    if not magic_system:
        raise HTTPException(status_code=404, detail="Magic system not found")
    for field, value in magic_system_in.model_dump(exclude_unset=True).items():
        setattr(magic_system, field, value)
    db.commit()
    db.refresh(magic_system)
    return MagicSystemResponse.model_validate(magic_system.to_dict())


@router.delete("/{magic_system_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_magic_system(magic_system_id: str, db: Session = Depends(get_db)):
    magic_system = db.query(MagicSystem).filter(MagicSystem.id == magic_system_id).first()
    if not magic_system:
        raise HTTPException(status_code=404, detail="Magic system not found")
    db.delete(magic_system)
    db.commit()
    return


@router.get("/world/{world_id}", response_model=List[MagicSystemList])
def get_magic_systems_by_world(world_id: str, db: Session = Depends(get_db)):
    magic_systems = db.query(MagicSystem).filter(MagicSystem.world_id == world_id).all()
    return [MagicSystemList.model_validate(ms.to_dict()) for ms in magic_systems]


@router.get("/{magic_system_id}/world", response_model=WorldList)
def get_magic_system_world(magic_system_id: str, db: Session = Depends(get_db)):
    magic_system = db.query(MagicSystem).filter(MagicSystem.id == magic_system_id).first()
    if not magic_system:
        raise HTTPException(status_code=404, detail="Magic system not found")
    world = db.query(World).filter(World.id == magic_system.world_id).first()
    if not world:
        raise HTTPException(status_code=404, detail="World not found")
    return WorldList.model_validate(world.to_dict()) 