from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import SessionLocal
from app.models.world import World

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_worlds(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all worlds with pagination"""
    worlds = db.query(World).offset(skip).limit(limit).all()
    return worlds

@router.get("/{world_id}")
def get_world(world_id: str, db: Session = Depends(get_db)):
    """Get a specific world by ID"""
    world = db.query(World).filter(World.id == world_id).first()
    if not world:
        raise HTTPException(status_code=404, detail="World not found")
    return world
