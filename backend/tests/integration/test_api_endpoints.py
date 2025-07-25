"""
Integration tests for API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestWorldEndpoints:
    """Integration tests for world endpoints."""
    
    def test_get_worlds(self, client: TestClient, populated_db: dict):
        """Test getting all worlds."""
        response = client.get("/api/v1/worlds/")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "Roshar"
    
    def test_get_world_by_id(self, client: TestClient, populated_db: dict):
        """Test getting a world by ID."""
        world_id = populated_db["world"].id
        response = client.get(f"/api/v1/worlds/{world_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == world_id
        assert data["name"] == "Roshar"
    
    def test_get_world_not_found(self, client: TestClient):
        """Test getting a non-existent world."""
        response = client.get("/api/v1/worlds/non-existent")
        assert response.status_code == 404
    
    def test_create_world(self, client: TestClient):
        """Test creating a new world."""
        world_data = {
            "id": "scadrial",
            "name": "Scadrial",
            "description": "A world of ash and mist",
            "system": "Scadrian System",
            "is_habitable": True,
            "magic_systems_description": "Allomancy and Feruchemy",
            "notable_features": "Ashfalls, mist, and the Final Empire"
        }
        
        response = client.post("/api/v1/worlds/", json=world_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["id"] == "scadrial"
        assert data["name"] == "Scadrial"
    
    def test_update_world(self, client: TestClient, populated_db: dict):
        """Test updating a world."""
        world_id = populated_db["world"].id
        update_data = {"description": "Updated description"}
        
        response = client.put(f"/api/v1/worlds/{world_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["description"] == "Updated description"
    
    def test_delete_world(self, client: TestClient, populated_db: dict):
        """Test deleting a world."""
        world_id = populated_db["world"].id
        
        response = client.delete(f"/api/v1/worlds/{world_id}")
        assert response.status_code == 204
        
        # Verify world is deleted
        get_response = client.get(f"/api/v1/worlds/{world_id}")
        assert get_response.status_code == 404
    
    def test_get_worlds_overview(self, client: TestClient, populated_db: dict):
        """Test getting worlds overview."""
        response = client.get("/api/v1/worlds/overview")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_worlds" in data
        assert "habitable_worlds" in data
        assert data["total_worlds"] == 1
    
    def test_search_worlds(self, client: TestClient, populated_db: dict):
        """Test searching worlds."""
        response = client.get("/api/v1/worlds/search?q=Roshar")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Roshar"


class TestBookEndpoints:
    """Integration tests for book endpoints."""
    
    def test_get_books(self, client: TestClient, populated_db: dict):
        """Test getting all books."""
        response = client.get("/api/v1/books/")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == "The Way of Kings"
    
    def test_get_book_by_id(self, client: TestClient, populated_db: dict):
        """Test getting a book by ID."""
        book_id = populated_db["book"].id
        response = client.get(f"/api/v1/books/{book_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == book_id
        assert data["title"] == "The Way of Kings"
    
    def test_get_books_by_series(self, client: TestClient, populated_db: dict):
        """Test getting books by series."""
        series_id = populated_db["series"].id
        response = client.get(f"/api/v1/books/series/{series_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "The Way of Kings"
    
    def test_get_standalone_books(self, client: TestClient, populated_db: dict):
        """Test getting standalone books."""
        response = client.get("/api/v1/books/standalone")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 0  # No standalone books in test data
    
    def test_create_book(self, client: TestClient, populated_db: dict):
        """Test creating a new book."""
        book_data = {
            "id": "words-of-radiance",
            "title": "Words of Radiance",
            "series_id": populated_db["series"].id,
            "world_id": populated_db["world"].id,
            "publication_date": "2014-03-04",
            "summary": "The second book in The Stormlight Archive",
            "page_count": 1087,
            "is_standalone": False,
            "reading_order": 2
        }
        
        response = client.post("/api/v1/books/", json=book_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["id"] == "words-of-radiance"
        assert data["title"] == "Words of Radiance"


class TestCharacterEndpoints:
    """Integration tests for character endpoints."""
    
    def test_get_characters(self, client: TestClient, populated_db: dict):
        """Test getting all characters."""
        response = client.get("/api/v1/characters/")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "Kaladin Stormblessed"
    
    def test_get_character_by_id(self, client: TestClient, populated_db: dict):
        """Test getting a character by ID."""
        character_id = populated_db["character"].id
        response = client.get(f"/api/v1/characters/{character_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == character_id
        assert data["name"] == "Kaladin Stormblessed"
    
    def test_get_characters_by_world(self, client: TestClient, populated_db: dict):
        """Test getting characters by world."""
        world_id = populated_db["world"].id
        response = client.get(f"/api/v1/characters/world/{world_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Kaladin Stormblessed"
    
    def test_get_characters_by_species(self, client: TestClient, populated_db: dict):
        """Test getting characters by species."""
        response = client.get("/api/v1/characters/species/Human")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["species"] == "Human"
    
    def test_create_character(self, client: TestClient, populated_db: dict):
        """Test creating a new character."""
        character_data = {
            "id": "shallan-davar",
            "name": "Shallan Davar",
            "aliases": ["Shallan", "Veil", "Radiant"],
            "world_of_origin_id": populated_db["world"].id,
            "species": "Human",
            "status": "alive",
            "biography": "A scholar and artist who becomes a Lightweaver",
            "appearance": "Red hair, light eyes, petite build",
            "personality": "Intelligent, artistic, complex",
            "abilities": "Surgebinding (Lightweaver), Shardblade"
        }
        
        response = client.post("/api/v1/characters/", json=character_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["id"] == "shallan-davar"
        assert data["name"] == "Shallan Davar"


class TestSeriesEndpoints:
    """Integration tests for series endpoints."""
    
    def test_get_series(self, client: TestClient, populated_db: dict):
        """Test getting all series."""
        response = client.get("/api/v1/series/")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "The Stormlight Archive"
    
    def test_get_series_by_id(self, client: TestClient, populated_db: dict):
        """Test getting a series by ID."""
        series_id = populated_db["series"].id
        response = client.get(f"/api/v1/series/{series_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == series_id
        assert data["name"] == "The Stormlight Archive"
    
    def test_get_ongoing_series(self, client: TestClient, populated_db: dict):
        """Test getting ongoing series."""
        response = client.get("/api/v1/series/ongoing")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "ongoing"
    
    def test_get_series_by_world(self, client: TestClient, populated_db: dict):
        """Test getting series by world."""
        world_id = populated_db["world"].id
        response = client.get(f"/api/v1/series/world/{world_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["world_id"] == world_id


class TestMagicSystemEndpoints:
    """Integration tests for magic system endpoints."""
    
    def test_get_magic_systems(self, client: TestClient, populated_db: dict):
        """Test getting all magic systems."""
        response = client.get("/api/v1/magic-systems/")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "Surgebinding"
    
    def test_get_magic_system_by_id(self, client: TestClient, populated_db: dict):
        """Test getting a magic system by ID."""
        magic_system_id = populated_db["magic_system"].id
        response = client.get(f"/api/v1/magic-systems/{magic_system_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == magic_system_id
        assert data["name"] == "Surgebinding"
    
    def test_get_investiture_based(self, client: TestClient, populated_db: dict):
        """Test getting investiture-based magic systems."""
        response = client.get("/api/v1/magic-systems/investiture-based")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["is_investiture_based"] is True
    
    def test_get_magic_systems_by_world(self, client: TestClient, populated_db: dict):
        """Test getting magic systems by world."""
        world_id = populated_db["world"].id
        response = client.get(f"/api/v1/magic-systems/world/{world_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["world_id"] == world_id


class TestShardEndpoints:
    """Integration tests for shard endpoints."""
    
    def test_get_shards(self, client: TestClient, populated_db: dict):
        """Test getting all shards."""
        response = client.get("/api/v1/shards/")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "Honor"
    
    def test_get_shard_by_id(self, client: TestClient, populated_db: dict):
        """Test getting a shard by ID."""
        shard_id = populated_db["shard"].id
        response = client.get(f"/api/v1/shards/{shard_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == shard_id
        assert data["name"] == "Honor"
    
    def test_get_whole_shards(self, client: TestClient, populated_db: dict):
        """Test getting whole shards."""
        response = client.get("/api/v1/shards/whole")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 0  # No whole shards in test data
    
    def test_get_splintered_shards(self, client: TestClient, populated_db: dict):
        """Test getting splintered shards."""
        response = client.get("/api/v1/shards/splintered")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "splintered"
    
    def test_get_shards_by_intent(self, client: TestClient, populated_db: dict):
        """Test getting shards by intent."""
        response = client.get("/api/v1/shards/intent/Honor")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["intent"] == "Honor"


class TestSearchEndpoints:
    """Integration tests for search endpoints."""
    
    def test_search_all(self, client: TestClient, populated_db: dict):
        """Test searching across all entities."""
        response = client.get("/api/v1/search/?q=Roshar")
        assert response.status_code == 200
        
        data = response.json()
        assert "worlds" in data
        assert "series" in data
        assert "books" in data
        assert "characters" in data
        assert "magic_systems" in data
        assert "shards" in data
        assert "total_results" in data
    
    def test_search_by_type(self, client: TestClient, populated_db: dict):
        """Test searching by entity type."""
        response = client.get("/api/v1/search/worlds?q=Roshar")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Roshar"
    
    def test_get_search_suggestions(self, client: TestClient, populated_db: dict):
        """Test getting search suggestions."""
        response = client.get("/api/v1/search/suggestions?q=Ros")
        assert response.status_code == 200
        
        data = response.json()
        assert "suggestions" in data
        assert "search_term" in data
        assert "Roshar" in data["suggestions"]


class TestHealthEndpoints:
    """Integration tests for health endpoints."""
    
    def test_health_check(self, client: TestClient):
        """Test basic health check."""
        response = client.get("/api/v1/health/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "cosmere-api"
    
    def test_database_health_check(self, client: TestClient):
        """Test database health check."""
        response = client.get("/api/v1/health/db")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "cosmere-api-database"
    
    def test_detailed_health_check(self, client: TestClient):
        """Test detailed health check."""
        response = client.get("/api/v1/health/detailed")
        assert response.status_code == 200
        
        data = response.json()
        assert "timestamp" in data
        assert "service" in data
        assert "status" in data
        assert "checks" in data
        assert data["status"] == "healthy" 