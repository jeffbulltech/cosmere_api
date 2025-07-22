from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.core.database import get_db
from app.models.magic_system import MagicSystem
from app.models.world import World

router = APIRouter(prefix="/magic-systems", tags=["Magic Systems"])


@router.get("/")
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
    
    # Convert to simple dict format to avoid model method issues
    result = []
    for ms in items:
        result.append({
            "id": ms.id,
            "name": ms.name,
            "world_id": ms.world_id,
            "type": ms.type,
            "power_source": ms.power_source,
            "description": ms.description,
            "created_at": ms.created_at.isoformat() if ms.created_at else None,
            "updated_at": ms.updated_at.isoformat() if ms.updated_at else None
        })
    
    return {
        "items": result,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_next": skip + limit < total,
        "has_prev": skip > 0,
    }


@router.get("/{magic_system_id}")
def get_magic_system(magic_system_id: str, db: Session = Depends(get_db)):
    magic_system = db.query(MagicSystem).filter(MagicSystem.id == magic_system_id).first()
    if not magic_system:
        raise HTTPException(status_code=404, detail="Magic system not found")
    return {
        "id": magic_system.id,
        "name": magic_system.name,
        "world_id": magic_system.world_id,
        "type": magic_system.type,
        "power_source": magic_system.power_source,
        "description": magic_system.description,
        "created_at": magic_system.created_at.isoformat() if magic_system.created_at else None,
        "updated_at": magic_system.updated_at.isoformat() if magic_system.updated_at else None
    } 