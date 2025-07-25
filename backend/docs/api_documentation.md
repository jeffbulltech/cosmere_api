# Cosmere API Documentation

## Overview

The Cosmere API provides comprehensive access to data about Brandon Sanderson's Cosmere universe, including worlds, books, characters, series, magic systems, and shards. This RESTful API is built with FastAPI and provides extensive search and filtering capabilities.

## Base URL

```
https://api.cosmere.com/api/v1
```

## Authentication

Currently, the API is open and does not require authentication. Future versions may implement API key authentication.

## Response Format

All API responses follow a consistent JSON format:

### Success Response
```json
{
  "items": [...],
  "total": 100,
  "skip": 0,
  "limit": 20,
  "page": 1,
  "pages": 5
}
```

### Error Response
```json
{
  "error": "Resource not found",
  "detail": "The requested world was not found",
  "status_code": 404
}
```

## Endpoints

### Worlds

#### Get All Worlds
```http
GET /worlds/
```

**Query Parameters:**
- `skip` (integer): Number of records to skip (default: 0)
- `limit` (integer): Number of records to return (default: 20, max: 100)
- `name` (string): Filter by world name
- `system` (string): Filter by planetary system
- `is_habitable` (boolean): Filter by habitable status

**Example:**
```bash
curl -X GET "https://api.cosmere.com/api/v1/worlds/?limit=10&is_habitable=true"
```

**Response:**
```json
{
  "items": [
    {
      "id": "roshar",
      "name": "Roshar",
      "description": "A world of stone and storms",
      "system": "Rosharan System",
      "is_habitable": true,
      "magic_systems_description": "Surgebinding and Voidbinding",
      "notable_features": "Highstorms, spren, and the Shattered Plains",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 10,
  "page": 1,
  "pages": 1
}
```

#### Get World by ID
```http
GET /worlds/{world_id}
```

**Example:**
```bash
curl -X GET "https://api.cosmere.com/api/v1/worlds/roshar"
```

#### Get Worlds Overview
```http
GET /worlds/overview
```

**Response:**
```json
{
  "total_worlds": 10,
  "habitable_worlds": 8,
  "worlds_with_series": 7,
  "worlds_with_magic_systems": 9,
  "worlds": [...]
}
```

#### Search Worlds
```http
GET /worlds/search?q={search_term}
```

**Example:**
```bash
curl -X GET "https://api.cosmere.com/api/v1/worlds/search?q=Roshar"
```

#### Create World
```http
POST /worlds/
```

**Request Body:**
```json
{
  "id": "scadrial",
  "name": "Scadrial",
  "description": "A world of ash and mist",
  "system": "Scadrian System",
  "is_habitable": true,
  "magic_systems_description": "Allomancy and Feruchemy",
  "notable_features": "Ashfalls, mist, and the Final Empire"
}
```

#### Update World
```http
PUT /worlds/{world_id}
```

#### Delete World
```http
DELETE /worlds/{world_id}
```

### Books

#### Get All Books
```http
GET /books/
```

**Query Parameters:**
- `skip` (integer): Number of records to skip
- `limit` (integer): Number of records to return
- `title` (string): Filter by book title
- `series_id` (string): Filter by series
- `world_id` (string): Filter by world
- `is_standalone` (boolean): Filter by standalone status

#### Get Book by ID
```http
GET /books/{book_id}
```

#### Get Books by Series
```http
GET /books/series/{series_id}
```

#### Get Standalone Books
```http
GET /books/standalone
```

#### Get Reading Order
```http
GET /books/reading-order/{series_id}
```

#### Search Books
```http
GET /books/search?q={search_term}
```

#### Create Book
```http
POST /books/
```

**Request Body:**
```json
{
  "id": "way-of-kings",
  "title": "The Way of Kings",
  "series_id": "stormlight-archive",
  "world_id": "roshar",
  "publication_date": "2010-08-31",
  "summary": "The first book in The Stormlight Archive",
  "page_count": 1007,
  "is_standalone": false,
  "reading_order": 1
}
```

### Characters

#### Get All Characters
```http
GET /characters/
```

**Query Parameters:**
- `skip` (integer): Number of records to skip
- `limit` (integer): Number of records to return
- `name` (string): Filter by character name
- `species` (string): Filter by species
- `status` (string): Filter by character status
- `world_id` (string): Filter by world of origin

#### Get Character by ID
```http
GET /characters/{character_id}
```

#### Get Characters by World
```http
GET /characters/world/{world_id}
```

#### Get Characters by Species
```http
GET /characters/species/{species}
```

#### Get Characters by Status
```http
GET /characters/status/{status}
```

#### Get POV Characters
```http
GET /characters/pov
```

#### Get Character with Relationships
```http
GET /characters/{character_id}/relationships
```

#### Search Characters
```http
GET /characters/search?q={search_term}
```

#### Create Character
```http
POST /characters/
```

**Request Body:**
```json
{
  "id": "kaladin-stormblessed",
  "name": "Kaladin Stormblessed",
  "aliases": ["Kal", "Stormblessed"],
  "world_of_origin_id": "roshar",
  "species": "Human",
  "status": "alive",
  "biography": "A former slave who becomes a Windrunner",
  "appearance": "Dark hair, dark eyes, athletic build",
  "personality": "Honorable, protective, brooding",
  "abilities": "Surgebinding (Windrunner), Shardblade, Shardplate"
}
```

### Series

#### Get All Series
```http
GET /series/
```

**Query Parameters:**
- `skip` (integer): Number of records to skip
- `limit` (integer): Number of records to return
- `name` (string): Filter by series name
- `status` (string): Filter by series status
- `world_id` (string): Filter by world

#### Get Series by ID
```http
GET /series/{series_id}
```

#### Get Ongoing Series
```http
GET /series/ongoing
```

#### Get Completed Series
```http
GET /series/completed
```

#### Get Series by World
```http
GET /series/world/{world_id}
```

#### Get Series Summary
```http
GET /series/{series_id}/summary
```

#### Search Series
```http
GET /series/search?q={search_term}
```

#### Create Series
```http
POST /series/
```

**Request Body:**
```json
{
  "id": "stormlight-archive",
  "name": "The Stormlight Archive",
  "description": "Epic fantasy series on Roshar",
  "world_id": "roshar",
  "planned_books": 10,
  "current_books": 4,
  "status": "ongoing",
  "reading_order": "Primary series"
}
```

### Magic Systems

#### Get All Magic Systems
```http
GET /magic-systems/
```

**Query Parameters:**
- `skip` (integer): Number of records to skip
- `limit` (integer): Number of records to return
- `name` (string): Filter by magic system name
- `world_id` (string): Filter by world
- `is_investiture_based` (boolean): Filter by investiture-based status

#### Get Magic System by ID
```http
GET /magic-systems/{magic_system_id}
```

#### Get Investiture-Based Magic Systems
```http
GET /magic-systems/investiture-based
```

#### Get Magic Systems by World
```http
GET /magic-systems/world/{world_id}
```

#### Get Magic System with Users
```http
GET /magic-systems/{magic_system_id}/users
```

#### Search Magic Systems
```http
GET /magic-systems/search?q={search_term}
```

#### Create Magic System
```http
POST /magic-systems/
```

**Request Body:**
```json
{
  "id": "surgebinding",
  "name": "Surgebinding",
  "world_id": "roshar",
  "description": "Magic system based on the Ten Surges",
  "mechanics": "Uses Stormlight to power abilities",
  "requirements": "Bond with a spren",
  "limitations": "Requires Stormlight to function",
  "is_investiture_based": true,
  "related_systems": "Voidbinding, Old Magic"
}
```

### Shards

#### Get All Shards
```http
GET /shards/
```

**Query Parameters:**
- `skip` (integer): Number of records to skip
- `limit` (integer): Number of records to return
- `name` (string): Filter by shard name
- `intent` (string): Filter by shard intent
- `status` (string): Filter by shard status
- `is_combined` (boolean): Filter by combined status

#### Get Shard by ID
```http
GET /shards/{shard_id}
```

#### Get Whole Shards
```http
GET /shards/whole
```

#### Get Splintered Shards
```http
GET /shards/splintered
```

#### Get Combined Shards
```http
GET /shards/combined
```

#### Get Shards by Intent
```http
GET /shards/intent/{intent}
```

#### Get Shard with Vessels
```http
GET /shards/{shard_id}/vessels
```

#### Search Shards
```http
GET /shards/search?q={search_term}
```

#### Create Shard
```http
POST /shards/
```

**Request Body:**
```json
{
  "id": "honor",
  "name": "Honor",
  "intent": "Honor",
  "status": "splintered",
  "current_vessel": "None",
  "original_vessel": "Tanavast",
  "description": "The Shard of Honor",
  "perpendicularity": "Stormfather",
  "magic_systems": "Surgebinding",
  "residence": "Roshar",
  "is_combined": false
}
```

### Search

#### Search All Entities
```http
GET /search/?q={search_term}
```

**Query Parameters:**
- `q` (string): Search term (required)
- `limit_per_type` (integer): Maximum results per entity type (default: 10)

**Example:**
```bash
curl -X GET "https://api.cosmere.com/api/v1/search/?q=Kaladin&limit_per_type=5"
```

**Response:**
```json
{
  "worlds": [...],
  "series": [...],
  "books": [...],
  "characters": [...],
  "magic_systems": [...],
  "shards": [...],
  "total_results": 15,
  "search_term": "Kaladin"
}
```

#### Search by Entity Type
```http
GET /search/{entity_type}?q={search_term}
```

**Example:**
```bash
curl -X GET "https://api.cosmere.com/api/v1/search/characters?q=Kaladin"
```

#### Get Search Suggestions
```http
GET /search/suggestions?q={search_term}
```

**Example:**
```bash
curl -X GET "https://api.cosmere.com/api/v1/search/suggestions?q=Kal"
```

**Response:**
```json
{
  "suggestions": ["Kaladin Stormblessed", "Kal", "Kaladin"],
  "search_term": "Kal"
}
```

#### Advanced Search
```http
POST /search/advanced
```

**Request Body:**
```json
{
  "search_term": "Kaladin",
  "entity_types": ["characters", "books"],
  "filters": {
    "world_id": "roshar",
    "status": "alive"
  },
  "limit": 20
}
```

### Health

#### Basic Health Check
```http
GET /health/
```

**Response:**
```json
{
  "status": "healthy",
  "service": "cosmere-api",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

#### Database Health Check
```http
GET /health/db
```

#### Detailed Health Check
```http
GET /health/detailed
```

**Response:**
```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "service": "cosmere-api",
  "version": "1.0.0",
  "status": "healthy",
  "checks": {
    "database": {
      "status": "healthy",
      "message": "Database connection is working"
    },
    "api": {
      "status": "healthy",
      "message": "API is responding"
    }
  }
}
```

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Validation Error |
| 500 | Internal Server Error |

## Rate Limiting

Currently, there are no rate limits implemented. Future versions may include rate limiting based on API keys.

## Pagination

All list endpoints support pagination with the following parameters:

- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 20, max: 100)

The response includes pagination metadata:

```json
{
  "items": [...],
  "total": 100,
  "skip": 0,
  "limit": 20,
  "page": 1,
  "pages": 5
}
```

## Filtering

Most endpoints support filtering via query parameters. The available filters depend on the entity type:

### Common Filters
- `name` / `title`: Filter by name or title
- `world_id`: Filter by world
- `skip` / `limit`: Pagination

### Entity-Specific Filters
- **Worlds**: `system`, `is_habitable`
- **Books**: `series_id`, `is_standalone`
- **Characters**: `species`, `status`
- **Series**: `status`
- **Magic Systems**: `is_investiture_based`
- **Shards**: `intent`, `status`, `is_combined`

## Search

The API provides comprehensive search functionality:

### Basic Search
Search across all entities or specific entity types using the `q` parameter.

### Advanced Search
Use the advanced search endpoint for complex queries with multiple filters.

### Search Suggestions
Get autocomplete suggestions for search terms.

## Data Models

### World
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "system": "string",
  "is_habitable": "boolean",
  "magic_systems_description": "string",
  "notable_features": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Book
```json
{
  "id": "string",
  "title": "string",
  "series_id": "string",
  "world_id": "string",
  "publication_date": "date",
  "summary": "string",
  "page_count": "integer",
  "is_standalone": "boolean",
  "reading_order": "integer",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Character
```json
{
  "id": "string",
  "name": "string",
  "aliases": ["string"],
  "world_of_origin_id": "string",
  "species": "string",
  "status": "string",
  "biography": "string",
  "appearance": "string",
  "personality": "string",
  "abilities": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Series
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "world_id": "string",
  "planned_books": "integer",
  "current_books": "integer",
  "status": "string",
  "reading_order": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Magic System
```json
{
  "id": "string",
  "name": "string",
  "world_id": "string",
  "description": "string",
  "mechanics": "string",
  "requirements": "string",
  "limitations": "string",
  "is_investiture_based": "boolean",
  "related_systems": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Shard
```json
{
  "id": "string",
  "name": "string",
  "intent": "string",
  "status": "string",
  "current_vessel": "string",
  "original_vessel": "string",
  "description": "string",
  "perpendicularity": "string",
  "magic_systems": "string",
  "residence": "string",
  "is_combined": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Examples

### Getting All Characters from Roshar
```bash
curl -X GET "https://api.cosmere.com/api/v1/characters/?world_id=roshar&limit=50"
```

### Searching for Books About Kaladin
```bash
curl -X GET "https://api.cosmere.com/api/v1/books/search?q=Kaladin"
```

### Getting Magic Systems by World
```bash
curl -X GET "https://api.cosmere.com/api/v1/magic-systems/world/roshar"
```

### Creating a New Character
```bash
curl -X POST "https://api.cosmere.com/api/v1/characters/" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "shallan-davar",
    "name": "Shallan Davar",
    "aliases": ["Shallan", "Veil", "Radiant"],
    "world_of_origin_id": "roshar",
    "species": "Human",
    "status": "alive",
    "biography": "A scholar and artist who becomes a Lightweaver"
  }'
```

### Advanced Search
```bash
curl -X POST "https://api.cosmere.com/api/v1/search/advanced" \
  -H "Content-Type: application/json" \
  -d '{
    "search_term": "Stormlight",
    "entity_types": ["books", "magic_systems"],
    "filters": {
      "world_id": "roshar"
    }
  }'
```

## SDKs and Libraries

### Python
```python
import requests

# Get all worlds
response = requests.get("https://api.cosmere.com/api/v1/worlds/")
worlds = response.json()

# Search for characters
response = requests.get("https://api.cosmere.com/api/v1/search/characters?q=Kaladin")
characters = response.json()
```

### JavaScript
```javascript
// Get all books
const response = await fetch('https://api.cosmere.com/api/v1/books/');
const books = await response.json();

// Create a new world
const worldData = {
  id: 'scadrial',
  name: 'Scadrial',
  description: 'A world of ash and mist'
};

const createResponse = await fetch('https://api.cosmere.com/api/v1/worlds/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(worldData)
});
```

## Support

For API support, please contact:
- Email: api-support@cosmere.com
- Documentation: https://docs.cosmere.com
- GitHub Issues: https://github.com/cosmere/api/issues

## Changelog

### v1.0.0 (2024-01-01)
- Initial API release
- Complete CRUD operations for all entities
- Advanced search functionality
- Health check endpoints
- Comprehensive documentation 