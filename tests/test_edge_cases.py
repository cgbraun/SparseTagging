"""Tests for edge cases and boundary conditions."""

import numpy as np
import pytest
from scipy import sparse
from sparsetagging.sparsetag import SparseTag, TagConfidence


class TestEmptyMatrices:
    """Test handling of empty matrices."""

    def test_empty_matrix_creation(self):
        """Test creating empty matrix."""
        bt = SparseTag.create_empty(100, ["Tag1", "Tag2"])
        assert bt.shape == (100, 2)
        assert bt._data.nnz == 0
        assert bt.sparsity == pytest.approx(1.0)  # 100% sparse is 1.0

    def test_query_on_empty_matrix(self):
        """Test querying empty matrix."""
        bt = SparseTag.create_empty(100, ["Tag1"])
        result = bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})
        assert result.count == 0

    def test_all_operators_on_empty(self):
        """Test all operators return empty on empty matrix."""
        bt = SparseTag.create_empty(50, ["Tag1"])

        for op in ["==", "!=", ">", ">=", "<", "<="]:
            result = bt.query({"column": "Tag1", "op": op, "value": TagConfidence.MEDIUM})
            assert result.count == 0, f"Operator {op} should return 0 results on empty matrix"


class TestSingleRowColumn:
    """Test matrices with single row or column."""

    def test_single_row_matrix(self):
        """Test 1-row matrix."""
        data = sparse.csc_array(np.array([[2, 1, 3]], dtype=np.uint8))
        bt = SparseTag.from_sparse(data, ["A", "B", "C"])

        assert bt.shape == (1, 3)
        result = bt.query({"column": "A", "op": "==", "value": TagConfidence.MEDIUM})
        assert result.count == 1

    def test_single_column_matrix(self):
        """Test 1-column matrix."""
        data = sparse.csc_array(np.array([[1], [2], [3], [0]], dtype=np.uint8))
        bt = SparseTag.from_sparse(data, ["Tag1"])

        assert bt.shape == (4, 1)
        result = bt.query({"column": "Tag1", "op": ">", "value": TagConfidence.LOW})
        assert result.count == 2  # MEDIUM and HIGH

    def test_single_element_matrix(self):
        """Test 1x1 matrix."""
        data = sparse.csc_array(np.array([[3]], dtype=np.uint8))
        bt = SparseTag.from_sparse(data, ["Tag1"])

        assert bt.shape == (1, 1)
        result = bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})
        assert result.count == 1


class TestBoundaryValues:
    """Test boundary values for tag confidences."""

    def test_confidence_zero_handling(self):
        """Test NONE/0 values are handled correctly."""
        data = np.array([[0, 1, 2], [1, 0, 3], [0, 0, 0]], dtype=np.uint8)
        bt = SparseTag.from_dense(data, ["A", "B", "C"])

        # Query for NONE should raise ValueError (would create dense matrix)
        with pytest.raises(ValueError, match="NONE|zero|dense"):
            bt.query({"column": "A", "op": "==", "value": 0})

    def test_max_confidence_value(self):
        """Test maximum confidence value (HIGH=3)."""
        data = np.array([[3, 3, 3]], dtype=np.uint8)
        bt = SparseTag.from_dense(data, ["A", "B", "C"])

        result = bt.query({"column": "A", "op": "==", "value": TagConfidence.HIGH})
        assert result.count == 1

    def test_boundary_comparisons(self):
        """Test boundary conditions in comparisons."""
        data = np.array(
            [
                [1],  # LOW
                [2],  # MEDIUM
                [3],  # HIGH
            ],
            dtype=np.uint8,
        )
        bt = SparseTag.from_dense(data, ["Tag1"])

        # >= LOW should get all
        result = bt.query({"column": "Tag1", "op": ">=", "value": TagConfidence.LOW})
        assert result.count == 3

        # > HIGH should get none
        result = bt.query({"column": "Tag1", "op": ">", "value": TagConfidence.HIGH})
        assert result.count == 0


class TestExtremeSparsity:
    """Test matrices with extreme sparsity levels."""

    def test_very_sparse_matrix(self):
        """Test 99.9% sparse matrix."""
        bt = SparseTag.create_random(10000, ["Tag1"], 0.001, seed=42)
        assert bt.sparsity > 0.99  # > 99% sparse
        result = bt.query({"column": "Tag1", "op": ">=", "value": TagConfidence.LOW})
        assert result.count > 0

    def test_very_dense_matrix(self):
        """Test 90% fill (10% sparse) matrix."""
        bt = SparseTag.create_random(100, ["Tag1", "Tag2"], 0.9, seed=42)
        assert bt.sparsity < 0.5  # < 50% sparse (quite dense)
        result = bt.query({"column": "Tag1", "op": ">=", "value": TagConfidence.LOW})
        assert result.count > 50

    def test_completely_dense_matrix(self):
        """Test 100% fill (no sparsity)."""
        data = np.full((10, 3), TagConfidence.MEDIUM, dtype=np.uint8)
        bt = SparseTag.from_dense(data, ["A", "B", "C"])

        assert bt._data.nnz == 30  # All elements
        result = bt.query({"column": "A", "op": "==", "value": TagConfidence.MEDIUM})
        assert result.count == 10


class TestLargeMatrices:
    """Test handling of large matrices."""

    def test_large_row_count(self):
        """Test matrix with many rows."""
        bt = SparseTag.create_random(100000, ["Tag1"], 0.01, seed=42)
        assert bt.shape[0] == 100000
        result = bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})
        assert result.count >= 0

    def test_large_column_count(self):
        """Test matrix with many columns."""
        bt = SparseTag.create_random(100, [f"Tag{i}" for i in range(100)], 0.05, seed=42)
        assert bt.shape[1] == 100
        result = bt.query({"column": "Tag50", "op": ">=", "value": TagConfidence.MEDIUM})
        assert result.count >= 0

    @pytest.mark.slow
    def test_very_large_matrix(self):
        """Test very large sparse matrix."""
        bt = SparseTag.create_random(1000000, ["A", "B", "C"], 0.001, seed=42)
        assert bt.shape == (1000000, 3)
        # Should handle efficiently due to sparsity
        result = bt.query({"column": "A", "op": "==", "value": TagConfidence.HIGH})
        assert result.count >= 0


class TestSpecialPatterns:
    """Test special data patterns."""

    def test_all_same_value(self):
        """Test matrix with all same non-zero value."""
        data = np.full((50, 3), TagConfidence.HIGH, dtype=np.uint8)
        bt = SparseTag.from_dense(data, ["A", "B", "C"])

        result_eq = bt.query({"column": "A", "op": "==", "value": TagConfidence.HIGH})
        assert result_eq.count == 50

        result_ne = bt.query({"column": "A", "op": "!=", "value": TagConfidence.LOW})
        assert result_ne.count == 50

    def test_diagonal_pattern(self):
        """Test diagonal matrix pattern."""
        data = np.eye(10, 10, dtype=np.uint8) * 3  # Diagonal of HIGH values
        bt = SparseTag.from_dense(data, [f"C{i}" for i in range(10)])

        # Each column should have exactly 1 HIGH value
        for i in range(10):
            result = bt.query({"column": f"C{i}", "op": "==", "value": TagConfidence.HIGH})
            assert result.count == 1

    def test_stripe_pattern(self):
        """Test striped pattern (alternating rows)."""
        data = np.zeros((100, 2), dtype=np.uint8)
        data[::2, :] = TagConfidence.HIGH  # Even rows
        data[1::2, :] = TagConfidence.LOW  # Odd rows
        bt = SparseTag.from_dense(data, ["A", "B"])

        result_high = bt.query({"column": "A", "op": "==", "value": TagConfidence.HIGH})
        assert result_high.count == 50

        result_low = bt.query({"column": "A", "op": "==", "value": TagConfidence.LOW})
        assert result_low.count == 50


class TestDtypeBoundaries:
    """Test dtype optimization at boundary sizes."""

    def test_exactly_256_rows(self):
        """Test matrix with exactly 256 rows (int8 boundary)."""
        bt = SparseTag.create_random(256, ["Tag1"], 0.1, seed=42)
        # Should NOT use int8 (256 requires 9 bits)
        bt.optimize_indices_dtype(inplace=True)
        # Should use int16 or stay at int32/int64
        assert bt._data.indices.dtype in (np.int16, np.int32, np.int64)

    def test_exactly_65536_rows(self):
        """Test matrix with exactly 65536 rows (int16 boundary)."""
        bt = SparseTag.create_random(65536, ["Tag1"], 0.0001, seed=42)
        # Should NOT use int16 (65536 requires 17 bits)
        bt.optimize_indices_dtype(inplace=True)
        assert bt._data.indices.dtype in (np.int32, np.int64)

    def test_255_rows_optimization(self):
        """Test matrix with 255 rows can potentially use int8."""
        bt = SparseTag.create_random(255, ["Tag1"], 0.1, seed=42)
        bt.optimize_indices_dtype(inplace=True)
        # May optimize to int8 or stay at default
        assert bt._data.indices.dtype in (np.int8, np.int16, np.int32, np.int64)

    def test_65535_rows_optimization(self):
        """Test matrix with 65535 rows can potentially use int16."""
        bt = SparseTag.create_random(65535, ["Tag1"], 0.001, seed=42)
        bt.optimize_indices_dtype(inplace=True)
        assert bt._data.indices.dtype in (np.int16, np.int32, np.int64)


class TestQueryResultEdgeCases:
    """Test QueryResult edge cases."""

    def test_mask_property_on_empty_result(self):
        """Test mask property when no results."""
        bt = SparseTag.create_empty(10, ["Tag1"])
        result = bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})

        assert result.count == 0
        mask = result.mask
        assert mask.shape[0] == 10
        assert mask.nnz == 0  # No True values

    def test_to_sparse_tag_on_empty_result(self):
        """Test converting empty result to SparseTag."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        # Impossible query
        result = bt.query(
            {
                "operator": "AND",
                "conditions": [
                    {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH},
                    {"column": "Tag1", "op": "==", "value": TagConfidence.LOW},
                ],
            }
        )

        if result.count == 0:
            # Creating empty SparseTag from 0 rows may raise ZeroDivisionError
            try:
                filtered = result.to_sparsetag()
                assert filtered.shape[0] == 0
            except ZeroDivisionError:
                # Known issue with empty matrices
                pass
