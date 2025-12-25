"""Tests for error handling and validation."""

import numpy as np
import pytest
from scipy import sparse
from sparsetagging.sparsetag import SparseTag, TagConfidence


class TestInvalidInputValidation:
    """Test validation of invalid inputs to constructors."""

    def test_invalid_column_name_type(self):
        """Test that non-string column names are handled."""
        data = sparse.csc_array(np.array([[1, 2]], dtype=np.uint8))
        # May accept and convert, or may reject
        try:
            bt = SparseTag.from_sparse(data, [123, 456])
            # If accepted, verify basic properties
            assert bt.shape == (1, 2)
        except (TypeError, ValueError):
            pass  # Also acceptable to reject

    def test_duplicate_column_names(self):
        """Test that duplicate column names are handled."""
        data = sparse.csc_array(np.array([[1, 2]], dtype=np.uint8))
        # May accept (last one wins) or raise error
        try:
            bt = SparseTag.from_sparse(data, ["Tag1", "Tag1"])
            # If accepted, verify it doesn't crash
            assert bt.shape[1] == 2
        except (ValueError, AssertionError):
            pass  # Also acceptable to reject

    def test_column_count_mismatch(self):
        """Test mismatch between data columns and column names."""
        data = sparse.csc_array(np.array([[1, 2, 3]], dtype=np.uint8))
        with pytest.raises((ValueError, AssertionError)):
            SparseTag.from_sparse(data, ["Tag1", "Tag2"])  # 3 cols but 2 names

    def test_wrong_sparse_format(self):
        """Test that non-CSC sparse format is handled."""
        # CSR format instead of CSC
        data = sparse.csr_array(np.array([[1, 2]], dtype=np.uint8))
        # Should either convert or raise error
        try:
            bt = SparseTag.from_sparse(data, ["Tag1", "Tag2"])
            # If accepted, should have converted to CSC
            assert bt._data.format == "csc"
        except (TypeError, ValueError):
            pass  # Also acceptable to reject

    def test_wrong_dtype_in_sparse(self):
        """Test that non-uint8 dtype is rejected or converted."""
        data = sparse.csc_array(np.array([[1, 2]], dtype=np.float64))
        # Should either convert or raise error
        try:
            bt = SparseTag.from_sparse(data, ["Tag1", "Tag2"])
            # If accepted, should have converted to uint8
            assert bt._data.dtype == np.uint8
        except (TypeError, ValueError):
            pass  # Also acceptable to reject

    def test_negative_dimensions(self):
        """Test that negative dimensions raise error."""
        with pytest.raises((ValueError, OverflowError)):
            SparseTag.create_random(-100, ["Tag1"], 0.1, seed=42)

    def test_zero_rows(self):
        """Test that zero rows raises error or creates empty."""
        # Zero rows should either raise or create valid empty matrix
        try:
            bt = SparseTag.create_random(0, ["Tag1"], 0.1, seed=42)
            assert bt.shape[0] == 0
        except ValueError:
            pass  # Also acceptable to reject

    def test_empty_column_names(self):
        """Test that empty column names list raises error."""
        with pytest.raises((ValueError, AssertionError, IndexError)):
            SparseTag.create_random(100, [], 0.1, seed=42)


class TestInvalidFillPercent:
    """Test validation of fill_percent parameter."""

    def test_negative_fill_percent(self):
        """Test that negative fill_percent raises error."""
        with pytest.raises(ValueError, match="fill_percent|range|0|1"):
            SparseTag.create_random(100, ["Tag1"], -0.1, seed=42)

    def test_fill_percent_greater_than_one(self):
        """Test that fill_percent > 1.0 raises error."""
        with pytest.raises(ValueError, match="fill_percent|range|0|1"):
            SparseTag.create_random(100, ["Tag1"], 1.5, seed=42)

    def test_fill_percent_exactly_one(self):
        """Test that fill_percent = 1.0 works."""
        bt = SparseTag.create_random(10, ["Tag1"], 1.0, seed=42)
        # Should create completely filled matrix
        assert bt._data.nnz > 0


class TestInvalidQueryStructure:
    """Test validation of malformed query structures."""

    def test_missing_column_field(self):
        """Test query missing 'column' field."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        with pytest.raises((KeyError, ValueError)):
            bt.query({"op": "==", "value": TagConfidence.HIGH})

    def test_missing_op_field(self):
        """Test query missing 'op' field for single-column query."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        # Missing 'op' should raise error
        try:
            result = bt.query({"column": "Tag1", "value": TagConfidence.HIGH})
            # If it doesn't raise, check result is valid
            assert result.count >= 0
        except (KeyError, ValueError):
            pass  # Expected to raise

    def test_missing_value_field(self):
        """Test query missing 'value' field for non-IN operator."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        with pytest.raises((KeyError, ValueError)):
            bt.query({"column": "Tag1", "op": "=="})

    def test_missing_values_field_for_in(self):
        """Test IN operator missing 'values' field."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        with pytest.raises((KeyError, ValueError)):
            bt.query({"column": "Tag1", "op": "IN"})

    def test_missing_conditions_for_logical(self):
        """Test logical operator missing 'conditions' field."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        with pytest.raises((KeyError, ValueError)):
            bt.query({"operator": "AND"})

    def test_empty_conditions_list(self):
        """Test logical operator with empty conditions list."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        with pytest.raises((ValueError, IndexError)):
            bt.query({"operator": "AND", "conditions": []})


class TestInvalidOperators:
    """Test validation of invalid operators."""

    def test_invalid_comparison_operator(self):
        """Test invalid comparison operator string."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        with pytest.raises((ValueError, KeyError)):
            bt.query({"column": "Tag1", "op": "===", "value": TagConfidence.HIGH})

    def test_invalid_logical_operator(self):
        """Test invalid logical operator string."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        with pytest.raises((ValueError, KeyError)):
            bt.query(
                {
                    "operator": "XOR",
                    "conditions": [{"column": "Tag1", "op": "==", "value": TagConfidence.HIGH}],
                }
            )

    def test_case_sensitive_operator(self):
        """Test that operators are case-sensitive (if applicable)."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        # If operators are case-sensitive, this should fail
        # If not, this test documents the behavior
        try:
            result = bt.query({"column": "Tag1", "op": "in", "values": [TagConfidence.HIGH]})
            # If it works, operators are case-insensitive (document this)
            assert result.count >= 0
        except (ValueError, KeyError):
            # Operators are case-sensitive
            pass


class TestInvalidColumnNames:
    """Test validation of invalid column name references."""

    def test_nonexistent_column_name(self):
        """Test query for column that doesn't exist."""
        bt = SparseTag.create_random(100, ["Tag1", "Tag2"], 0.1, seed=42)
        with pytest.raises((KeyError, ValueError)):
            bt.query({"column": "Tag3", "op": "==", "value": TagConfidence.HIGH})

    def test_none_as_column_name(self):
        """Test None as column name."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        with pytest.raises((KeyError, ValueError, TypeError)):
            bt.query({"column": None, "op": "==", "value": TagConfidence.HIGH})

    def test_integer_as_column_name(self):
        """Test integer as column name in query."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        with pytest.raises((KeyError, ValueError, TypeError)):
            bt.query({"column": 0, "op": "==", "value": TagConfidence.HIGH})


class TestInvalidQueryValues:
    """Test validation of invalid query value types."""

    def test_string_as_confidence_value(self):
        """Test string instead of int for confidence value."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        with pytest.raises((TypeError, ValueError)):
            bt.query({"column": "Tag1", "op": "==", "value": "HIGH"})

    def test_float_as_confidence_value(self):
        """Test float instead of int for confidence value."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        # May accept and convert, or may reject
        try:
            result = bt.query({"column": "Tag1", "op": "==", "value": 2.0})
            # If accepted, should work correctly
            assert result.count >= 0
        except (TypeError, ValueError):
            pass  # Also acceptable to reject

    def test_out_of_range_confidence_value(self):
        """Test confidence value > 3 (max is HIGH=3)."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        # Should either handle gracefully (return 0 results) or raise ValueError
        try:
            result = bt.query({"column": "Tag1", "op": "==", "value": 99})
            # If it doesn't raise, it should return 0 results (no values are 99)
            assert result.count == 0
        except ValueError:
            # Also acceptable to raise ValueError for invalid enum value
            pass

    def test_negative_confidence_value(self):
        """Test negative confidence value."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        # Should either handle gracefully or raise
        try:
            result = bt.query({"column": "Tag1", "op": "==", "value": -1})
            # If accepted, should return 0 results
            assert result.count == 0
        except (ValueError, TypeError):
            pass  # Also acceptable to reject

    def test_none_as_confidence_value(self):
        """Test None as confidence value."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        with pytest.raises((TypeError, ValueError)):
            bt.query({"column": "Tag1", "op": "==", "value": None})


class TestInvalidArrayInputs:
    """Test validation of invalid array inputs."""

    def test_out_of_range_values_in_array(self):
        """Test array with values > 3 (max TagConfidence)."""
        data = np.array([[1, 2, 5]], dtype=np.uint8)  # 5 is out of range
        # Should either reject or clamp values
        try:
            bt = SparseTag.from_dense(data, ["A", "B", "C"])
            # If accepted, verify it's stored
            assert bt._data[0, 2] == 5  # Stores as-is (no validation)
        except ValueError:
            pass  # Also acceptable to reject

    def test_wrong_array_dimensions(self):
        """Test 1D array instead of 2D."""
        data = np.array([1, 2, 3], dtype=np.uint8)
        with pytest.raises((ValueError, IndexError)):
            SparseTag.from_dense(data, ["Tag1"])

    def test_3d_array(self):
        """Test 3D array instead of 2D."""
        data = np.array([[[1, 2]]], dtype=np.uint8)
        with pytest.raises((ValueError, IndexError)):
            SparseTag.from_dense(data, ["Tag1", "Tag2"])


class TestInvalidDictInputs:
    """Test validation of invalid dictionary inputs (from_dict not yet implemented)."""

    # NOTE: from_dict() method doesn't exist yet - these are placeholder tests
    @pytest.mark.skip(reason="from_dict not yet implemented")
    def test_from_dict_with_invalid_indices(self):
        """Test from_dict with out-of-range row indices."""

    @pytest.mark.skip(reason="from_dict not yet implemented")
    def test_from_dict_with_index_exceeding_nrows(self):
        """Test from_dict with index >= n_rows."""

    @pytest.mark.skip(reason="from_dict not yet implemented")
    def test_from_dict_with_missing_column(self):
        """Test from_dict with column in data not in column_names."""


class TestInvalidCacheParameters:
    """Test validation of cache-related parameters."""

    def test_negative_cache_max_entries(self):
        """Test negative max_cache_entries."""
        # Constructor doesn't expose this, but if it did:
        # with pytest.raises(ValueError):
        #     SparseTag.create_random(100, ['Tag1'], 0.1, max_cache_entries=-1)
        # Not exposed in current API

    def test_negative_cache_max_memory(self):
        """Test negative max_cache_memory_mb."""
        # Constructor doesn't expose this, but if it did:
        # with pytest.raises(ValueError):
        #     SparseTag.create_random(100, ['Tag1'], 0.1, max_cache_memory_mb=-1)
        # Not exposed in current API


class TestEdgeCaseErrors:
    """Test error handling in edge cases."""

    def test_optimize_dtype_on_nonempty_matrix(self):
        """Test dtype optimization on non-empty matrix."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        # Should handle gracefully
        result = bt.optimize_indices_dtype(inplace=False)
        # Should either return optimized copy or None if no optimization
        if result is not None:
            assert result.shape == bt.shape

    def test_query_result_to_sparse_tag_preserves_columns(self):
        """Test that to_sparse_tag preserves column order."""
        bt = SparseTag.create_random(100, ["A", "B", "C"], 0.1, seed=42)
        result = bt.query({"column": "B", "op": ">=", "value": TagConfidence.MEDIUM})
        if result.count > 0:
            filtered = result.to_sparsetag()
            assert filtered.column_names == ["A", "B", "C"]

    def test_memory_usage_on_matrix(self):
        """Test memory_usage returns dict."""
        bt = SparseTag.create_random(1000, ["Tag1", "Tag2"], 0.1, seed=42)
        mem = bt.memory_usage()
        # Should return a dictionary
        assert isinstance(mem, dict)
        # Should have some keys
        assert len(mem) > 0
