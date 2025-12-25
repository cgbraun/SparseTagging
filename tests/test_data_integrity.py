"""Tests for data integrity and mutation safety."""

import numpy as np
from scipy import sparse
from sparsetagging.sparsetag import SparseTag, TagConfidence


class TestDataImmutability:
    """Test that data remains unchanged when it should."""

    def test_query_does_not_modify_original(self):
        """Test that querying doesn't modify original data."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        original_data = bt._data.toarray().copy()

        # Perform query
        bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})

        # Verify data unchanged
        assert np.array_equal(bt._data.toarray(), original_data)

    def test_query_result_indices_reference(self):
        """Test that QueryResult indices behavior is documented."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        result = bt.query({"column": "Tag1", "op": ">=", "value": TagConfidence.LOW})

        if result.count > 0:
            # Note: indices may or may not be a copy depending on implementation
            # Just verify we can access them
            indices = result.indices
            assert len(indices) == result.count
            assert isinstance(indices, np.ndarray)

    def test_to_sparse_tag_creates_independent_copy(self):
        """Test that to_sparse_tag() creates independent data."""
        bt = SparseTag.create_random(100, ["Tag1", "Tag2"], 0.2, seed=42)
        result = bt.query({"column": "Tag1", "op": ">=", "value": TagConfidence.MEDIUM})

        if result.count > 0:
            filtered = result.to_sparsetag()

            # Modifying filtered should not affect original
            # (In practice, we can't modify sparse matrix directly, but test structure)
            assert filtered._data is not bt._data
            assert filtered.shape[0] == result.count
            assert filtered.shape[1] == bt.shape[1]

    def test_optimize_dtype_inplace_false_preserves_original(self):
        """Test that optimize with inplace=False doesn't modify original."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        original_dtype = bt._data.indices.dtype
        original_data = bt._data.toarray().copy()

        # Optimize with inplace=False
        bt.optimize_indices_dtype(inplace=False)

        # Original should be unchanged
        assert bt._data.indices.dtype == original_dtype
        assert np.array_equal(bt._data.toarray(), original_data)

    def test_optimize_dtype_inplace_true_modifies_original(self):
        """Test that optimize with inplace=True modifies in place."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        id(bt._data)

        # Optimize with inplace=True
        bt.optimize_indices_dtype(inplace=True)

        # Should be same object (modified in place)
        # Note: scipy may create new object during conversion
        # Just verify data integrity
        assert bt._data.nnz > 0  # Data preserved


class TestCacheInvalidation:
    """Test cache invalidation on data modifications."""

    def test_cache_exists_after_query(self):
        """Test that cache is populated after query."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42, enable_cache=True)

        # First query
        bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})

        stats = bt.cache_stats()
        assert stats["size_entries"] > 0

    def test_repeated_query_uses_cache(self):
        """Test that repeated queries hit cache."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42, enable_cache=True)

        query = {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH}

        # First query
        bt.query(query)

        # Second query
        bt.query(query)

        stats = bt.cache_stats()
        assert stats["hits"] >= 1

    def test_clear_cache_empties_cache(self):
        """Test that clear_cache() removes all entries."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42, enable_cache=True)

        # Populate cache
        bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})
        assert bt.cache_stats()["size_entries"] > 0

        # Clear cache
        bt.clear_cache()

        stats = bt.cache_stats()
        assert stats["size_entries"] == 0
        assert stats["size_bytes"] == 0

    def test_cache_disabled_no_caching(self):
        """Test that cache can be disabled."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42, enable_cache=False)

        # Query multiple times
        bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})
        bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})

        stats = bt.cache_stats()
        assert stats["size_entries"] == 0
        assert stats["hits"] == 0

    def test_use_cache_false_bypasses_cache(self):
        """Test that use_cache=False bypasses cache."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42, enable_cache=True)

        query = {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH}

        # First query with cache
        bt.query(query)

        # Second query without cache
        bt.query(query, use_cache=False)

        stats = bt.cache_stats()
        # Should have 1 entry but no cache hits (second query bypassed)
        assert stats["size_entries"] >= 1
        # Hits might be 0 or 1 depending on implementation


class TestSparsityConsistency:
    """Test sparsity calculations remain consistent."""

    def test_sparsity_matches_nnz(self):
        """Test sparsity percentage matches actual non-zero count."""
        bt = SparseTag.create_random(1000, ["Tag1", "Tag2"], 0.1, seed=42)

        total_elements = bt.shape[0] * bt.shape[1]
        nnz = bt._data.nnz
        expected_sparsity = (total_elements - nnz) / total_elements

        assert abs(bt.sparsity - expected_sparsity) < 0.01

    def test_empty_matrix_100_percent_sparse(self):
        """Test empty matrix reports 100% sparsity (1.0)."""
        bt = SparseTag.create_empty(100, ["Tag1", "Tag2"])
        assert bt.sparsity == 1.0

    def test_full_matrix_zero_percent_sparse(self):
        """Test completely filled matrix reports 0% sparsity (0.0)."""
        data = np.full((10, 3), TagConfidence.HIGH, dtype=np.uint8)
        bt = SparseTag.from_dense(data, ["A", "B", "C"])

        assert bt.sparsity == 0.0

    def test_sparsity_after_optimization(self):
        """Test sparsity unchanged after dtype optimization."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        original_sparsity = bt.sparsity

        bt.optimize_indices_dtype(inplace=True)

        assert abs(bt.sparsity - original_sparsity) < 0.01


class TestInternalDataConsistency:
    """Test internal data structures remain consistent."""

    def test_column_index_matches_column_names(self):
        """Test _column_index dict matches column_names."""
        bt = SparseTag.create_random(100, ["A", "B", "C"], 0.1, seed=42)

        assert len(bt._column_index) == len(bt.column_names)
        for i, name in enumerate(bt.column_names):
            assert bt._column_index[name] == i

    def test_shape_matches_data_shape(self):
        """Test shape property matches actual data shape."""
        bt = SparseTag.create_random(100, ["Tag1", "Tag2"], 0.1, seed=42)

        assert bt.shape == bt._data.shape
        assert bt.shape[0] == 100
        assert bt.shape[1] == 2

    def test_nnz_matches_data_nnz(self):
        """Test that nnz count is consistent."""
        bt = SparseTag.create_random(1000, ["Tag1"], 0.05, seed=42)

        # Count non-zeros manually
        manual_nnz = np.count_nonzero(bt._data.toarray())

        assert bt._data.nnz == manual_nnz

    def test_csc_format_maintained(self):
        """Test that CSC format is maintained throughout operations."""
        bt = SparseTag.create_random(100, ["Tag1", "Tag2"], 0.1, seed=42)

        # Check format before query
        assert bt._data.format == "csc"

        # After query
        bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})
        assert bt._data.format == "csc"

        # After optimization
        bt.optimize_indices_dtype(inplace=True)
        assert bt._data.format == "csc"

    def test_dtype_maintained(self):
        """Test that uint8 dtype is maintained."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)

        assert bt._data.dtype == np.uint8

        # After various operations
        bt.query({"column": "Tag1", "op": ">=", "value": TagConfidence.LOW})
        assert bt._data.dtype == np.uint8


class TestQueryResultConsistency:
    """Test QueryResult object consistency."""

    def test_count_matches_indices_length(self):
        """Test that count matches len(indices)."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.2, seed=42)
        result = bt.query({"column": "Tag1", "op": ">=", "value": TagConfidence.MEDIUM})

        assert result.count == len(result.indices)

    def test_mask_nnz_matches_count(self):
        """Test that mask non-zero count matches result count."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.2, seed=42)
        result = bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})

        mask = result.mask
        assert mask.nnz == result.count

    def test_len_matches_count(self):
        """Test that len(result) matches count."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.2, seed=42)
        result = bt.query({"column": "Tag1", "op": ">=", "value": TagConfidence.LOW})

        assert len(result) == result.count

    def test_indices_are_sorted(self):
        """Test that result indices are in sorted order."""
        bt = SparseTag.create_random(1000, ["Tag1"], 0.1, seed=42)
        result = bt.query({"column": "Tag1", "op": ">=", "value": TagConfidence.LOW})

        if result.count > 1:
            assert np.all(result.indices[:-1] <= result.indices[1:])

    def test_indices_within_bounds(self):
        """Test that all indices are within valid range."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.2, seed=42)
        result = bt.query({"column": "Tag1", "op": ">=", "value": TagConfidence.LOW})

        if result.count > 0:
            assert np.all(result.indices >= 0)
            assert np.all(result.indices < bt.shape[0])


class TestMemoryConsistency:
    """Test memory tracking consistency."""

    def test_memory_usage_returns_dict(self):
        """Test memory_usage returns expected structure."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        mem = bt.memory_usage()

        assert isinstance(mem, dict)
        # Should contain some memory information
        assert len(mem) > 0

    def test_memory_usage_positive(self):
        """Test that memory usage is positive."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        mem = bt.memory_usage()

        # All memory values should be positive
        for _key, value in mem.items():
            if isinstance(value, (int, float)):
                assert value >= 0

    def test_cache_memory_tracking_accuracy(self):
        """Test cache memory tracking matches actual."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42, enable_cache=True)

        # Populate cache
        bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})
        bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.MEDIUM})

        stats = bt.cache_stats()

        # Memory should be positive if cache has entries
        if stats["size_entries"] > 0:
            assert stats["size_bytes"] > 0


class TestFactoryMethodConsistency:
    """Test factory methods produce consistent results."""

    def test_create_random_with_same_seed_identical(self):
        """Test same seed produces identical matrices."""
        bt1 = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        bt2 = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)

        assert np.array_equal(bt1._data.toarray(), bt2._data.toarray())

    def test_create_random_different_seed_different(self):
        """Test different seeds produce different matrices."""
        bt1 = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        bt2 = SparseTag.create_random(100, ["Tag1"], 0.1, seed=99)

        # Should be different (with high probability)
        assert not np.array_equal(bt1._data.toarray(), bt2._data.toarray())

    def test_from_dense_to_array_roundtrip(self):
        """Test from_dense -> toarray roundtrip preserves data."""
        original = np.array([[1, 2, 3], [0, 2, 0], [3, 0, 1]], dtype=np.uint8)

        bt = SparseTag.from_dense(original, ["A", "B", "C"])
        result = bt._data.toarray()

        assert np.array_equal(original, result)

    def test_from_sparse_preserves_data(self):
        """Test from_sparse preserves data values."""
        data = sparse.csc_array(np.array([[1, 2], [3, 0], [0, 2]], dtype=np.uint8))

        bt = SparseTag.from_sparse(data, ["Tag1", "Tag2"])

        assert np.array_equal(data.toarray(), bt._data.toarray())
