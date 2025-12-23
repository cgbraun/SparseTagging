"""Query cache management with memory bounds and statistics."""

import hashlib
import json
import logging
from typing import Dict, Optional, Union, TYPE_CHECKING, Any
import numpy as np

if TYPE_CHECKING:
    from .basetag import QueryResult, TagConfidence

logger = logging.getLogger(__name__)

DEFAULT_CACHE_MAX_ENTRIES = 256
DEFAULT_CACHE_MAX_MEMORY_MB = 10
DEFAULT_LARGE_RESULT_THRESHOLD_MB = 1.0
CACHE_OVERHEAD_BYTES = 200


class QueryEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for query dictionaries.

    Handles TagConfidence enums and NumPy types that aren't natively JSON serializable.
    This ensures cache keys can be generated for all valid query structures.
    """
    def default(self, obj: Any) -> Any:
        # Import here to avoid circular dependency
        from .basetag import TagConfidence

        if isinstance(obj, TagConfidence):
            return int(obj)
        elif isinstance(obj, (np.integer, np.floating)):
            return int(obj) if isinstance(obj, np.integer) else float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


class QueryCacheManager:
    """
    Manages query result caching with memory bounds and statistics.

    Features:
    - MD5-based cache keys for consistent hashing
    - Memory-bounded storage (entries + MB limits)
    - Hit/miss statistics tracking
    - Automatic size tracking (O(1))
    """

    def __init__(
        self,
        max_entries: int = DEFAULT_CACHE_MAX_ENTRIES,
        max_memory_mb: float = DEFAULT_CACHE_MAX_MEMORY_MB,
        large_result_threshold_mb: float = DEFAULT_LARGE_RESULT_THRESHOLD_MB
    ) -> None:
        self._cache: Dict[str, Any] = {}  # query_hash → QueryResult
        self._cache_hits = 0
        self._cache_misses = 0
        self._cache_memory_bytes = 0
        self._max_entries = max_entries
        self._max_memory_mb = max_memory_mb
        self._large_result_threshold_mb = large_result_threshold_mb

    def get(self, query_dict: Dict[str, Any]) -> Optional[Any]:
        """Get cached result for query, or None if not cached."""
        key = self._generate_key(query_dict)
        if key in self._cache:
            self._cache_hits += 1
            logger.debug(f"Cache hit (rate: {self.hit_rate:.1%})")
            return self._cache[key]
        self._cache_misses += 1
        return None

    def put(self, query_dict: Dict[str, Any], result: Any) -> None:
        """Store query result in cache if it meets caching criteria."""
        if not self._should_cache(result):
            return

        key = self._generate_key(query_dict)
        result_size = result.indices.nbytes + CACHE_OVERHEAD_BYTES
        self._cache[key] = result
        self._cache_memory_bytes += result_size
        logger.debug(f"Cached result ({len(self._cache)} entries, {self.memory_mb:.2f}MB)")

    def clear(self) -> None:
        """Clear all cached entries."""
        old_size = len(self._cache)
        self._cache.clear()
        self._cache_memory_bytes = 0
        logger.info(f"Cache cleared: {old_size} entries removed")

    def stats(self) -> Dict[str, Union[int, float, bool]]:
        """Get cache performance statistics."""
        total = self._cache_hits + self._cache_misses
        hit_rate = self._cache_hits / total if total > 0 else 0

        # Recalculate actual size for accuracy
        size_bytes = sum(
            r.indices.nbytes + CACHE_OVERHEAD_BYTES for r in self._cache.values()
        )

        return {
            'hits': self._cache_hits,
            'misses': self._cache_misses,
            'hit_rate': hit_rate,
            'size_entries': len(self._cache),
            'size_bytes': size_bytes,
            'size_mb': size_bytes / (1024**2)
        }

    @property
    def hit_rate(self) -> float:
        """Calculate current cache hit rate."""
        total = self._cache_hits + self._cache_misses
        return self._cache_hits / total if total > 0 else 0

    @property
    def memory_mb(self) -> float:
        """Get current cache memory usage in MB."""
        return self._cache_memory_bytes / (1024**2)

    def _generate_key(self, query_dict: Dict[str, Any]) -> str:
        """Generate MD5 cache key from query dictionary."""
        # Import here to avoid circular dependency
        from .basetag import TagConfidence

        # Fast path for simple single-column queries
        if 'column' in query_dict and 'operator' not in query_dict:
            col = query_dict['column']
            op = query_dict.get('op', '==')

            if 'value' in query_dict:
                val = int(query_dict['value']) if isinstance(query_dict['value'], TagConfidence) else query_dict['value']
                key_str = f"{col}|{op}|{val}"
            elif 'values' in query_dict:
                vals = tuple(int(v) if isinstance(v, TagConfidence) else v for v in query_dict['values'])
                key_str = f"{col}|{op}|{vals}"
            else:
                key_str = f"{col}|{op}"

            return hashlib.md5(key_str.encode()).hexdigest()

        # Complex query: use JSON serialization
        try:
            query_str = json.dumps(query_dict, sort_keys=True, cls=QueryEncoder)
            return hashlib.md5(query_str.encode()).hexdigest()
        except (TypeError, ValueError) as e:
            logger.warning(f"Failed to serialize query, using repr: {e}")
            query_str = repr(sorted(query_dict.items()))
            return hashlib.md5(query_str.encode()).hexdigest()

    def _should_cache(self, result: Any) -> bool:
        """Determine if query result should be cached."""
        # Check entry limit
        if len(self._cache) >= self._max_entries:
            logger.debug(f"Cache full ({self._max_entries} entries)")
            return False

        # Check result size
        result_size_mb = (result.indices.nbytes + CACHE_OVERHEAD_BYTES) / (1024**2)
        if result_size_mb > self._large_result_threshold_mb:
            logger.debug(f"Not caching large result ({result_size_mb:.2f}MB)")
            return False

        # Check total cache memory
        if self.memory_mb + result_size_mb > self._max_memory_mb:
            logger.debug(f"Not caching (would exceed {self._max_memory_mb}MB)")
            return False

        return True
