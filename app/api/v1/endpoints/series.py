from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.core.database import get_db
from app.models.series import Series
from app.models.book import Book
from app.models.world import World
from app.schemas.series import (
    SeriesCreate, SeriesUpdate, SeriesResponse, SeriesList, SeriesPaginatedResponse
)
from app.schemas.book import BookList
from app.schemas.world import WorldList

router = APIRouter(prefix="/series", tags=["Series"])


@router.get("/", response_model=List[SeriesList])
def list_series(db: Session = Depends(get_db)):
    series = db.query(Series).all()
    return [SeriesList.model_validate(s.to_dict()) for s in series]


@router.post("/", response_model=SeriesResponse, status_code=status.HTTP_201_CREATED)
def create_series(series_in: SeriesCreate, db: Session = Depends(get_db)):
    series = Series(**series_in.model_dump())
    db.add(series)
    db.commit()
    db.refresh(series)
    return SeriesResponse.model_validate(series.to_dict())


@router.get("/{series_id}", response_model=SeriesResponse)
def get_series(series_id: str, db: Session = Depends(get_db)):
    series = db.query(Series).filter(Series.id == series_id).first()
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    return SeriesResponse.model_validate(series.to_dict())


@router.put("/{series_id}", response_model=SeriesResponse)
def update_series(series_id: str, series_in: SeriesUpdate, db: Session = Depends(get_db)):
    series = db.query(Series).filter(Series.id == series_id).first()
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    for field, value in series_in.model_dump(exclude_unset=True).items():
        setattr(series, field, value)
    db.commit()
    db.refresh(series)
    return SeriesResponse.model_validate(series.to_dict())


@router.delete("/{series_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_series(series_id: str, db: Session = Depends(get_db)):
    series = db.query(Series).filter(Series.id == series_id).first()
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    db.delete(series)
    db.commit()
    return


@router.get("/{series_id}/books", response_model=List[BookList])
def get_series_books(series_id: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.series_id == series_id).all()
    return [BookList.model_validate(b.to_dict()) for b in books]


@router.get("/{series_id}/worlds", response_model=List[WorldList])
def get_series_worlds(series_id: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.series_id == series_id).all()
    world_ids = set(b.world_id for b in books if b.world_id)
    worlds = db.query(World).filter(World.id.in_(world_ids)).all() if world_ids else []
    return [WorldList.model_validate(w.to_dict()) for w in worlds] 