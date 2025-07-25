"""
Cache service for Redis-based caching.
"""
import json
import hashlib
from typing import Any, Optional, Dict, List
from datetime import timedelta
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Optional Redis import
try:
    import aioredis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    aioredis = None


class CacheService:
    """Service for Redis-based caching."""
    
    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self.default_ttl = settings.CACHE_TTL
        self._redis = None
    
    async def get_redis(self):
        """Get Redis connection."""
        if not REDIS_AVAILABLE:
            logger.warning("Redis not available - caching disabled")
            return None
        if self._redis is None:
            self._redis = aioredis.from_url(self.redis_url)
        return self._redis
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate a cache key from prefix and arguments."""
        # Create a hash of the arguments
        key_parts = [prefix]
        
        for arg in args:
            key_parts.append(str(arg))
        
        for key, value in sorted(kwargs.items()):
            key_parts.append(f"{key}:{value}")
        
        key_string = "|".join(key_parts)
        return f"cosmere:{hashlib.md5(key_string.encode()).hexdigest()}"
    
    async def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        try:
            redis = await self.get_redis()
            if redis is None:
                return None
            value = await redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting from cache: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set a value in cache."""
        try:
            redis = await self.get_redis()
            if redis is None:
                return False
            ttl = ttl or self.default_ttl
            await redis.setex(key, ttl, json.dumps(value, default=str))
            return True
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete a value from cache."""
        try:
            redis = await self.get_redis()
            if redis is None:
                return False
            await redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if a key exists in cache."""
        try:
            redis = await self.get_redis()
            if redis is None:
                return False
            return await redis.exists(key) > 0
        except Exception as e:
            logger.error(f"Error checking cache existence: {e}")
            return False
    
    async def get_or_set(self, key: str, getter_func, ttl: int = None) -> Any:
        """Get from cache or set if not exists."""
        # Try to get from cache first
        cached_value = await self.get(key)
        if cached_value is not None:
            return cached_value
        
        # If not in cache, get from function and cache it
        value = await getter_func() if hasattr(getter_func, '__call__') else getter_func
        await self.set(key, value, ttl)
        return value
    
    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching a pattern."""
        try:
            redis = await self.get_redis()
            if redis is None:
                return 0
            keys = await redis.keys(pattern)
            if keys:
                await redis.delete(*keys)
                return len(keys)
            return 0
        except Exception as e:
            logger.error(f"Error invalidating cache pattern: {e}")
            return 0
    
    async def invalidate_entity(self, entity_type: str, entity_id: str = None) -> int:
        """Invalidate cache for a specific entity type and optionally entity ID."""
        pattern = f"cosmere:{entity_type}:*"
        if entity_id:
            pattern = f"cosmere:{entity_type}:{entity_id}:*"
        
        return await self.invalidate_pattern(pattern)
    
    # Entity-specific cache methods
    async def get_world(self, world_id: str) -> Optional[Dict[str, Any]]:
        """Get world from cache."""
        key = self._generate_key("world", world_id)
        return await self.get(key)
    
    async def set_world(self, world_id: str, world_data: Dict[str, Any], ttl: int = None) -> bool:
        """Set world in cache."""
        key = self._generate_key("world", world_id)
        return await self.set(key, world_data, ttl)
    
    async def get_books_by_series(self, series_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get books by series from cache."""
        key = self._generate_key("books", "series", series_id)
        return await self.get(key)
    
    async def set_books_by_series(self, series_id: str, books_data: List[Dict[str, Any]], ttl: int = None) -> bool:
        """Set books by series in cache."""
        key = self._generate_key("books", "series", series_id)
        return await self.set(key, books_data, ttl)
    
    async def get_character_relationships(self, character_id: str) -> Optional[Dict[str, Any]]:
        """Get character relationships from cache."""
        key = self._generate_key("character", "relationships", character_id)
        return await self.get(key)
    
    async def set_character_relationships(self, character_id: str, relationships_data: Dict[str, Any], ttl: int = None) -> bool:
        """Set character relationships in cache."""
        key = self._generate_key("character", "relationships", character_id)
        return await self.set(key, relationships_data, ttl)
    
    async def get_search_results(self, search_term: str, entity_type: str = None) -> Optional[Dict[str, Any]]:
        """Get search results from cache."""
        key = self._generate_key("search", search_term, entity_type=entity_type)
        return await self.get(key)
    
    async def set_search_results(self, search_term: str, results: Dict[str, Any], entity_type: str = None, ttl: int = None) -> bool:
        """Set search results in cache."""
        key = self._generate_key("search", search_term, entity_type=entity_type)
        return await self.set(key, results, ttl)
    
    async def get_overview(self, overview_type: str) -> Optional[Dict[str, Any]]:
        """Get overview data from cache."""
        key = self._generate_key("overview", overview_type)
        return await self.get(key)
    
    async def set_overview(self, overview_type: str, overview_data: Dict[str, Any], ttl: int = None) -> bool:
        """Set overview data in cache."""
        key = self._generate_key("overview", overview_type)
        return await self.set(key, overview_data, ttl)
    
    async def close(self):
        """Close Redis connection."""
        if self._redis:
            await self._redis.close()
            self._redis = None


# Global cache service instance
cache_service = CacheService()
