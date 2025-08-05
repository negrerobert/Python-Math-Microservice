"""
Caching system for mathematical operations
"""
import hashlib
import json
import time
from typing import Any, Optional, Dict, Union
from cachetools import TTLCache
from app.utils.logger import cache_logger


class MathCache:
    """
    In-memory cache for mathematical operations with TTL (Time-To-Live)
    """

    def __init__(self, maxsize: int = 1000, ttl: int = 300):  # 5 minutes TTL
        """
        Initialize cache

        Args:
            maxsize: Maximum number of cached items
            ttl: Time-to-live in seconds
        """
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self.stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'deletes': 0,
            'size': 0
        }
        self.start_time = time.time()
        cache_logger.info("Cache initialized", extra={
            'maxsize': maxsize,
            'ttl_seconds': ttl
        })

    def _generate_key(self, operation: str, params: Dict[str, Any]) -> str:
        """
        Generate a unique cache key for the operation and parameters

        Args:
            operation: Type of mathematical operation
            params: Operation parameters

        Returns:
            Unique cache key
        """
        # Create a deterministic string from operation and sorted params
        key_data = {
            'operation': operation,
            'params': dict(sorted(params.items()))
        }
        key_string = json.dumps(key_data, sort_keys=True)

        # Generate SHA256 hash for consistent key length
        return hashlib.sha256(key_string.encode()).hexdigest()[:16]

    def get(self, operation: str, params: Dict[str, Any]) -> Optional[Union[int, float]]:
        """
        Get cached result for operation and parameters

        Args:
            operation: Type of mathematical operation
            params: Operation parameters

        Returns:
            Cached result or None if not found
        """
        key = self._generate_key(operation, params)

        try:
            result = self.cache[key]
            self.stats['hits'] += 1
            cache_logger.debug("Cache hit", extra={
                'operation': operation,
                'key': key,
                'result': result
            })
            return result
        except KeyError:
            self.stats['misses'] += 1
            cache_logger.debug("Cache miss", extra={
                'operation': operation,
                'key': key
            })
            return None

    def set(self, operation: str, params: Dict[str, Any], result: Union[int, float]) -> None:
        """
        Cache the result for operation and parameters

        Args:
            operation: Type of mathematical operation
            params: Operation parameters
            result: Operation result to cache
        """
        key = self._generate_key(operation, params)
        self.cache[key] = result
        self.stats['sets'] += 1
        self.stats['size'] = len(self.cache)

        cache_logger.debug("Cache set", extra={
            'operation': operation,
            'key': key,
            'result': result,
            'cache_size': self.stats['size']
        })

    def delete(self, operation: str, params: Dict[str, Any]) -> bool:
        """
        Delete cached result for operation and parameters

        Args:
            operation: Type of mathematical operation
            params: Operation parameters

        Returns:
            True if deleted, False if not found
        """
        key = self._generate_key(operation, params)

        try:
            del self.cache[key]
            self.stats['deletes'] += 1
            self.stats['size'] = len(self.cache)
            cache_logger.debug("Cache delete", extra={
                'operation': operation,
                'key': key
            })
            return True
        except KeyError:
            return False

    def clear(self) -> None:
        """Clear all cached items"""
        old_size = len(self.cache)
        self.cache.clear()
        self.stats['size'] = 0

        cache_logger.info("Cache cleared", extra={
            'items_removed': old_size
        })

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics

        Returns:
            Dictionary with cache statistics
        """
        total_requests = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        uptime_seconds = time.time() - self.start_time

        return {
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'hit_rate_percent': round(hit_rate, 2),
            'sets': self.stats['sets'],
            'deletes': self.stats['deletes'],
            'current_size': len(self.cache),
            'max_size': self.cache.maxsize,
            'ttl_seconds': self.cache.ttl,
            'uptime_seconds': round(uptime_seconds, 2)
        }

    def get_cache_info(self) -> Dict[str, Any]:
        """Get detailed cache information including stored keys"""
        keys_info = []
        current_time = time.time()

        # Get sample keys (limit to first 10 for performance)
        sample_keys = list(self.cache.keys())[:10]

        for key in sample_keys:
            try:
                # TTLCache doesn't have expire_time method, so we'll calculate it differently
                # We can't get exact expiration time, so we'll just show if key exists
                keys_info.append({
                    'key': key,
                    'value': str(self.cache[key])[:50] + "..." if len(str(self.cache[key])) > 50 else str(self.cache[key]),
                    'status': 'active'
                })
            except KeyError:
                # Key might have expired between getting the list and accessing it
                continue

        return {
            'stats': self.get_stats(),
            'sample_keys': keys_info,
            'total_keys': len(self.cache),
            'note': 'TTL expiration times not available with current cache implementation'
        }


# Global cache instance
math_cache = MathCache(maxsize=1000, ttl=300)  # 5 minutes TTL