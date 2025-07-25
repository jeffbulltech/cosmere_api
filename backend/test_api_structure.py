#!/usr/bin/env python3
"""
Simple test script to validate API structure without database connection.
"""
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_imports():
    """Test that all our modules can be imported."""
    print("🔍 Testing module imports...")
    
    try:
        # Test core modules
        from app.core.config import settings
        print("✅ Core config imported successfully")
        
        from app.core.database import get_db
        print("✅ Database module imported successfully")
        
        # Test models
        from app.models import World, Book, Character, Series, MagicSystem, Shard
        print("✅ All models imported successfully")
        
        # Test schemas
        from app.schemas import world, book, character, series, magic_system, shard
        print("✅ All schemas imported successfully")
        
        # Test repositories
        from app.repositories import (
            WorldRepository, BookRepository, CharacterRepository,
            SeriesRepository, MagicSystemRepository, ShardRepository
        )
        print("✅ All repositories imported successfully")
        
        # Test services
        from app.services import (
            WorldService, BookService, CharacterService,
            SeriesService, MagicSystemService, ShardService, SearchService
        )
        print("✅ All services imported successfully")
        
        # Test API endpoints
        from app.api.v1.endpoints import (
            worlds, books, characters, series, magic_systems, shards, search, health
        )
        print("✅ All API endpoints imported successfully")
        
        # Test main app
        from app.main import app
        print("✅ Main app imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_app_structure():
    """Test that the FastAPI app has the expected structure."""
    print("\n🔍 Testing FastAPI app structure...")
    
    try:
        from app.main import app
        
        # Check if app is a FastAPI instance
        from fastapi import FastAPI
        if isinstance(app, FastAPI):
            print("✅ App is a valid FastAPI instance")
        else:
            print("❌ App is not a FastAPI instance")
            return False
        
        # Check for expected routes
        routes = [route.path for route in app.routes]
        print(f"✅ Found {len(routes)} routes")
        
        # Check for API v1 routes
        api_routes = [r for r in routes if r.startswith('/api/v1')]
        print(f"✅ Found {len(api_routes)} API v1 routes")
        
        # Check for specific endpoint categories
        world_routes = [r for r in routes if '/worlds' in r]
        book_routes = [r for r in routes if '/books' in r]
        character_routes = [r for r in routes if '/characters' in r]
        search_routes = [r for r in routes if '/search' in r]
        health_routes = [r for r in routes if '/health' in r]
        
        print(f"✅ World routes: {len(world_routes)}")
        print(f"✅ Book routes: {len(book_routes)}")
        print(f"✅ Character routes: {len(character_routes)}")
        print(f"✅ Search routes: {len(search_routes)}")
        print(f"✅ Health routes: {len(health_routes)}")
        
        return True
        
    except Exception as e:
        print(f"❌ App structure test failed: {e}")
        return False

def test_configuration():
    """Test configuration loading."""
    print("\n🔍 Testing configuration...")
    
    try:
        from app.core.config import settings
        
        # Check essential settings
        required_settings = [
            'APP_NAME', 'APP_VERSION', 'API_V1_STR', 'PROJECT_NAME',
            'DATABASE_URL', 'SECRET_KEY'
        ]
        
        for setting in required_settings:
            if hasattr(settings, setting):
                print(f"✅ {setting}: {getattr(settings, setting)}")
            else:
                print(f"❌ Missing setting: {setting}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Cosmere API Structure")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_app_structure,
        test_configuration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API structure is valid.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 