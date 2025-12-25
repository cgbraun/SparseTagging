"""Integration tests for end-to-end workflows."""

import numpy as np
import pytest
from sparsetagging.sparsetag import SparseTag, TagConfidence


class TestBasicWorkflows:
    """Test basic end-to-end workflows."""

    def test_create_query_filter_workflow(self):
        """Test: Create → Query → Filter → Extract workflow."""
        # Create data
        bt = SparseTag.create_random(1000, ["Tag1", "Tag2", "Tag3"], 0.1, seed=42)
        assert bt.shape == (1000, 3)

        # Query for high confidence tags
        result = bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})
        assert result.count >= 0

        # Filter to new SparseTag
        if result.count > 0:
            filtered = result.to_sparsetag()
            assert filtered.shape[0] == result.count
            assert filtered.shape[1] == 3
            assert filtered.column_names == ["Tag1", "Tag2", "Tag3"]

            # All rows in filtered should have Tag1 == HIGH
            for i in range(min(10, filtered.shape[0])):
                assert filtered._data[i, 0] == TagConfidence.HIGH

    def test_multi_stage_filtering(self):
        """Test: Multiple query stages to progressively filter data."""
        bt = SparseTag.create_random(1000, ["A", "B", "C"], 0.2, seed=42)

        # Stage 1: Filter by column A
        result1 = bt.query({"column": "A", "op": ">=", "value": TagConfidence.MEDIUM})

        if result1.count > 0:
            filtered1 = result1.to_sparsetag()

            # Stage 2: Filter result by column B
            result2 = filtered1.query({"column": "B", "op": "==", "value": TagConfidence.HIGH})

            # Result should be subset of first filter
            assert result2.count <= result1.count

    def test_create_optimize_query_workflow(self):
        """Test: Create → Optimize → Query workflow."""
        # Create small matrix
        bt = SparseTag.create_random(200, ["Tag1", "Tag2"], 0.1, seed=42)

        # Optimize indices
        bt.optimize_indices_dtype(inplace=True)

        # Query should still work correctly
        result = bt.query({"column": "Tag1", "op": ">=", "value": TagConfidence.LOW})
        assert result.count >= 0

        # Verify data integrity
        assert bt._data.nnz > 0


class TestCachingWorkflows:
    """Test workflows involving caching."""

    def test_repeated_query_workflow(self):
        """Test workflow with repeated queries (cache hits)."""
        bt = SparseTag.create_random(1000, ["Tag1"], 0.1, seed=42, enable_cache=True)

        query = {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH}

        # First query (cache miss)
        result1 = bt.query(query)
        stats1 = bt.cache_stats()
        assert stats1["misses"] >= 1

        # Second query (cache hit)
        result2 = bt.query(query)
        stats2 = bt.cache_stats()
        assert stats2["hits"] >= 1

        # Results should be identical
        assert result1.count == result2.count
        assert np.array_equal(result1.indices, result2.indices)

    def test_query_pattern_workflow(self):
        """Test realistic query pattern with partial cache hits."""
        bt = SparseTag.create_random(1000, ["A", "B"], 0.1, seed=42, enable_cache=True)

        queries = [
            {"column": "A", "op": "==", "value": TagConfidence.HIGH},
            {"column": "A", "op": "==", "value": TagConfidence.MEDIUM},
            {"column": "A", "op": "==", "value": TagConfidence.HIGH},  # Repeat
            {"column": "B", "op": ">=", "value": TagConfidence.MEDIUM},
            {"column": "A", "op": "==", "value": TagConfidence.HIGH},  # Repeat again
        ]

        for query in queries:
            bt.query(query)

        stats = bt.cache_stats()
        # Should have cache hits from repeated queries
        assert stats["hits"] >= 2

    def test_cache_clear_workflow(self):
        """Test workflow with cache clearing."""
        bt = SparseTag.create_random(500, ["Tag1"], 0.1, seed=42, enable_cache=True)

        # Populate cache
        bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})
        assert bt.cache_stats()["size_entries"] > 0

        # Clear cache
        bt.clear_cache()
        assert bt.cache_stats()["size_entries"] == 0

        # Query again (should miss cache)
        bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})
        stats = bt.cache_stats()
        assert stats["size_entries"] >= 1


class TestComplexQueryWorkflows:
    """Test workflows with complex nested queries."""

    def test_progressive_and_refinement(self):
        """Test progressively refining with AND conditions."""
        bt = SparseTag.create_random(1000, ["A", "B", "C", "D"], 0.15, seed=42)

        # Start with single condition
        result1 = bt.query({"column": "A", "op": ">=", "value": TagConfidence.MEDIUM})
        count1 = result1.count

        # Add second condition
        result2 = bt.query(
            {
                "operator": "AND",
                "conditions": [
                    {"column": "A", "op": ">=", "value": TagConfidence.MEDIUM},
                    {"column": "B", "op": ">=", "value": TagConfidence.MEDIUM},
                ],
            }
        )
        count2 = result2.count

        # Add third condition
        result3 = bt.query(
            {
                "operator": "AND",
                "conditions": [
                    {"column": "A", "op": ">=", "value": TagConfidence.MEDIUM},
                    {"column": "B", "op": ">=", "value": TagConfidence.MEDIUM},
                    {"column": "C", "op": ">=", "value": TagConfidence.MEDIUM},
                ],
            }
        )
        count3 = result3.count

        # Each refinement should reduce or maintain count
        assert count2 <= count1
        assert count3 <= count2

    def test_or_expansion_workflow(self):
        """Test expanding results with OR conditions."""
        bt = SparseTag.create_random(1000, ["A", "B"], 0.1, seed=42)

        # Single column
        result1 = bt.query({"column": "A", "op": "==", "value": TagConfidence.HIGH})
        count1 = result1.count

        # OR with second column (should have >= results)
        result2 = bt.query(
            {
                "operator": "OR",
                "conditions": [
                    {"column": "A", "op": "==", "value": TagConfidence.HIGH},
                    {"column": "B", "op": "==", "value": TagConfidence.HIGH},
                ],
            }
        )
        count2 = result2.count

        # OR should have equal or more results
        assert count2 >= count1

    def test_complex_nested_workflow(self):
        """Test complex nested query workflow."""
        bt = SparseTag.create_random(1000, ["A", "B", "C"], 0.15, seed=42)

        # Complex query: (A==HIGH OR B==HIGH) AND C>=MEDIUM
        result = bt.query(
            {
                "operator": "AND",
                "conditions": [
                    {
                        "operator": "OR",
                        "conditions": [
                            {"column": "A", "op": "==", "value": TagConfidence.HIGH},
                            {"column": "B", "op": "==", "value": TagConfidence.HIGH},
                        ],
                    },
                    {"column": "C", "op": ">=", "value": TagConfidence.MEDIUM},
                ],
            }
        )

        assert result.count >= 0

        # Verify results match conditions
        if result.count > 0:
            for idx in result.indices[:5]:
                val_a = bt._data[idx, 0]
                val_b = bt._data[idx, 1]
                val_c = bt._data[idx, 2]

                # Must satisfy: (A==HIGH OR B==HIGH) AND C>=MEDIUM
                assert val_a == TagConfidence.HIGH or val_b == TagConfidence.HIGH
                assert val_c >= TagConfidence.MEDIUM


class TestDataTransformationWorkflows:
    """Test workflows involving data transformations."""

    @pytest.mark.skip(reason="from_dict not yet implemented")
    def test_dict_to_query_workflow(self):
        """Test: Dict → SparseTag → Query workflow (placeholder)."""

    def test_array_to_sparse_workflow(self):
        """Test: Dense array → SparseTag → Sparse operations."""
        # Create dense array
        dense = np.zeros((100, 3), dtype=np.uint8)
        dense[::10, 0] = TagConfidence.HIGH
        dense[::5, 1] = TagConfidence.MEDIUM
        dense[::2, 2] = TagConfidence.LOW

        # Convert to SparseTag
        bt = SparseTag.from_dense(dense, ["A", "B", "C"])

        # Verify sparsity (ratio 0-1, not percentage)
        assert bt.sparsity > 0.5  # > 50% sparse

        # Query
        result = bt.query({"column": "A", "op": "==", "value": TagConfidence.HIGH})
        assert result.count == 10

    def test_sparse_to_filtered_sparse_workflow(self):
        """Test: Sparse → Query → Filtered sparse → Query again."""
        bt = SparseTag.create_random(1000, ["A", "B", "C"], 0.1, seed=42)

        # First filter
        result1 = bt.query({"column": "A", "op": ">=", "value": TagConfidence.MEDIUM})

        if result1.count > 10:
            filtered = result1.to_sparsetag()

            # Second filter on filtered data
            result2 = filtered.query({"column": "B", "op": "==", "value": TagConfidence.HIGH})

            # Both should be valid
            assert result2.count >= 0
            assert result2.count <= result1.count


class TestMemoryOptimizationWorkflows:
    """Test workflows involving memory optimization."""

    def test_create_large_optimize_workflow(self):
        """Test creating large sparse matrix and optimizing."""
        # Create large sparse matrix
        bt = SparseTag.create_random(50000, ["Tag1"], 0.01, seed=42)

        # Optimize
        bt.optimize_indices_dtype(inplace=True)

        # May reduce memory (if < 65K rows and optimization succeeds)

        # Should maintain data integrity
        assert bt._data.nnz > 0
        assert bt.shape[0] == 50000

        # Query should work after optimization
        result = bt.query({"column": "Tag1", "op": "==", "value": TagConfidence.HIGH})
        assert result.count >= 0

    def test_memory_tracking_workflow(self):
        """Test tracking memory through operations."""
        bt = SparseTag.create_random(10000, ["Tag1", "Tag2"], 0.05, seed=42, enable_cache=True)

        # Initial memory
        mem1 = bt.memory_usage()
        assert isinstance(mem1, dict)

        # Populate cache
        for val in [TagConfidence.LOW, TagConfidence.MEDIUM, TagConfidence.HIGH]:
            bt.query({"column": "Tag1", "op": "==", "value": val})

        # Cache should have memory
        stats = bt.cache_stats()
        assert stats["size_bytes"] > 0


class TestRealWorldScenarios:
    """Test realistic real-world usage scenarios."""

    def test_tag_filtering_dashboard_scenario(self):
        """Simulate tag filtering dashboard: multiple filters, caching."""
        # Simulate 10K items with 10 tag columns
        bt = SparseTag.create_random(
            10000, [f"Tag{i}" for i in range(10)], 0.05, seed=42, enable_cache=True
        )

        # User filters by Tag0 = HIGH
        result1 = bt.query({"column": "Tag0", "op": "==", "value": TagConfidence.HIGH})
        count1 = result1.count

        # User adds Tag1 >= MEDIUM
        bt.query(
            {
                "operator": "AND",
                "conditions": [
                    {"column": "Tag0", "op": "==", "value": TagConfidence.HIGH},
                    {"column": "Tag1", "op": ">=", "value": TagConfidence.MEDIUM},
                ],
            }
        )

        # User goes back to first query (cache hit)
        result3 = bt.query({"column": "Tag0", "op": "==", "value": TagConfidence.HIGH})
        count3 = result3.count

        # Third query should match first (cache hit)
        assert count3 == count1

        # Should have cache hits
        stats = bt.cache_stats()
        assert stats["hits"] >= 1

    def test_batch_processing_scenario(self):
        """Simulate batch processing: load, filter, export."""
        # Load data
        bt = SparseTag.create_random(5000, ["Quality", "Relevance", "Safety"], 0.1, seed=42)

        # Filter: High quality AND high relevance
        result = bt.query(
            {
                "operator": "AND",
                "conditions": [
                    {"column": "Quality", "op": ">=", "value": TagConfidence.HIGH},
                    {"column": "Relevance", "op": ">=", "value": TagConfidence.HIGH},
                ],
            }
        )

        # Export filtered subset
        if result.count > 0:
            filtered = result.to_sparsetag()

            # Verify exported data
            assert filtered.shape[0] == result.count
            assert filtered.column_names == ["Quality", "Relevance", "Safety"]

            # All filtered rows should meet criteria
            for i in range(min(10, filtered.shape[0])):
                assert filtered._data[i, 0] >= TagConfidence.HIGH  # Quality
                assert filtered._data[i, 1] >= TagConfidence.HIGH  # Relevance

    def test_incremental_analysis_scenario(self):
        """Simulate incremental analysis: multiple queries building on each other."""
        bt = SparseTag.create_random(2000, ["A", "B", "C", "D"], 0.1, seed=42)

        # Analysis step 1: Find all HIGH in A
        high_a = bt.query({"column": "A", "op": "==", "value": TagConfidence.HIGH})

        # Analysis step 2: Of those, how many have HIGH in B?
        if high_a.count > 0:
            filtered_a = high_a.to_sparsetag()
            high_b = filtered_a.query({"column": "B", "op": "==", "value": TagConfidence.HIGH})

            # Analysis step 3: Of those, how many have HIGH in C?
            if high_b.count > 0:
                filtered_b = high_b.to_sparsetag()
                high_c = filtered_b.query({"column": "C", "op": "==", "value": TagConfidence.HIGH})

                # Should be progressively smaller
                assert high_c.count <= high_b.count
                assert high_b.count <= high_a.count

    @pytest.mark.slow
    def test_large_scale_workflow(self):
        """Test large-scale workflow (100K+ rows)."""
        # Create large dataset
        bt = SparseTag.create_random(
            100000, ["Tag1", "Tag2", "Tag3"], 0.01, seed=42, enable_cache=True
        )

        # Complex query
        result = bt.query(
            {
                "operator": "OR",
                "conditions": [
                    {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH},
                    {
                        "operator": "AND",
                        "conditions": [
                            {"column": "Tag2", "op": ">=", "value": TagConfidence.MEDIUM},
                            {"column": "Tag3", "op": "!=", "value": TagConfidence.LOW},
                        ],
                    },
                ],
            }
        )

        # Should complete efficiently
        assert result.count >= 0

        # Cache should work
        result2 = bt.query(
            {
                "operator": "OR",
                "conditions": [
                    {"column": "Tag1", "op": "==", "value": TagConfidence.HIGH},
                    {
                        "operator": "AND",
                        "conditions": [
                            {"column": "Tag2", "op": ">=", "value": TagConfidence.MEDIUM},
                            {"column": "Tag3", "op": "!=", "value": TagConfidence.LOW},
                        ],
                    },
                ],
            }
        )

        assert result2.count == result.count
        stats = bt.cache_stats()
        assert stats["hits"] >= 1
