from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class BookResponse(BaseModel):
    id: str
    title: str
    isbn: Optional[str] = None
    publication_date: Optional[str] = None
    word_count: Optional[int] = None
    chronological_order: Optional[int] = None
    series_id: Optional[str] = None
    world_id: Optional[str] = None
    summary: Optional[str] = None
    cosmere_significance: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BookList(BaseModel):
    books: List[BookResponse]
    total: int
    skip: int
    limit: int
