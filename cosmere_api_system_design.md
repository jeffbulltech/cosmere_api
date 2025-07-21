# Cosmere API System Design

## Overview
A comprehensive public API system to serve detailed information about Brandon Sanderson's Cosmere universe, including books, characters, magic systems, worlds, and their interconnections.

## Technology Stack

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI (async support, automatic OpenAPI docs, excellent performance)
- **Database**: PostgreSQL (relational data with JSONB for flexible attributes)
- **ORM**: SQLAlchemy 2.0 with Alembic for migrations
- **Cache**: Redis (API response caching and rate limiting)
- **Search**: Elasticsearch (full-text search across all content)
- **Task Queue**: Celery with Redis broker (background data processing)

### Frontend
- **Framework**: React 18 with TypeScript
- **State Management**: React Query (server state) + Zustand (client state)
- **UI Library**: Tailwind CSS + Headless UI
- **Build Tool**: Vite
- **Documentation**: Interactive API explorer built with React

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Web Server**: Nginx (reverse proxy, static file serving)
- **API Gateway**: Kong or AWS API Gateway (rate limiting, authentication)
- **Monitoring**: Prometheus + Grafana
- **Logging**: Structured logging with ELK stack
- **CI/CD**: GitHub Actions
- **Deployment**: AWS ECS or DigitalOcean App Platform

## Database Schema

### Core Entities

#### Books
```sql
CREATE TABLE books (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    series_id UUID REFERENCES series(id),
    world_id UUID REFERENCES worlds(id),
    publication_date DATE,
    chronological_order INTEGER,
    word_count INTEGER,
    isbn VARCHAR(20),
    summary TEXT,
    cosmere_significance JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### Characters
```sql
CREATE TABLE characters (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    aliases TEXT[],
    world_of_origin_id UUID REFERENCES worlds(id),
    species VARCHAR(100),
    magic_abilities JSONB,
    affiliations JSONB,
    status VARCHAR(50), -- alive, dead, cognitive_shadow, etc.
    first_appearance_book_id UUID REFERENCES books(id),
    biography TEXT,
    cosmere_significance JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### Worlds
```sql
CREATE TABLE worlds (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    system VARCHAR(255),
    shard_id UUID REFERENCES shards(id),
    magic_systems JSONB,
    geography JSONB,
    culture_notes TEXT,
    technology_level VARCHAR(100),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### Magic Systems
```sql
CREATE TABLE magic_systems (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    world_id UUID REFERENCES worlds(id),
    type VARCHAR(100), -- allomancy, feruchemy, hemalurgy, etc.
    mechanics JSONB,
    limitations JSONB,
    power_source VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### Shards
```sql
CREATE TABLE shards (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    intent VARCHAR(255),
    vessel_name VARCHAR(255),
    vessel_status VARCHAR(100),
    world_location_id UUID REFERENCES worlds(id),
    splinter_info JSONB,
    description TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Relationship Tables
```sql
-- Many-to-many relationships
CREATE TABLE character_books (
    character_id UUID REFERENCES characters(id),
    book_id UUID REFERENCES books(id),
    role VARCHAR(100), -- protagonist, antagonist, supporting, etc.
    PRIMARY KEY (character_id, book_id)
);

CREATE TABLE character_relationships (
    character_id UUID REFERENCES characters(id),
    related_character_id UUID REFERENCES characters(id),
    relationship_type VARCHAR(100),
    description TEXT,
    book_context_id UUID REFERENCES books(id)
);
```

## API Design

### REST Endpoints

#### Books
```
GET    /api/v1/books                    # List all books with pagination
GET    /api/v1/books/{id}               # Get specific book
GET    /api/v1/books/series/{series_id} # Books in a series
GET    /api/v1/books/world/{world_id}   # Books set on a world
```

#### Characters
```
GET    /api/v1/characters               # List characters with filters
GET    /api/v1/characters/{id}          # Get specific character
GET    /api/v1/characters/search        # Full-text search
GET    /api/v1/characters/{id}/relationships # Character connections
GET    /api/v1/characters/{id}/appearances   # Books they appear in
```

#### Worlds
```
GET    /api/v1/worlds                   # List all worlds
GET    /api/v1/worlds/{id}              # Get specific world
GET    /api/v1/worlds/{id}/characters   # Characters from this world
GET    /api/v1/worlds/{id}/magic-systems # Magic systems on this world
```

#### Magic Systems
```
GET    /api/v1/magic-systems            # List all magic systems
GET    /api/v1/magic-systems/{id}       # Get specific magic system
GET    /api/v1/magic-systems/world/{world_id} # Magic systems by world
```

#### Cross-References
```
GET    /api/v1/connections              # Cosmere-wide connections
GET    /api/v1/timeline                 # Chronological events
GET    /api/v1/search                   # Global search across all entities
```

### Response Format
```json
{
  "data": {
    "id": "uuid",
    "type": "character",
    "attributes": {
      "name": "Kaladin",
      "world_of_origin": "Roshar",
      "magic_abilities": ["Windrunning", "Surgebinding"],
      "status": "alive"
    },
    "relationships": {
      "books": [
        {"id": "book-uuid", "role": "protagonist"}
      ],
      "connections": [
        {"character_id": "syl-uuid", "type": "spren_bond"}
      ]
    }
  },
  "meta": {
    "timestamp": "2025-07-19T10:00:00Z",
    "version": "1.0"
  }
}
```

## Backend Architecture

### Project Structure
```
cosmere-api/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── books.py
│   │   │   │   ├── characters.py
│   │   │   │   ├── worlds.py
│   │   │   │   └── magic_systems.py
│   │   │   └── api.py
│   │   └── dependencies.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── models/
│   │   ├── book.py
│   │   ├── character.py
│   │   ├── world.py
│   │   └── magic_system.py
│   ├── schemas/
│   │   ├── book.py
│   │   ├── character.py
│   │   └── responses.py
│   ├── services/
│   │   ├── search_service.py
│   │   ├── cache_service.py
│   │   └── data_service.py
│   └── main.py
├── migrations/
├── tests/
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

### Key Features

#### Caching Strategy
```python
from functools import wraps
from app.core.cache import redis_client

def cache_response(ttl: int = 3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            result = await func(*args, **kwargs)
            await redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator
```

#### Search Integration
```python
from elasticsearch import AsyncElasticsearch

class SearchService:
    def __init__(self):
        self.es = AsyncElasticsearch([{"host": "elasticsearch", "port": 9200}])
    
    async def search_characters(self, query: str, filters: dict = None):
        search_body = {
            "query": {
                "bool": {
                    "must": [
                        {"multi_match": {
                            "query": query,
                            "fields": ["name^2", "aliases", "biography"]
                        }}
                    ]
                }
            }
        }
        
        if filters:
            search_body["query"]["bool"]["filter"] = [
                {"term": {k: v}} for k, v in filters.items()
            ]
        
        return await self.es.search(index="characters", body=search_body)
```

## Frontend Architecture

### React Application Structure
```
cosmere-frontend/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── SearchBar.tsx
│   │   ├── books/
│   │   │   ├── BookList.tsx
│   │   │   ├── BookDetail.tsx
│   │   │   └── BookCard.tsx
│   │   ├── characters/
│   │   │   ├── CharacterList.tsx
│   │   │   ├── CharacterDetail.tsx
│   │   │   └── CharacterConnections.tsx
│   │   └── worlds/
│   │       ├── WorldMap.tsx
│   │       └── WorldDetail.tsx
│   ├── hooks/
│   │   ├── useCharacters.ts
│   │   ├── useBooks.ts
│   │   └── useSearch.ts
│   ├── services/
│   │   └── api.ts
│   ├── types/
│   │   └── cosmere.ts
│   └── App.tsx
└── package.json
```

### API Client
```typescript
class CosmereAPI {
  private baseURL = process.env.REACT_APP_API_URL;
  
  async getCharacter(id: string): Promise<Character> {
    const response = await fetch(`${this.baseURL}/characters/${id}`);
    return response.json();
  }
  
  async searchCharacters(query: string, filters?: SearchFilters): Promise<SearchResult<Character>> {
    const params = new URLSearchParams({ q: query, ...filters });
    const response = await fetch(`${this.baseURL}/characters/search?${params}`);
    return response.json();
  }
}
```

## Deployment Architecture

### Docker Compose (Development)
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "5240:5240"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/cosmere
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
      - elasticsearch
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: cosmere
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    
  elasticsearch:
    image: elasticsearch:8.8.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:5240/api/v1
```

### Production Considerations

#### Rate Limiting
- 1000 requests per hour for anonymous users
- 10,000 requests per hour for registered users
- Special allowances for academic/research use

#### Authentication (Optional)
- JWT tokens for user accounts
- API keys for third-party developers
- OAuth integration for user-contributed content

#### Monitoring
- API response times and error rates
- Database query performance
- Cache hit rates
- Search performance metrics

#### Data Management
- Automated backups with point-in-time recovery
- Content versioning for editorial updates
- Admin interface for content management
- Data validation and consistency checks

## Development Roadmap

### Phase 1: Core API (Months 1-2)
- Basic CRUD operations for all entities
- Database schema implementation
- Core search functionality
- Basic caching layer

### Phase 2: Advanced Features (Months 3-4)
- Complex relationship queries
- Full-text search with Elasticsearch
- Performance optimization
- Comprehensive API documentation

### Phase 3: Frontend & Polish (Months 5-6)
- React frontend application
- Interactive API documentation
- Production deployment
- Performance monitoring

### Phase 4: Community Features (Months 7+)
- User-contributed content system
- Discussion forums
- Theory tracking and verification
- Mobile application

## Content Strategy

### Data Sources
- Official books and novellas
- Word of Brandon (WoB) database
- Coppermind wiki (with attribution)
- Official artwork and maps
- Audio book annotations

### Content Maintenance
- Regular updates with new releases
- Community-driven fact checking
- Spoiler management system
- Theory vs. canon distinction

This system design provides a robust, scalable foundation for serving Cosmere information while maintaining flexibility for future expansion as the universe grows.