import aioredis
import redis
import json
from typing import Any, Optional, Callable
from app.core.config import settings
import functools
import asyncio

class CacheService:
    def __init__(self):
        self.redis = aioredis.from_url(settings.redis_url, decode_responses=True)
        self.default_ttl = settings.cache_ttl

    async def get(self, key: str) -> Optional[Any]:
        try:
            value = await self.redis.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        try:
            ttl = ttl or self.default_ttl
            return await self.redis.setex(key, ttl, json.dumps(value, default=str))
        except Exception as e:
            print(f"Cache set error: {e}")
            return False

    async def delete(self, key: str) -> int:
        try:
            return await self.redis.delete(key)
        except Exception as e:
            print(f"Cache delete error: {e}")
            return 0

    async def clear_pattern(self, pattern: str) -> int:
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                return await self.redis.delete(*keys)
            return 0
        except Exception as e:
            print(f"Cache clear pattern error: {e}")
            return 0

class SyncCacheService:
    def __init__(self):
        self.redis = redis.from_url(settings.redis_url, decode_responses=True)
        self.default_ttl = settings.cache_ttl

    def get(self, key: str) -> Optional[Any]:
        try:
            value = self.redis.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            print(f"Sync cache get error: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        try:
            ttl = ttl or self.default_ttl
            return self.redis.setex(key, ttl, json.dumps(value, default=str))
        except Exception as e:
            print(f"Sync cache set error: {e}")
            return False

    def delete(self, key: str) -> int:
        try:
            return self.redis.delete(key)
        except Exception as e:
            print(f"Sync cache delete error: {e}")
            return 0

    def clear_pattern(self, pattern: str) -> int:
        try:
            keys = self.redis.keys(pattern)
            if keys:
                return self.redis.delete(*keys)
            return 0
        except Exception as e:
            print(f"Sync cache clear pattern error: {e}")
            return 0

# Decorator for caching synchronous endpoint responses
def cache_response(ttl: int = 3600, key_prefix: str = ""):  # 1 hour default
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_service = SyncCacheService()
            # Create a cache key based on function name and arguments
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached_result = cache_service.get(cache_key)
            if cached_result:
                return cached_result
            result = func(*args, **kwargs)
            cache_service.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator

# Decorator for caching asynchronous endpoint responses
def cache_response_async(ttl: int = 3600, key_prefix: str = ""):  # 1 hour default
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cache_service = CacheService()
            # Create a cache key based on function name and arguments
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached_result = await cache_service.get(cache_key)
            if cached_result:
                return cached_result
            result = await func(*args, **kwargs)
            await cache_service.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator 