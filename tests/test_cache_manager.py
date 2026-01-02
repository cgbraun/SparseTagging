"""Tests for QueryCacheManager."""

import json

import numpy as np
import pytest
from sparsetagging.cache_manager import QueryCacheManager, QueryEncoder
from sparsetagging.sparsetag import QueryResult, SparseTag, TagConfidence


class TestCacheManager:
    """Test suite for QueryCacheManager functionality."""

    def test_initialization(self):
        """Test cache manager initializes correctly."""
        cm = QueryCacheManager(max_entries=100, max_memory_mb=5.0)
        assert cm.stats()["size_entries"] == 0
        assert cm.hit_rate == pytest.approx(0.0)
        assert cm.memory_mb == pytest.approx(0.0)

    def test_get_put_cycle(self):
        """Test storing and retrieving results."""
        cm = QueryCacheManager()
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42, enable_cache=False)
        query = {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH}
        result = QueryResult(np.array([1, 2, 3]), bt)

        # Cache miss
        assert cm.get(query) is None

        # Store
        cm.put(query, result)

        # Cache hit
        cached = cm.get(query)
        assert cached is not None
        assert np.array_equal(cached.indices, result.indices)

    def test_cache_hit_miss_tracking(self):
        """Test hit/miss statistics are tracked correctly."""
        cm = QueryCacheManager()
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42, enable_cache=False)

        query1 = {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH}
        query2 = {"column": "Tag1", "op": "==", "value": TagConfidence.LOW}

        result1 = QueryResult(np.array([1, 2, 3]), bt)
        QueryResult(np.array([4, 5]), bt)

        # First access - miss
        assert cm.get(query1) is None
        stats = cm.stats()
        assert stats["hits"] == 0
        assert stats["misses"] == 1

        # Cache it
        cm.put(query1, result1)

        # Second access - hit
        cached = cm.get(query1)
        assert cached is not None
        stats = cm.stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["hit_rate"] == pytest.approx(0.5)

        # Different query - miss
        assert cm.get(query2) is None
        stats = cm.stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 2

    def test_memory_bounds(self):
        """Test cache respects memory limits."""
        cm = QueryCacheManager(max_memory_mb=0.001)  # Very small limit (1KB)
        bt = SparseTag.create_random(10000, ["Tag1"], 0.1, seed=42, enable_cache=False)
        result = QueryResult(np.arange(5000), bt)  # Large result (~40KB)

        query = {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH}
        cm.put(query, result)

        # Should not cache due to size
        stats = cm.stats()
        assert stats["size_entries"] == 0  # Too large to cache

    def test_entry_limit(self):
        """Test cache respects entry limits."""
        cm = QueryCacheManager(max_entries=3)
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42, enable_cache=False)

        # Add 3 entries (should all be cached)
        for i in range(3):
            query = {"column": "Tag1", "op": "==", "value": i + 1}
            result = QueryResult(np.array([i]), bt)
            cm.put(query, result)

        stats = cm.stats()
        assert stats["size_entries"] == 3

        # Try to add 4th entry (should not be cached)
        query4 = {"column": "Tag1", "op": "==", "value": 3}
        result4 = QueryResult(np.array([10]), bt)
        cm.put(query4, result4)

        stats = cm.stats()
        assert stats["size_entries"] == 3  # Still 3, not 4

    def test_clear(self):
        """Test cache clearing."""
        cm = QueryCacheManager()
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42, enable_cache=False)
        result = QueryResult(np.array([1, 2, 3]), bt)
        query = {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH}

        cm.put(query, result)
        assert cm.stats()["size_entries"] == 1

        cm.clear()
        assert cm.stats()["size_entries"] == 0
        assert cm.memory_mb == pytest.approx(0.0)

    def test_key_generation_simple_query(self):
        """Test fast path for simple single-column queries."""
        cm = QueryCacheManager()

        # Simple query should use fast path
        query1 = {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH}
        key1 = cm._generate_key(query1)
        assert isinstance(key1, str)
        assert len(key1) == 32  # MD5 hash length

        # Same query should generate same key
        query2 = {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH}
        key2 = cm._generate_key(query2)
        assert key1 == key2

        # Different value should generate different key
        query3 = {"column": "Tag1", "op": "==", "value": TagConfidence.LOW}
        key3 = cm._generate_key(query3)
        assert key1 != key3

    def test_key_generation_complex_query(self):
        """Test JSON serialization path for complex queries."""
        cm = QueryCacheManager()

        # Complex query uses JSON serialization
        query1 = {
            "operator": "AND",
            "conditions": [
                {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH},
                {"column": "Tag2", "op": ">=", "value": TagConfidence.MEDIUM},
            ],
        }
        key1 = cm._generate_key(query1)
        assert isinstance(key1, str)
        assert len(key1) == 32

        # Same complex query should generate same key
        query2 = {
            "operator": "AND",
            "conditions": [
                {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH},
                {"column": "Tag2", "op": ">=", "value": TagConfidence.MEDIUM},
            ],
        }
        key2 = cm._generate_key(query2)
        assert key1 == key2

    def test_key_generation_with_in_operator(self):
        """Test key generation with IN operator and values list."""
        cm = QueryCacheManager()

        query = {"column": "Tag1", "op": "IN", "values": [TagConfidence.HIGH, TagConfidence.MEDIUM]}
        key = cm._generate_key(query)
        assert isinstance(key, str)
        assert len(key) == 32

    def test_stats_accuracy(self):
        """Test that stats accurately reflect cache state."""
        cm = QueryCacheManager()
        bt = SparseTag.create_random(1000, ["Tag1"], 0.1, seed=42, enable_cache=False)

        # Add multiple entries
        for i in range(5):
            query = {"column": "Tag1", "op": "==", "value": i % 3 + 1}
            result = QueryResult(np.array([i * 10, i * 10 + 1]), bt)
            cm.put(query, result)

        stats = cm.stats()
        assert stats["size_entries"] <= 5
        assert stats["size_bytes"] > 0
        assert stats["size_mb"] > 0
        assert stats["size_mb"] == stats["size_bytes"] / (1024**2)

    def test_large_result_threshold(self):
        """Test that large results are not cached based on threshold."""
        cm = QueryCacheManager(large_result_threshold_mb=0.001)  # 1KB threshold
        bt = SparseTag.create_random(10000, ["Tag1"], 0.1, seed=42, enable_cache=False)

        # Small result (should be cached)
        small_result = QueryResult(np.array([1, 2, 3]), bt)
        small_query = {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH}
        cm.put(small_query, small_result)
        assert cm.stats()["size_entries"] == 1

        # Large result (should not be cached)
        large_result = QueryResult(np.arange(1000), bt)
        large_query = {
            "column": "Tag1",
            "op": "IN",
            "values": [TagConfidence.HIGH, TagConfidence.MEDIUM],
        }
        cm.put(large_query, large_result)
        assert cm.stats()["size_entries"] == 1  # Still only 1 entry


class TestQueryEncoder:
    """Test suite for QueryEncoder JSON serialization."""

    def test_encode_tag_confidence(self):
        """Test encoding TagConfidence enum values."""
        QueryEncoder()

        query = {"value": TagConfidence.HIGH}
        result = json.dumps(query, cls=QueryEncoder)
        assert "3" in result  # HIGH = 3

    def test_encode_numpy_types(self):
        """Test encoding NumPy integer and float types."""
        QueryEncoder()

        # NumPy integer
        query = {"value": np.int64(42)}
        result = json.dumps(query, cls=QueryEncoder)
        assert "42" in result

        # NumPy float
        query = {"value": np.float64(3.14)}
        result = json.dumps(query, cls=QueryEncoder)
        assert "3.14" in result

    def test_encode_numpy_array(self):
        """Test encoding NumPy arrays."""
        QueryEncoder()

        query = {"values": np.array([1, 2, 3])}
        result = json.dumps(query, cls=QueryEncoder)
        decoded = json.loads(result)
        assert decoded["values"] == [1, 2, 3]

    def test_encode_mixed_types(self):
        """Test encoding mixed types in complex query."""
        query = {
            "operator": "AND",
            "conditions": [
                {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH},
                {"column": "Tag2", "op": "IN", "values": np.array([1, 2])},
            ],
        }

        result = json.dumps(query, cls=QueryEncoder)
        decoded = json.loads(result)

        assert decoded["operator"] == "AND"
        assert decoded["conditions"][0]["value"] == 3  # HIGH
        assert decoded["conditions"][1]["values"] == [1, 2]
