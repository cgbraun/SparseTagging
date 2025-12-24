"""Performance regression tests."""
import pytest
import numpy as np
from src.sparsetag import SparseTag, TagConfidence


class TestPerformanceOptimizations:
    """Test performance optimizations work."""

    def test_cache_memory_tracking_is_accurate(self):
        """Incremental tracking matches actual memory."""
        bt = SparseTag.create_random(10000, ['Tag1'], 0.01, seed=42, enable_cache=True)

        # Populate cache
        for val in [TagConfidence.LOW, TagConfidence.MEDIUM, TagConfidence.HIGH]:
            bt.query({'column': 'Tag1', 'op': '==', 'value': val})

        # Get tracked memory
        tracked = bt.cache_stats()['size_bytes']

        # Calculate actual (accessing cache manager's internal cache)
        actual = sum(r.indices.nbytes + 200 for r in bt._cache_manager._cache.values())

        assert tracked == actual

    @pytest.mark.slow
    def test_no_performance_regression(self):
        """Ensure bug fixes don't slow queries."""
        bt = SparseTag.create_random(100000, ['Tag1', 'Tag2'], 0.01, seed=42)

        import time
        query = {'column': 'Tag1', 'op': '==', 'value': TagConfidence.HIGH}

        times = []
        for _ in range(10):
            start = time.perf_counter()
            bt.query(query, use_cache=False)
            times.append(time.perf_counter() - start)

        avg_time = np.mean(times)
        assert avg_time < 0.001, f"Query too slow: {avg_time*1000:.2f}ms (expected <1ms)"
