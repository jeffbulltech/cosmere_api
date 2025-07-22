# Cosmere API Implementation Plan

## Project Overview
**Duration**: 6 months (can be compressed to 4 months with full-time dedication)  
**Team Size**: 1-3 developers  
**Methodology**: Agile with 2-week sprints  

## Phase 1: Foundation & Core Infrastructure (Weeks 1-4)

### Week 1: Project Setup & Environment

#### Day 1-2: Repository & Development Environment
```bash
# 1. Initialize repositories
mkdir cosmere-api && cd cosmere-api
git init
mkdir backend frontend docs

# 2. Backend project structure
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic pydantic redis
```

**Deliverables:**
- [x] GitHub repositories created (backend, frontend, docs)
- [x] Python virtual environment configured
- [x] Basic project structure established
- [x] Development dependencies installed
- [x] .gitignore and README files created

#### Day 3-4: Database Setup
```python
# backend/app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/cosmere")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

**Tasks:**
- [ ] Install and configure PostgreSQL locally
- [ ] Create development database
- [ ] Set up SQLAlchemy with basic configuration
- [ ] Initialize Alembic for migrations
- [ ] Create first migration (empty tables)

#### Day 5-7: Basic FastAPI Application
```python
# backend/app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title="Cosmere API",
    description="API for Brandon Sanderson's Cosmere universe",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
```

**Deliverables:**
- [x] FastAPI application skeleton
- [x] CORS middleware configured
- [x] Basic health check endpoint
- [x] Environment configuration setup
- [x] Docker development environment

### Week 2: Core Data Models

#### Day 1-3: Define Base Models
```python
# backend/app/models/base.py
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

**Priority Order for Models:**
1. **Worlds** (foundational - everything else references these)
2. **Series** (book organization)
3. **Books** (core content)
4. **Characters** (main entities)
5. **Magic Systems** (world-specific)

#### Day 4-5: Implement Core Models
```python
# backend/app/models/world.py
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from .base import BaseModel

class World(BaseModel):
    __tablename__ = "worlds"
    
    name = Column(String(255), nullable=False, unique=True)
    system = Column(String(255))
    geography = Column(JSONB)
    culture_notes = Column(Text)
    technology_level = Column(String(100))
```

**Tasks:**
- [ ] Create World model with JSONB fields
- [ ] Create Series model
- [ ] Create Book model with foreign keys
- [ ] Create Character model with relationships
- [ ] Write and run migrations

#### Day 6-7: Model Relationships
```python
# backend/app/models/relationships.py
from sqlalchemy import Column, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

# Many-to-many association table
character_books = Table(
    'character_books',
    BaseModel.metadata,
    Column('character_id', UUID(as_uuid=True), ForeignKey('characters.id')),
    Column('book_id', UUID(as_uuid=True), ForeignKey('books.id')),
    Column('role', String(100))
)
```

**Deliverables:**
- [x] All core models implemented
- [x] Relationships properly defined
- [x] Database migrations created and tested
- [x] Model validation with Pydantic schemas

### Week 3: Basic CRUD Operations

#### Day 1-2: Pydantic Schemas
```python
# backend/app/schemas/character.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class CharacterBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    aliases: Optional[List[str]] = []
    species: Optional[str] = None
    status: Optional[str] = "unknown"

class CharacterCreate(CharacterBase):
    world_of_origin_id: uuid.UUID
    biography: Optional[str] = None

class Character(CharacterBase):
    id: uuid.UUID
    world_of_origin_id: uuid.UUID
    magic_abilities: Optional[Dict[str, Any]] = {}
    created_at: datetime
    
    class Config:
        from_attributes = True
```

#### Day 3-4: Repository Pattern
```python
# backend/app/repositories/character_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterUpdate
from typing import List, Optional

class CharacterRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, character_data: CharacterCreate) -> Character:
        character = Character(**character_data.dict())
        self.db.add(character)
        self.db.commit()
        self.db.refresh(character)
        return character
    
    def get_by_id(self, character_id: str) -> Optional[Character]:
        return self.db.query(Character).filter(Character.id == character_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Character]:
        return self.db.query(Character).offset(skip).limit(limit).all()
```

#### Day 5-7: API Endpoints
```python
# backend/app/api/v1/endpoints/characters.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.character_repository import CharacterRepository
from app.schemas.character import Character, CharacterCreate
from typing import List

router = APIRouter()

@router.post("/", response_model=Character)
def create_character(
    character_data: CharacterCreate,
    db: Session = Depends(get_db)
):
    repo = CharacterRepository(db)
    return repo.create(character_data)

@router.get("/{character_id}", response_model=Character)
def get_character(character_id: str, db: Session = Depends(get_db)):
    repo = CharacterRepository(db)
    character = repo.get_by_id(character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character
```

**Deliverables:**
- [x] Complete CRUD operations for all entities
- [x] Repository pattern implemented
- [x] API endpoints with proper validation
- [x] Error handling and HTTP status codes
- [x] Basic API documentation generated

### Week 4: Testing & Data Seeding

#### Day 1-3: Unit Tests
```python
# backend/tests/test_character_repository.py
import pytest
from sqlalchemy.orm import Session
from app.repositories.character_repository import CharacterRepository
from app.schemas.character import CharacterCreate
from tests.conftest import TestingSessionLocal

def test_create_character():
    db = TestingSessionLocal()
    repo = CharacterRepository(db)
    
    character_data = CharacterCreate(
        name="Kaladin",
        world_of_origin_id="roshar-uuid",
        species="Human",
        status="alive"
    )
    
    character = repo.create(character_data)
    assert character.name == "Kaladin"
    assert character.id is not None
```

#### Day 4-5: Integration Tests
```python
# backend/tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_character():
    response = client.post("/api/v1/characters/", json={
        "name": "Kaladin",
        "world_of_origin_id": "valid-uuid",
        "species": "Human"
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Kaladin"
```

#### Day 6-7: Sample Data Seeding
```python
# backend/scripts/seed_data.py
from app.core.database import SessionLocal
from app.models import World, Book, Character, Series

def seed_basic_data():
    db = SessionLocal()
    
    # Create Roshar
    roshar = World(
        name="Roshar",
        system="Rosharan System",
        geography={"type": "storm-swept", "highstorms": True},
        technology_level="medieval_plus"
    )
    db.add(roshar)
    
    # Create Stormlight Archive series
    stormlight = Series(name="The Stormlight Archive")
    db.add(stormlight)
    
    # Create Way of Kings
    wok = Book(
        title="The Way of Kings",
        series=stormlight,
        world=roshar,
        publication_date="2010-08-31",
        chronological_order=1
    )
    db.add(wok)
    
    db.commit()
```

**Deliverables:**
- [x] Comprehensive test suite (unit & integration)
- [x] Test database configuration
- [x] Sample data seeding script
- [x] CI/CD pipeline setup (GitHub Actions)
- [x] Code coverage reports

## Phase 2: Enhanced Features & Search (Weeks 5-8)

### Week 5: Advanced Querying & Filtering

#### Day 1-3: Complex Queries
```python
# backend/app/repositories/character_repository.py (enhanced)
def get_characters_by_world(self, world_id: str) -> List[Character]:
    return self.db.query(Character).filter(
        Character.world_of_origin_id == world_id
    ).all()

def get_characters_by_magic_ability(self, ability: str) -> List[Character]:
    return self.db.query(Character).filter(
        Character.magic_abilities.op('?')(ability)
    ).all()

def search_characters(self, query: str, filters: dict = None) -> List[Character]:
    q = self.db.query(Character)
    
    # Text search
    if query:
        q = q.filter(
            or_(
                Character.name.ilike(f"%{query}%"),
                Character.aliases.any(query),
                Character.biography.ilike(f"%{query}%")
            )
        )
    
    # Apply filters
    if filters:
        if 'world_id' in filters:
            q = q.filter(Character.world_of_origin_id == filters['world_id'])
        if 'status' in filters:
            q = q.filter(Character.status == filters['status'])
    
    return q.all()
```

#### Day 4-5: Pagination & Sorting
```python
# backend/app/schemas/common.py
from pydantic import BaseModel, Field
from typing import Optional, List, Generic, TypeVar

T = TypeVar('T')

class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=1000)
    sort_by: Optional[str] = None
    sort_order: str = Field("asc", regex="^(asc|desc)$")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_prev: bool
```

#### Day 6-7: Advanced Endpoints
```python
# backend/app/api/v1/endpoints/characters.py (enhanced)
@router.get("/", response_model=PaginatedResponse[Character])
def get_characters(
    pagination: PaginationParams = Depends(),
    world_id: Optional[str] = None,
    status: Optional[str] = None,
    magic_ability: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    repo = CharacterRepository(db)
    filters = {k: v for k, v in {
        'world_id': world_id,
        'status': status,
        'magic_ability': magic_ability
    }.items() if v is not None}
    
    characters = repo.search_characters(search or "", filters)
    total = len(characters)
    
    # Apply pagination
    items = characters[pagination.skip:pagination.skip + pagination.limit]
    
    return PaginatedResponse(
        items=items,
        total=total,
        skip=pagination.skip,
        limit=pagination.limit,
        has_next=pagination.skip + pagination.limit < total,
        has_prev=pagination.skip > 0
    )
```

### Week 6: Elasticsearch Integration

#### Day 1-2: Elasticsearch Setup
```python
# backend/app/core/elasticsearch.py
from elasticsearch import AsyncElasticsearch
from app.core.config import settings

es = AsyncElasticsearch([settings.ELASTICSEARCH_URL])

# Character index mapping
CHARACTER_MAPPING = {
    "mappings": {
        "properties": {
            "name": {"type": "text", "analyzer": "standard"},
            "aliases": {"type": "text", "analyzer": "standard"},
            "biography": {"type": "text", "analyzer": "standard"},
            "world_name": {"type": "keyword"},
            "magic_abilities": {"type": "nested"},
            "status": {"type": "keyword"},
            "created_at": {"type": "date"}
        }
    }
}
```

#### Day 3-4: Search Service
```python
# backend/app/services/search_service.py
from elasticsearch import AsyncElasticsearch
from typing import List, Dict, Any, Optional

class SearchService:
    def __init__(self, es: AsyncElasticsearch):
        self.es = es
    
    async def index_character(self, character: Dict[str, Any]):
        await self.es.index(
            index="characters",
            id=character["id"],
            body=character
        )
    
    async def search_characters(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        size: int = 50
    ) -> Dict[str, Any]:
        search_body = {
            "query": {
                "bool": {
                    "must": []
                }
            },
            "size": size,
            "sort": [{"_score": {"order": "desc"}}]
        }
        
        if query:
            search_body["query"]["bool"]["must"].append({
                "multi_match": {
                    "query": query,
                    "fields": ["name^3", "aliases^2", "biography"],
                    "type": "best_fields",
                    "fuzziness": "AUTO"
                }
            })
        else:
            search_body["query"] = {"match_all": {}}
        
        if filters:
            filter_clauses = []
            for key, value in filters.items():
                filter_clauses.append({"term": {key: value}})
            
            if filter_clauses:
                search_body["query"]["bool"]["filter"] = filter_clauses
        
        result = await self.es.search(index="characters", body=search_body)
        return result
```

#### Day 5-7: Search Endpoints
```python
# backend/app/api/v1/endpoints/search.py
from fastapi import APIRouter, Depends, Query
from app.services.search_service import SearchService
from app.core.elasticsearch import es
from typing import Optional, List

router = APIRouter()

@router.get("/characters")
async def search_characters(
    q: str = Query(..., description="Search query"),
    world: Optional[str] = Query(None, description="Filter by world"),
    status: Optional[str] = Query(None, description="Filter by status"),
    size: int = Query(20, ge=1, le=100)
):
    search_service = SearchService(es)
    
    filters = {}
    if world:
        filters["world_name"] = world
    if status:
        filters["status"] = status
    
    results = await search_service.search_characters(q, filters, size)
    
    return {
        "query": q,
        "total": results["hits"]["total"]["value"],
        "results": [hit["_source"] for hit in results["hits"]["hits"]],
        "took": results["took"]
    }

@router.get("/global")
async def global_search(
    q: str = Query(..., description="Search across all content"),
    size: int = Query(20, ge=1, le=100)
):
    search_service = SearchService(es)
    
    # Search across multiple indices
    results = await search_service.multi_index_search(q, size)
    
    return {
        "query": q,
        "results": results
    }
```

### Week 7: Caching & Performance

#### Day 1-2: Redis Caching
```python
# backend/app/core/cache.py
import redis.asyncio as redis
import json
from typing import Any, Optional
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL)

class CacheService:
    def __init__(self):
        self.client = redis_client
        self.default_ttl = 3600  # 1 hour
    
    async def get(self, key: str) -> Optional[Any]:
        value = await self.client.get(key)
        return json.loads(value) if value else None
    
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        ttl = ttl or self.default_ttl
        return await self.client.setex(
            key, 
            ttl, 
            json.dumps(value, default=str)
        )
    
    async def delete(self, key: str) -> int:
        return await self.client.delete(key)
    
    async def clear_pattern(self, pattern: str) -> int:
        keys = await self.client.keys(pattern)
        if keys:
            return await self.client.delete(*keys)
        return 0

# Decorator for caching
def cache_response(ttl: int = 3600, key_prefix: str = ""):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            cache_service = CacheService()
            
            # Create cache key
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = await cache_service.get(cache_key)
            if cached_result:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache_service.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator
```

#### Day 3-4: Database Optimization
```python
# backend/app/repositories/character_repository.py (optimized)
from sqlalchemy.orm import joinedload, selectinload

class CharacterRepository:
    def get_character_with_relationships(self, character_id: str) -> Optional[Character]:
        return self.db.query(Character).options(
            joinedload(Character.world_of_origin),
            selectinload(Character.books),
            selectinload(Character.magic_systems)
        ).filter(Character.id == character_id).first()
    
    def get_characters_optimized(self, skip: int = 0, limit: int = 100) -> List[Character]:
        return self.db.query(Character).options(
            joinedload(Character.world_of_origin)
        ).offset(skip).limit(limit).all()
```

#### Day 5-7: Performance Monitoring
```python
# backend/app/middleware/performance.py
import time
from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)

class PerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        # Log slow requests
        if process_time > 1.0:  # Log requests taking more than 1 second
            logger.warning(
                f"Slow request: {request.method} {request.url} took {process_time:.2f}s"
            )
        
        return response
```

### Week 8: Relationship APIs & Complex Queries

#### Day 1-3: Character Relationships
```python
# backend/app/models/character_relationship.py
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import BaseModel

class CharacterRelationship(BaseModel):
    __tablename__ = "character_relationships"
    
    character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"))
    related_character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"))
    relationship_type = Column(String(100))  # friend, enemy, mentor, etc.
    description = Column(Text)
    book_context_id = Column(UUID(as_uuid=True), ForeignKey("books.id"))
    
    character = relationship("Character", foreign_keys=[character_id])
    related_character = relationship("Character", foreign_keys=[related_character_id])
    book_context = relationship("Book")
```

#### Day 4-5: Relationship Endpoints
```python
# backend/app/api/v1/endpoints/relationships.py
@router.get("/characters/{character_id}/relationships")
async def get_character_relationships(
    character_id: str,
    relationship_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    repo = RelationshipRepository(db)
    relationships = repo.get_character_relationships(character_id, relationship_type)
    
    return {
        "character_id": character_id,
        "relationships": relationships
    }

@router.get("/characters/{character_id}/network")
async def get_character_network(
    character_id: str,
    depth: int = Query(2, ge=1, le=3),
    db: Session = Depends(get_db)
):
    """Get character relationship network up to specified depth"""
    repo = RelationshipRepository(db)
    network = repo.get_relationship_network(character_id, depth)
    
    return {
        "character_id": character_id,
        "depth": depth,
        "network": network
    }
```

#### Day 6-7: Cross-Book Analysis
```python
# backend/app/api/v1/endpoints/analysis.py
@router.get("/cross-references")
async def get_cross_references(
    entity_type: str = Query(..., regex="^(character|magic_system|organization)$"),
    db: Session = Depends(get_db)
):
    """Find entities that appear across multiple books/worlds"""
    repo = AnalysisRepository(db)
    cross_refs = repo.get_cross_references(entity_type)
    
    return {
        "entity_type": entity_type,
        "cross_references": cross_refs
    }

@router.get("/timeline")
async def get_cosmere_timeline(
    world_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get chronological timeline of events"""
    repo = AnalysisRepository(db)
    timeline = repo.get_timeline(world_id)
    
    return {
        "world_id": world_id,
        "timeline": timeline
    }
```

**Week 8 Deliverables:**
- [x] Complete relationship system
- [x] Network analysis endpoints
- [x] Cross-reference tracking
- [x] Timeline generation
- [x] Performance optimizations applied

## Phase 3: Frontend Development (Weeks 9-12)

### Week 9: React Application Setup

#### Day 1-2: Project Initialization
```bash
# Create React app with TypeScript
npx create-react-app cosmere-frontend --template typescript
cd cosmere-frontend

# Install additional dependencies
npm install @tanstack/react-query axios react-router-dom
npm install -D tailwindcss postcss autoprefixer @types/node
npm install @headlessui/react @heroicons/react
npm install recharts d3 @types/d3  # For data visualizations

# Initialize Tailwind
npx tailwindcss init -p
```

#### Day 3-4: Project Structure & Configuration
```typescript
// src/types/cosmere.ts
export interface Character {
  id: string;
  name: string;
  aliases: string[];
  world_of_origin: World;
  species?: string;
  magic_abilities: Record<string, any>;
  status: 'alive' | 'dead' | 'cognitive_shadow' | 'unknown';
  biography?: string;
  created_at: string;
}

export interface World {
  id: string;
  name: string;
  system?: string;
  geography: Record<string, any>;
  technology_level?: string;
}

export interface Book {
  id: string;
  title: string;
  series: Series;
  world: World;
  publication_date: string;
  chronological_order: number;
  summary?: string;
}

export interface SearchResult<T> {
  items: T[];
  total: number;
  query: string;
  took: number;
}
```

#### Day 5-7: API Service Layer
```typescript
// src/services/api.ts
import axios from 'axios';
import { Character, World, Book, SearchResult } from '../types/cosmere';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5240/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export class CosmereAPI {
  // Characters
  static async getCharacters(params?: {
    skip?: number;
    limit?: number;
    world_id?: string;
    status?: string;
    search?: string;
  }) {
    const response = await apiClient.get('/characters', { params });
    return response.data;
  }

  static async getCharacter(id: string): Promise<Character> {
    const response = await apiClient.get(`/characters/${id}`);
    return response.data;
  }

  static async getCharacterRelationships(id: string) {
    const response = await apiClient.get(`/characters/${id}/relationships`);
    return response.data;
  }

  // Search
  static async searchCharacters(query: string, filters?: Record<string, string>): Promise<SearchResult<Character>> {
    const response = await apiClient.get('/search/characters', {
      params: { q: query, ...filters }
    });
    return response.data;
  }

  static async globalSearch(query: string): Promise<SearchResult<any>> {
    const response = await apiClient.get('/search/global', {
      params: { q: query }
    });
    return response.data;
  }

  // Worlds
  static async getWorlds() {
    const response = await apiClient.get('/worlds');
    return response.data;
  }

  static async getWorld(id: string): Promise<World> {
    const response = await apiClient.get(`/worlds/${id}`);
    return response.data;
  }

  // Books
  static async getBooks(params?: { series_id?: string; world_id?: string }) {
    const response = await apiClient.get('/books', { params });
    return response.data;
  }

  static async getBook(id: string): Promise<Book> {
    const response = await apiClient.get(`/books/${id}`);
    return response.data;
  }
}
```

### Week 10: Core Components & Navigation

#### Day 1-2: Layout Components
```typescript
// src/components/layout/Header.tsx
import React from 'react';
import { Link } from 'react-router-dom';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import SearchBar from '../common/SearchBar';

const Header: React.FC = () => {
  return (
    <header className="bg-slate-900 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-blue-400">
            Cosmere API
          </Link>
          
          <nav className="hidden md:flex space-x-6">
            <Link to="/characters" className="hover:text-blue-400">Characters</Link>
            <Link to="/books" className="hover:text-blue-400">Books</Link>
            <Link to="/worlds" className="hover:text-blue-400">Worlds</Link>
            <Link to="/magic-systems" className="hover:text-blue-400">Magic</Link>
            <Link to="/timeline" className="hover:text-blue-400">Timeline</Link>
          </nav>
          
          <div className="flex-1 max-w-md mx-8">
            <SearchBar />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
```

#### Day 3-4: Search Components
```typescript
// src/components/common/SearchBar.tsx
import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { debounce } from 'lodash';

const SearchBar: React.FC = () => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();