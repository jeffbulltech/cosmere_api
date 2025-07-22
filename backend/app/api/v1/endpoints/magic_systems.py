from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import SessionLocal
from app.models.magic_system import MagicSystem

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_magic_systems(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all magic systems with pagination"""
    magic_systems = db.query(MagicSystem).offset(skip).limit(limit).all()
    return magic_systems

@router.get("/{magic_system_id}")
def get_magic_system(magic_system_id: str, db: Session = Depends(get_db)):
    """Get a specific magic system by ID"""
    magic_system = db.query(MagicSystem).filter(MagicSystem.id == magic_system_id).first()
    if not magic_system:
        raise HTTPException(status_code=404, detail="Magic system not found")
    return magic_system
