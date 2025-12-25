"""Tests for critical bug fixes."""

import json

import numpy as np
import pytest
from scipy import sparse
from sparsetagging.cache_manager import QueryEncoder
from sparsetagging.sparsetag import SparseTag, TagConfidence


class TestIndexDtypeValidation:
    """Test index dtype conversion validation."""

    def test_validates_max_index_before_conversion(self):
        """Ensures conversion validates actual index values."""
        # Create matrix with data in high row indices
        n_rows = 300
        rows = np.array([250, 260, 270, 280, 290])
        cols = np.array([0, 1, 2, 3, 4])
        values = np.array([1, 2, 3, 1, 2], dtype=np.uint8)
        data = sparse.csc_array((values, (rows, cols)), shape=(n_rows, 5), dtype=np.uint8)

        bt = SparseTag.from_sparse(data, [f"Tag{i}" for i in range(5)])

        # Should NOT optimize to int8 (max index 290 > 127)
        result = bt.optimize_indices_dtype(inplace=False)

        # Should either not optimize or use int16
        if result is not None:
            assert result._data.indices.dtype in (
                np.int16,
                np.int32,
            ), f"Should use int16 or int32, got {result._data.indices.dtype}"

        # Verify data integrity
        assert bt._data.nnz == 5
        assert np.all(bt._data.indices >= 250)

    def test_preserves_data_after_optimization(self):
        """Ensures optimization doesn't corrupt data."""
        bt = SparseTag.create_random(1000, ["Tag1", "Tag2"], 0.1, seed=42)
        original = bt._data.toarray()

        bt.optimize_indices_dtype(inplace=True)
        optimized = bt._data.toarray()

        assert np.array_equal(original, optimized)


class TestOverflowProtection:
    """Test integer overflow protection."""

    def test_detects_overflow_in_create_random(self):
        """Ensures overflow is detected and raises clear error."""
        with pytest.raises(ValueError, match="exceeds safe limit"):
            SparseTag.create_random(100000, ["Tag1"] * 50000, 0.5, seed=42)

    def test_handles_zero_nnz(self):
        """Handles zero fill_percent gracefully."""
        bt = SparseTag.create_random(1000, ["Tag1", "Tag2"], 0.0, seed=42)
        assert bt._data.nnz == 0
        assert bt.shape == (1000, 2)

    def test_thread_safe_random_generation(self):
        """Ensures local RNG doesn't affect global state."""
        np.random.seed(999)
        bt1 = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)

        np.random.seed(111)  # Different global seed
        bt2 = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)

        # Should be identical (local RNG ignores global state)
        assert np.array_equal(bt1._data.toarray(), bt2._data.toarray())


class TestJSONSerialization:
    """Test JSON serialization for cache keys."""

    def test_handles_tagconfidence_enums(self):
        """Ensures enums are serialized correctly."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42, enable_cache=True)

        # Query with enum (should not crash)
        query = {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH}
        bt.query(query)
        bt.query(query)  # Should hit cache

        stats = bt.cache_stats()
        assert stats["hits"] == 1

    def test_query_encoder_handles_types(self):
        """QueryEncoder handles various types."""
        QueryEncoder()

        # TagConfidence enum
        assert json.dumps({"value": TagConfidence.HIGH}, cls=QueryEncoder) == '{"value": 3}'

        # NumPy types
        assert json.dumps({"value": np.int32(5)}, cls=QueryEncoder) == '{"value": 5}'
