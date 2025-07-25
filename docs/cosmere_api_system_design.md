# Cosmere API System Design

## Overview
A comprehensive public API system to serve detailed information about Brandon Sanderson's Cosmere universe, including books, characters, magic systems, worlds, and their interconnections.

## Current Implementation Status

### ✅ Completed Features
- **Backend API**: FastAPI-based REST API with PostgreSQL database (✅ FULLY WORKING)
- **Core Models**: Books, Characters, Worlds, Magic Systems, Series, Shards, Character Relationships
- **Complete CRUD Operations**: List, get, create, update, delete for all entities (✅ FULLY WORKING)
- **Database Schema**: Complete relational schema with proper foreign keys and relationships (✅ FIXED)
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation (✅ WORKING)
- **CORS Support**: Configured for frontend integration
- **Modern Frontend**: React application with modern UI components and responsive design (✅ FULLY WORKING)
- **Search Endpoints**: Basic search functionality across entities
- **Character Relationships**: Full relationship system with network analysis
- **Data Seeding**: Scripts to populate database with Cosmere data
- **Caching**: Redis caching service implemented and working
- **Search Integration**: Elasticsearch service implemented with fallback mechanisms
- **SQLAlchemy Relationships**: Fixed ambiguous foreign key relationships between shards and worlds (✅ RESOLVED)
- **Frontend Entry Point**: Fixed missing index.js file issue (✅ RESOLVED)

### 🔄 In Progress
- **Advanced Features**: Character relationships visualization, world maps, etc.

### ❌ Not Yet Implemented
- **Authentication & Authorization**: No user management system
- **Rate Limiting**: Configuration exists but not implemented
- **File Upload**: Upload system configured but not implemented
- **Monitoring**: Metrics and logging infrastructure
- **Production Deployment**: Docker and deployment configuration
- **Testing**: Comprehensive test suite

## Technology Stack

### Backend (Implemented)
- **Language**: Python 3.9+
- **Framework**: FastAPI (async support, automatic OpenAPI docs)
- **Database**: PostgreSQL (relational data with proper relationships)
- **ORM**: SQLAlchemy 2.0 with Alembic for migrations
- **Validation**: Pydantic for data validation and serialization
- **Configuration**: Pydantic Settings for environment management

### Frontend (Modern Implementation)
- **Framework**: React 18 with TypeScript
- **Build Tool**: Create React App with TypeScript
- **Routing**: React Router DOM
- **State Management**: React Query for server state, useState for local state
- **Styling**: Tailwind CSS with custom design system
- **UI Components**: Modern, reusable component library (Card, Button, Badge, Input, etc.)
- **Icons**: Heroicons for consistent iconography
- **Responsive Design**: Mobile-first responsive layout
- **Animations**: Smooth transitions and hover effects

### Infrastructure (Planned)
- **Cache**: Redis (service implemented, not actively used)
- **Search**: Elasticsearch (service implemented, not fully integrated)
- **Containerization**: Docker (files exist but not configured)
- **Monitoring**: Prometheus + Grafana (planned)
- **CI/CD**: GitHub Actions (planned)

## Database Schema (Current Implementation)

### Core Entities (Implemented)

#### Books
```sql
CREATE TABLE books (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    series_id VARCHAR(36) REFERENCES series(id),
    world_id VARCHAR(36) REFERENCES worlds(id),
    publication_date DATE,
    chronological_order INTEGER,
    word_count INTEGER,
    isbn VARCHAR(20),
    summary TEXT,
    cosmere_significance TEXT, -- JSON string
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### Characters
```sql
CREATE TABLE characters (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    aliases TEXT, -- JSON string
    world_of_origin_id VARCHAR(36) REFERENCES worlds(id),
    species VARCHAR(100),
    magic_abilities TEXT, -- JSON string
    affiliations TEXT, -- JSON string
    status VARCHAR(50),
    first_appearance_book_id VARCHAR(36) REFERENCES books(id),
    biography TEXT,
    cosmere_significance TEXT, -- JSON string
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### Worlds
```sql
CREATE TABLE worlds (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    system VARCHAR(255),
    shard_id VARCHAR(36) REFERENCES shards(id),
    magic_systems TEXT, -- JSON string
    geography TEXT, -- JSON string
    culture_notes TEXT,
    technology_level VARCHAR(100),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### Magic Systems
```sql
CREATE TABLE magic_systems (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    world_id VARCHAR(36) REFERENCES worlds(id),
    type VARCHAR(100),
    mechanics TEXT, -- JSON string
    limitations TEXT, -- JSON string
    power_source VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### Character Relationships
```sql
CREATE TABLE character_relationships (
    id VARCHAR(36) PRIMARY KEY,
    character_id VARCHAR(36) REFERENCES characters(id),
    related_character_id VARCHAR(36) REFERENCES characters(id),
    relationship_type VARCHAR(100),
    description TEXT,
    book_context_id VARCHAR(36) REFERENCES books(id),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Key Differences from Original Design
1. **UUID vs String IDs**: Using VARCHAR(36) instead of UUID type for better compatibility
2. **JSON Storage**: Using TEXT fields for JSON data instead of JSONB (PostgreSQL-specific)
3. **Simplified Relationships**: Direct foreign keys instead of complex many-to-many tables
4. **Character Relationships**: Implemented as separate table with explicit relationship types

## API Design (Current Implementation)

### Implemented Endpoints

#### Books
```
GET    /api/v1/books/                    # List all books with pagination
GET    /api/v1/books/{id}                # Get specific book
POST   /api/v1/books/                    # Create new book
PUT    /api/v1/books/{id}                # Update book
DELETE /api/v1/books/{id}                # Delete book
```

#### Characters
```
GET    /api/v1/characters/               # List characters with filters
GET    /api/v1/characters/{id}           # Get specific character
POST   /api/v1/characters/               # Create new character
PUT    /api/v1/characters/{id}           # Update character
DELETE /api/v1/characters/{id}           # Delete character
```

#### Worlds
```
GET    /api/v1/worlds/                   # List all worlds
GET    /api/v1/worlds/{id}               # Get specific world
POST   /api/v1/worlds/                   # Create new world
PUT    /api/v1/worlds/{id}               # Update world
DELETE /api/v1/worlds/{id}               # Delete world
```

#### Magic Systems
```
GET    /api/v1/magic-systems/            # List all magic systems
GET    /api/v1/magic-systems/{id}        # Get specific magic system
POST   /api/v1/magic-systems/            # Create new magic system
PUT    /api/v1/magic-systems/{id}        # Update magic system
DELETE /api/v1/magic-systems/{id}        # Delete magic system
```

#### Character Relationships
```
GET    /api/v1/character-relationships/  # List relationships
GET    /api/v1/character-relationships/{id} # Get specific relationship
POST   /api/v1/character-relationships/  # Create relationship
PUT    /api/v1/character-relationships/{id} # Update relationship
DELETE /api/v1/character-relationships/{id} # Delete relationship
```

#### Search
```
GET    /api/v1/search/characters         # Search characters
GET    /api/v1/search/global             # Global search across all entities
```

### Response Format (Current)
```json
{
  "items": [
    {
      "id": "uuid-string",
      "name": "Character Name",
      "world_of_origin_id": "world-uuid",
      "species": "Human",
      "status": "alive",
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-01-01T00:00:00Z"
    }
  ],
  "total": 100,
  "skip": 0,
  "limit": 20,
  "has_next": true,
  "has_prev": false
}
```

### Key Differences from Original Design
1. **Simplified Response Format**: Direct object arrays instead of JSON:API format
2. **Pagination**: Standard offset/limit pagination instead of cursor-based
3. **No Relationships in Response**: Related data not automatically included
4. **Basic Filtering**: Query parameters for basic filtering instead of complex query language

## Backend Architecture (Current Implementation)

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
│   │   │   │   ├── magic_systems.py
│   │   │   │   ├── character_relationships.py
│   │   │   │   ├── series.py
│   │   │   │   ├── shards.py
│   │   │   │   └── search.py
│   │   │   └── api.py
│   │   └── dependencies.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   │   ├── base.py
│   │   ├── book.py
│   │   ├── character.py
│   │   ├── world.py
│   │   ├── magic_system.py
│   │   ├── character_relationship.py
│   │   ├── series.py
│   │   └── shards.py
│   ├── schemas/
│   │   ├── base.py
│   │   ├── book.py
│   │   ├── character.py
│   │   ├── world.py
│   │   └── magic_system.py
│   ├── services/
│   │   ├── cache_service.py
│   │   └── search_service.py
│   └── main.py
├── migrations/
├── tests/
└── requirements.txt
```

### Key Features (Implemented)

#### Basic CRUD Operations
- All entities have complete CRUD operations
- Proper error handling with HTTP status codes
- Input validation using Pydantic schemas
- Database transaction management

#### Search Functionality
- Basic text search across entity names
- Filtering by various attributes
- Pagination support
- Elasticsearch service implemented but not fully integrated

#### Data Validation
- Pydantic schemas for request/response validation
- Type checking and data transformation
- Error messages for validation failures

### Key Features (Planned)

#### Caching Strategy
```python
# Implemented but not actively used
from app.services.cache_service import cache_response

@cache_response(ttl=3600)
def get_characters(skip: int = 0, limit: int = 20):
    # Implementation
    pass
```

#### Search Integration
```python
# Service implemented but not fully integrated
from app.services.search_service import SearchService

async def search_characters(query: str, filters: dict = None):
    search_service = SearchService()
    return await search_service.search_characters(query, filters)
```

## Frontend Architecture (Current Implementation)

### React Application Structure
```
cosmere-frontend/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.tsx (empty)
│   │   │   ├── Footer.tsx (empty)
│   │   │   ├── SearchBar.tsx (empty)
│   │   │   ├── LoadingSpinner.tsx (empty)
│   │   │   └── ErrorBoundary.tsx (empty)
│   │   ├── books/
│   │   │   ├── BookList.tsx (empty)
│   │   │   ├── BookDetail.tsx (empty)
│   │   │   └── BookCard.tsx (empty)
│   │   ├── characters/
│   │   │   ├── CharacterList.tsx (empty)
│   │   │   ├── CharacterDetail.tsx (empty)
│   │   │   ├── CharacterCard.tsx (empty)
│   │   │   ├── CharacterSearch.tsx (empty)
│   │   │   └── CharacterConnections.tsx (empty)
│   │   └── worlds/
│   │       ├── WorldList.tsx (empty)
│   │       ├── WorldDetail.tsx (empty)
│   │       └── WorldCard.tsx (empty)
│   ├── pages/
│   │   ├── Books.tsx (basic implementation)
│   │   ├── Characters.tsx (basic implementation)
│   │   ├── Worlds.tsx (basic implementation)
│   │   └── MagicSystems.tsx (basic implementation)
│   ├── services/
│   │   └── api.ts (basic implementation)
│   ├── types/
│   │   └── cosmere.ts (not implemented)
│   └── App.tsx (basic routing)
└── package.json
```

### Current Implementation Status
- **Basic Routing**: React Router configured with main pages
- **API Integration**: Basic fetch calls to backend endpoints
- **Data Display**: Simple list views for all entities
- **No Styling**: Basic HTML structure without CSS framework
- **No State Management**: Using basic React hooks
- **No Error Handling**: Basic error states
- **No Loading States**: Basic loading indicators

### API Client (Current)
```typescript
// Basic implementation
const API_BASE = '/api/v1';

export async function fetchCharacters() {
  const res = await fetch(`${API_BASE}/characters/`);
  if (!res.ok) throw new Error('Failed to fetch characters');
  const data = await res.json();
  return data.items || data;
}
```

## Deployment Architecture (Planned)

### Development Environment
- **Database**: PostgreSQL running locally
- **Backend**: FastAPI server on port 5240
- **Frontend**: Vite dev server on port 5173
- **No Containerization**: Running directly on host

### Production Considerations (Planned)

#### Rate Limiting
- Configuration exists but not implemented
- Planned: 1000 requests per hour for anonymous users
- Planned: 10,000 requests per hour for registered users

#### Authentication (Planned)
- No authentication system implemented
- Planned: JWT tokens for user accounts
- Planned: API keys for third-party developers

#### Monitoring (Planned)
- Basic logging implemented
- Planned: API response times and error rates
- Planned: Database query performance
- Planned: Cache hit rates

#### Data Management (Implemented)
- Database migrations with Alembic
- Data seeding scripts
- Basic backup strategy

## Development Roadmap (Updated)

### Phase 1: Core API ✅ COMPLETED (Months 1-2)
- ✅ Basic CRUD operations for all entities
- ✅ Database schema implementation
- ✅ Core search functionality
- ✅ Basic caching layer (implemented but not used)

### Phase 2: Advanced Features 🔄 IN PROGRESS (Months 3-4)
- 🔄 Complex relationship queries (partially implemented)
- 🔄 Full-text search with Elasticsearch (service implemented)
- ❌ Performance optimization
- ✅ Comprehensive API documentation

### Phase 3: Frontend & Polish ❌ NOT STARTED (Months 5-6)
- ❌ React frontend application (basic structure only)
- ❌ Interactive API documentation
- ❌ Production deployment
- ❌ Performance monitoring

### Phase 4: Community Features ❌ NOT STARTED (Months 7+)
- ❌ User-contributed content system
- ❌ Discussion forums
- ❌ Theory tracking and verification
- ❌ Mobile application

## Content Strategy (Implemented)

### Data Sources (Implemented)
- ✅ Database populated with Cosmere data
- ✅ Character relationships established
- ✅ World and magic system information
- ✅ Book and series data

### Content Maintenance (Planned)
- ❌ Regular updates with new releases
- ❌ Community-driven fact checking
- ❌ Spoiler management system
- ❌ Theory vs. canon distinction

## Current Issues and Technical Debt

### Backend Issues
1. **Data Validation**: ✅ RESOLVED - Pydantic validation working correctly, foreign key constraints properly enforced
2. **JSON Storage**: Using TEXT fields instead of JSONB for better PostgreSQL integration
3. **Caching**: ✅ RESOLVED - Redis caching actively used across all API endpoints with proper invalidation
4. **Search**: ✅ RESOLVED - Elasticsearch fully integrated with API endpoints and fallback mechanisms
5. **Error Handling**: Basic error handling, needs more comprehensive approach

### Frontend Issues
1. **Empty Components**: ✅ RESOLVED - All components implemented with full functionality
2. **No Styling**: ✅ RESOLVED - Tailwind CSS implemented with responsive design
3. **Basic State Management**: Using React hooks effectively, no advanced state management needed yet
4. **No Error Boundaries**: ✅ RESOLVED - ErrorBoundary component implemented
5. **No Loading States**: ✅ RESOLVED - LoadingSpinner component and loading states implemented

### Infrastructure Issues
1. **No Containerization**: No Docker setup for easy deployment
2. **No Testing**: No automated tests implemented
3. **No CI/CD**: No continuous integration pipeline
4. **No Monitoring**: No production monitoring or alerting

## Next Steps

### ✅ Recently Completed (Step 1)
**Fixed Data Validation Issues and Added Missing CRUD Operations**
- ✅ Added POST, PUT, DELETE operations to characters endpoint
- ✅ Added POST, PUT, DELETE operations to magic_systems endpoint
- ✅ Implemented proper JSON serialization/deserialization for database storage
- ✅ Added comprehensive error handling for foreign key constraints
- ✅ Verified all CRUD operations work correctly with proper validation
- ✅ Tested error handling for non-existent records (404 responses)

### ✅ Recently Completed (Step 2)
**Implemented Frontend Components and Added Styling**
- ✅ Created comprehensive TypeScript types for all Cosmere entities
- ✅ Enhanced API service with full CRUD operations and proper typing
- ✅ Built reusable common components (Header, Footer, LoadingSpinner, ErrorBoundary, SearchBar)
- ✅ Implemented entity-specific components (CharacterCard, BookCard, WorldCard, MagicSystemCard)
- ✅ Created list components with filtering, search, and pagination
- ✅ Added responsive grid layouts and modern UI design
- ✅ Integrated Tailwind CSS for consistent styling
- ✅ Added error handling and loading states throughout the application
- ✅ Implemented search functionality with debouncing and suggestions
- ✅ Created empty states and proper user feedback

### ✅ Recently Completed (Step 6)
**Implement Detail Pages for All Entities**
- ✅ Created comprehensive CharacterDetail page with full character information display
- ✅ Created comprehensive BookDetail page with book information and related data
- ✅ Created comprehensive WorldDetail page with world information and magic systems
- ✅ Created comprehensive MagicSystemDetail page with mechanics and limitations
- ✅ Created comprehensive SeriesDetail page with series information and related books
- ✅ Created comprehensive ShardDetail page with shard information and vessel details
- ✅ Added proper routing for all detail pages in App.tsx
- ✅ Implemented consistent UI design with responsive layouts
- ✅ Added edit and delete functionality with confirmation modals
- ✅ Included quick action links to related entities
- ✅ Added proper error handling and loading states
- ✅ Ensured all card components link to their respective detail pages

### ✅ Recently Completed (Step 4)
**Complete Search Integration with Elasticsearch**
- ✅ Enhanced SearchService with comprehensive Elasticsearch operations
- ✅ Created IndexingService for database-to-Elasticsearch synchronization
- ✅ Implemented robust fallback mechanisms for when Elasticsearch is unavailable
- ✅ Added Elasticsearch management endpoints (health, indices, indexing, stats)
- ✅ Enhanced search endpoints with Elasticsearch queries and fuzzy matching
- ✅ Added search suggestions endpoint with autocomplete functionality
- ✅ Implemented proper document indexing and deletion for all entity types
- ✅ Fixed Shard model relationship issues for proper data retrieval
- ✅ Added comprehensive error handling and logging for search operations
- ✅ Ensured API remains functional even without Elasticsearch running

### ✅ Recently Completed (Step 3)
**Integrated Redis Caching Across All API Endpoints**
- ✅ Added caching decorators to all remaining endpoints (series, shards, search, character_relationships)
- ✅ Implemented cache invalidation for all CRUD operations (POST, PUT, DELETE)
- ✅ Enhanced cache management endpoints to include all entity types
- ✅ Fixed SQLAlchemy relationship issues in Shard model for proper caching
- ✅ Verified caching functionality with comprehensive testing
- ✅ Implemented proper TTL strategies (30 minutes for lists, 1 hour for details, 15 minutes for search)
- ✅ Added cache status monitoring and debugging endpoints
- ✅ Ensured cache consistency across all entity types

### Immediate Priorities (Next 2-4 weeks)
1. **Fix Data Validation Issues**: ✅ COMPLETED - Resolved Pydantic validation errors and added missing CRUD operations
2. **Implement Frontend Components**: ✅ COMPLETED - Built out all component files with modern UI and functionality
3. **Add Styling**: ✅ COMPLETED - Implemented Tailwind CSS with responsive design
4. **Integrate Caching**: ✅ COMPLETED - Actively use Redis caching in API endpoints
5. **Complete Search Integration**: ✅ COMPLETED - Fully integrated Elasticsearch with API and fallback mechanisms
6. **Implement Detail Pages**: ✅ COMPLETED - Created comprehensive detail pages for all entities

### Medium-term Goals (Next 2-3 months)
1. **Add Authentication**: Implement user management system
2. **Implement Rate Limiting**: Add proper rate limiting middleware
3. **Add Testing**: Comprehensive test suite for backend and frontend
4. **Production Deployment**: Docker setup and deployment configuration
5. **Performance Optimization**: Database query optimization and caching strategies

### Long-term Goals (Next 6+ months)
1. **Community Features**: User-contributed content and discussion forums
2. **Mobile Application**: React Native or similar mobile app
3. **Advanced Analytics**: Usage analytics and content insights
4. **API Versioning**: Proper API versioning strategy
5. **Internationalization**: Multi-language support

## System Status Summary (Latest Update)

### ✅ Current System Status: FULLY OPERATIONAL
**Both backend API and frontend are now fully functional and stable.**

#### Backend API (✅ WORKING)
- **Server**: Running on http://localhost:8000
- **API Documentation**: Available at http://localhost:8000/docs
- **All Endpoints**: Shards, Characters, Worlds, Books, Series, Magic Systems, Search, Cache Management
- **Database**: PostgreSQL with proper relationships and data
- **Caching**: Redis integration working
- **Search**: Elasticsearch integration with fallback mechanisms

#### Frontend (✅ WORKING)
- **Application**: Running on http://localhost:3000
- **Framework**: React with TypeScript and Tailwind CSS
- **Components**: All pages and components fully implemented
- **Responsive Design**: Mobile-first responsive layout
- **API Integration**: Properly connected to backend API

#### Recent Fixes Applied
1. **SQLAlchemy Relationship Issues**: ✅ RESOLVED - Fixed ambiguous foreign key relationships between shards and worlds tables
2. **Frontend Entry Point**: ✅ RESOLVED - Fixed missing index.js file issue for Create React App
3. **API Schema Validation**: ✅ RESOLVED - Removed deprecated world_location_id references from shard schemas
4. **Database Schema**: ✅ CLEAN - Verified no conflicting columns in database tables

#### System Health
- **Backend**: All API endpoints responding correctly
- **Frontend**: All pages loading and functioning properly
- **Database**: All relationships working without ambiguity
- **Documentation**: OpenAPI docs generating correctly

The Cosmere API system is now in a fully operational state with both backend and frontend working seamlessly together. All major issues have been resolved and the system is ready for development and testing.