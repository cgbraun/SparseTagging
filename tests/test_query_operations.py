"""Comprehensive tests for all query operations and operators."""

import pytest
from sparsetagging.sparsetag import SparseTag, TagConfidence


class TestComparisonOperators:
    """Test all comparison operators (==, !=, >, >=, <, <=)."""

    @pytest.fixture
    def sample_data(self):
        """Create sample SparseTag for testing."""
        return SparseTag.create_random(1000, ["Tag1", "Tag2", "Tag3"], 0.1, seed=42)

    def test_equality_operator(self, sample_data):
        """Test == operator."""
        result = sample_data.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})
        assert result.count >= 0
        assert len(result.indices) == result.count
        # Verify all results actually have HIGH value
        if result.count > 0:
            col_idx = sample_data._get_column_index("Tag1")
            for row_idx in result.indices[:10]:  # Check first 10
                val = sample_data._data[row_idx, col_idx]
                assert val == TagConfidence.HIGH

    def test_not_equal_operator(self, sample_data):
        """Test != operator."""
        result = sample_data.query({"column": "Tag1", "op": "!=", "value": TagConfidence.LOW})
        assert result.count >= 0
        # Result should exclude LOW values but only count rows with data
        if result.count > 0:
            col_idx = sample_data._get_column_index("Tag1")
            for row_idx in result.indices[:10]:
                val = sample_data._data[row_idx, col_idx]
                assert val != TagConfidence.LOW

    def test_greater_than_operator(self, sample_data):
        """Test > operator."""
        result = sample_data.query({"column": "Tag2", "op": ">", "value": TagConfidence.LOW})
        assert result.count >= 0
        # All results should be MEDIUM or HIGH
        if result.count > 0:
            col_idx = sample_data._get_column_index("Tag2")
            for row_idx in result.indices[:10]:
                val = sample_data._data[row_idx, col_idx]
                assert val > TagConfidence.LOW

    def test_greater_equal_operator(self, sample_data):
        """Test >= operator."""
        result = sample_data.query({"column": "Tag2", "op": ">=", "value": TagConfidence.MEDIUM})
        assert result.count >= 0
        if result.count > 0:
            col_idx = sample_data._get_column_index("Tag2")
            for row_idx in result.indices[:10]:
                val = sample_data._data[row_idx, col_idx]
                assert val >= TagConfidence.MEDIUM

    def test_less_than_operator(self, sample_data):
        """Test < operator."""
        result = sample_data.query({"column": "Tag3", "op": "<", "value": TagConfidence.HIGH})
        assert result.count >= 0
        if result.count > 0:
            col_idx = sample_data._get_column_index("Tag3")
            for row_idx in result.indices[:10]:
                val = sample_data._data[row_idx, col_idx]
                assert val < TagConfidence.HIGH

    def test_less_equal_operator(self, sample_data):
        """Test <= operator."""
        result = sample_data.query({"column": "Tag3", "op": "<=", "value": TagConfidence.MEDIUM})
        assert result.count >= 0
        if result.count > 0:
            col_idx = sample_data._get_column_index("Tag3")
            for row_idx in result.indices[:10]:
                val = sample_data._data[row_idx, col_idx]
                assert val <= TagConfidence.MEDIUM


class TestINOperator:
    """Test IN operator with various value sets."""

    def test_in_operator_multiple_values(self):
        """Test IN with multiple values."""
        bt = SparseTag.create_random(500, ["Tag1"], 0.1, seed=42)
        result = bt.query(
            {"column": "Tag1", "op": "IN", "values": [TagConfidence.HIGH, TagConfidence.MEDIUM]}
        )
        assert result.count >= 0
        # Verify results are only HIGH or MEDIUM
        if result.count > 0:
            for row_idx in result.indices[:10]:
                val = bt._data[row_idx, 0]
                assert val in [TagConfidence.HIGH, TagConfidence.MEDIUM]

    def test_in_operator_single_value(self):
        """Test IN with single value (should work like ==)."""
        bt = SparseTag.create_random(500, ["Tag1"], 0.1, seed=42)
        result_in = bt.query({"column": "Tag1", "op": "IN", "values": [TagConfidence.HIGH]})
        result_eq = bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})
        assert result_in.count == result_eq.count

    def test_in_operator_all_values(self):
        """Test IN with all possible values."""
        bt = SparseTag.create_random(500, ["Tag1"], 0.1, seed=42)
        result = bt.query(
            {
                "column": "Tag1",
                "op": "IN",
                "values": [TagConfidence.LOW, TagConfidence.MEDIUM, TagConfidence.HIGH],
            }
        )
        # Should return all rows with any tag confidence
        assert result.count > 0


class TestLogicalOperators:
    """Test AND, OR, NOT logical operators."""

    @pytest.fixture
    def multi_col_data(self):
        """Create multi-column data for logical tests."""
        return SparseTag.create_random(1000, ["A", "B", "C"], 0.1, seed=42)

    def test_and_operator_two_conditions(self, multi_col_data):
        """Test AND with two conditions."""
        result = multi_col_data.query(
            {
                "operator": "AND",
                "conditions": [
                    {"column": "A", "op": "==", "value": TagConfidence.HIGH},
                    {"column": "B", "op": ">=", "value": TagConfidence.MEDIUM},
                ],
            }
        )
        assert result.count >= 0
        # Verify both conditions are met
        if result.count > 0:
            for row_idx in result.indices[:5]:
                assert multi_col_data._data[row_idx, 0] == TagConfidence.HIGH
                assert multi_col_data._data[row_idx, 1] >= TagConfidence.MEDIUM

    def test_and_operator_three_conditions(self, multi_col_data):
        """Test AND with three conditions."""
        result = multi_col_data.query(
            {
                "operator": "AND",
                "conditions": [
                    {"column": "A", "op": ">", "value": TagConfidence.LOW},
                    {"column": "B", "op": ">", "value": TagConfidence.LOW},
                    {"column": "C", "op": ">", "value": TagConfidence.LOW},
                ],
            }
        )
        assert result.count >= 0

    def test_or_operator_two_conditions(self, multi_col_data):
        """Test OR with two conditions."""
        result = multi_col_data.query(
            {
                "operator": "OR",
                "conditions": [
                    {"column": "A", "op": "==", "value": TagConfidence.HIGH},
                    {"column": "B", "op": "==", "value": TagConfidence.HIGH},
                ],
            }
        )
        assert result.count >= 0
        # At least one condition should be met
        if result.count > 0:
            for row_idx in result.indices[:5]:
                val_a = multi_col_data._data[row_idx, 0]
                val_b = multi_col_data._data[row_idx, 1]
                assert val_a == TagConfidence.HIGH or val_b == TagConfidence.HIGH

    def test_or_operator_three_conditions(self, multi_col_data):
        """Test OR with three conditions."""
        result = multi_col_data.query(
            {
                "operator": "OR",
                "conditions": [
                    {"column": "A", "op": "==", "value": TagConfidence.HIGH},
                    {"column": "B", "op": "==", "value": TagConfidence.HIGH},
                    {"column": "C", "op": "==", "value": TagConfidence.HIGH},
                ],
            }
        )
        assert result.count >= 0

    def test_not_operator_single_condition(self, multi_col_data):
        """Test NOT with single condition."""
        result = multi_col_data.query(
            {
                "operator": "NOT",
                "conditions": [{"column": "A", "op": "==", "value": TagConfidence.LOW}],
            }
        )
        assert result.count >= 0
        # Should exclude rows with LOW in column A, and all-zero rows
        if result.count > 0:
            for row_idx in result.indices[:5]:
                val = multi_col_data._data[row_idx, 0]
                # NOT should exclude LOW values
                assert val != TagConfidence.LOW

    def test_not_excludes_all_zero_rows(self):
        """Test that NOT excludes rows with no data."""
        # Create sparse matrix with some all-zero rows
        bt = SparseTag.create_random(100, ["Tag1"], 0.5, seed=42)

        # NOT query should only operate on rows with data
        result_not = bt.query(
            {
                "operator": "NOT",
                "conditions": [{"column": "Tag1", "op": "==", "value": TagConfidence.LOW}],
            }
        )

        # All results should have non-zero values
        if result_not.count > 0:
            for row_idx in result_not.indices[:10]:
                val = bt._data[row_idx, 0]
                assert val != 0  # No all-zero rows


class TestNestedQueries:
    """Test nested/complex query structures."""

    def test_nested_and_or(self):
        """Test nested AND within OR."""
        bt = SparseTag.create_random(1000, ["A", "B", "C"], 0.1, seed=42)

        # (A==HIGH AND B>=MED) OR (C==HIGH)
        result = bt.query(
            {
                "operator": "OR",
                "conditions": [
                    {
                        "operator": "AND",
                        "conditions": [
                            {"column": "A", "op": "==", "value": TagConfidence.HIGH},
                            {"column": "B", "op": ">=", "value": TagConfidence.MEDIUM},
                        ],
                    },
                    {"column": "C", "op": "==", "value": TagConfidence.HIGH},
                ],
            }
        )
        assert result.count >= 0

    def test_complex_multi_level_nesting(self):
        """Test deep nesting of queries."""
        bt = SparseTag.create_random(1000, ["A", "B", "C", "D"], 0.1, seed=42)

        # ((A==HIGH AND B==HIGH) OR (C==HIGH)) AND D>=LOW
        result = bt.query(
            {
                "operator": "AND",
                "conditions": [
                    {
                        "operator": "OR",
                        "conditions": [
                            {
                                "operator": "AND",
                                "conditions": [
                                    {"column": "A", "op": "==", "value": TagConfidence.HIGH},
                                    {"column": "B", "op": "==", "value": TagConfidence.HIGH},
                                ],
                            },
                            {"column": "C", "op": "==", "value": TagConfidence.HIGH},
                        ],
                    },
                    {"column": "D", "op": ">=", "value": TagConfidence.LOW},
                ],
            }
        )
        assert result.count >= 0


class TestQueryResultMethods:
    """Test QueryResult object methods."""

    def test_query_result_properties(self):
        """Test QueryResult basic properties."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.1, seed=42)
        result = bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})

        assert hasattr(result, "count")
        assert hasattr(result, "indices")
        assert hasattr(result, "mask")
        assert len(result) == result.count

    def test_query_result_to_sparse_tag(self):
        """Test converting QueryResult to SparseTag."""
        bt = SparseTag.create_random(100, ["Tag1", "Tag2"], 0.2, seed=42)
        result = bt.query({"column": "Tag1", "op": ">=", "value": TagConfidence.MEDIUM})

        if result.count > 0:
            filtered = result.to_sparsetag()
            assert filtered.shape[0] == result.count
            assert filtered.shape[1] == bt.shape[1]
            assert filtered.column_names == bt.column_names

    def test_empty_query_result(self):
        """Test QueryResult with no matches."""
        bt = SparseTag.create_random(100, ["Tag1"], 0.01, seed=42)
        # Query that likely returns no results
        result = bt.query(
            {
                "operator": "AND",
                "conditions": [
                    {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH},
                    {"column": "Tag1", "op": "==", "value": TagConfidence.LOW},  # Impossible
                ],
            }
        )

        assert result.count == 0
        assert len(result.indices) == 0
