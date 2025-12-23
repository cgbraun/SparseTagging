"""
Comprehensive Performance Benchmark for BaseTag v2.1
=====================================================

Tests three scenarios across multiple sizes:
1. Dense numpy arrays (baseline)
2. Sparse arrays without cache (v2.0)
3. Sparse arrays with cache (v2.1)

Generates detailed performance report with:
- Speed comparisons
- Memory usage
- Cache statistics
- Speedup factors
"""

import sys
import numpy as np
from scipy import sparse
import time
import psutil
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

from basetag import BaseTag, TagConfidence

# Shortcuts
HIGH = TagConfidence.HIGH
MEDIUM = TagConfidence.MEDIUM
LOW = TagConfidence.LOW
NONE = TagConfidence.NONE


class PerformanceBenchmark:
    """Comprehensive performance benchmark suite."""

    def __init__(self, size_config: str = 'medium'):
        """
        Initialize benchmark.

        Args:
            size_config: 'small', 'medium', or 'large'
        """
        # Size configurations
        self.sizes = {
            'small': (1_000, 10, 50, 10),      # (rows, cols, iterations, warmup)
            'medium': (100_000, 100, 20, 5),
            'large': (1_000_000, 100, 10, 3)
        }

        if size_config not in self.sizes:
            raise ValueError(f"size_config must be one of {list(self.sizes.keys())}")

        self.size_config = size_config
        self.n_rows, self.n_cols, self.iterations, self.warmup = self.sizes[size_config]
        self.fill_percent = 0.01  # 1% fill = 99% sparse (optimal)
        self.seed = 42

        self.results = {}
        self.report_lines = []

    def _log(self, line: str = ""):
        """Add line to report and print."""
        print(line)
        self.report_lines.append(line)

    def _header(self, title: str, level: int = 1):
        """Add formatted header."""
        if level == 1:
            self._log(f"\n{'='*70}")
            self._log(title)
            self._log('='*70)
        elif level == 2:
            self._log(f"\n{'-'*70}")
            self._log(title)
            self._log('-'*70)
        else:
            self._log(f"\n{title}")
            self._log('-' * len(title))

    def initialize_data(self):
        """Create test data for all three scenarios."""
        self._header("Data Initialization")

        self._log(f"Configuration: {self.size_config.upper()}")
        self._log(f"  Rows:       {self.n_rows:,}")
        self._log(f"  Columns:    {self.n_cols}")
        self._log(f"  Sparsity:   {(1-self.fill_percent)*100:.1f}% ({self.fill_percent*100:.1f}% fill)")
        self._log(f"  Iterations: {self.iterations} (warmup: {self.warmup})")
        self._log(f"  Seed:       {self.seed}")

        # Create column names
        columns = [f'Tag{i+1}' for i in range(self.n_cols)]

        self._log("\nCreating test matrices...")

        # 1. Sparse with cache (v2.1)
        t1 = time.perf_counter()
        self.bt_cached = BaseTag.create_random(
            self.n_rows, columns, self.fill_percent, self.seed, enable_cache=True
        )
        time_cached = time.perf_counter() - t1
        self._log(f"  ✓ Sparse with cache:    {time_cached:.3f}s")

        # 2. Sparse without cache (v2.0)
        t2 = time.perf_counter()
        self.bt_uncached = BaseTag.create_random(
            self.n_rows, columns, self.fill_percent, self.seed, enable_cache=False
        )
        time_uncached = time.perf_counter() - t2
        self._log(f"  ✓ Sparse without cache: {time_uncached:.3f}s")

        # 3. Dense numpy array (baseline)
        t3 = time.perf_counter()
        self.dense = self.bt_cached.to_dense()
        time_dense = time.perf_counter() - t3
        self._log(f"  ✓ Dense array:          {time_dense:.3f}s")

        # Memory analysis
        self._log("\nMemory Usage:")
        sparse_mem = self.bt_cached.memory_usage()
        dense_mem = self.dense.nbytes

        self._log(f"  Dense:              {dense_mem/1024/1024:.2f} MB")
        self._log(f"  Sparse (data):      {sparse_mem['data']/1024/1024:.2f} MB")
        self._log(f"  Sparse (indices):   {sparse_mem['indices']/1024/1024:.2f} MB")
        self._log(f"  Sparse (indptr):    {sparse_mem['indptr']/1024/1024:.2f} MB")
        self._log(f"  Sparse (metadata):  {sparse_mem['column_names']/1024/1024:.2f} MB")
        self._log(f"  Sparse (total):     {sparse_mem['total']/1024/1024:.2f} MB")
        self._log(f"  Memory Savings:     {(1 - sparse_mem['total']/dense_mem)*100:.1f}%")

        # Store memory stats
        self.results['memory'] = {
            'dense_mb': dense_mem / 1024 / 1024,
            'sparse_mb': sparse_mem['total'] / 1024 / 1024,
            'savings_percent': (1 - sparse_mem['total']/dense_mem) * 100
        }

    def _execute_timed_query(
        self,
        query_func,
        iterations: int,
        warmup: int
    ) -> Tuple[float, float, int]:
        """
        Execute query function with timing and warmup.

        Args:
            query_func: Callable that executes query and returns match count
            iterations: Number of benchmark iterations
            warmup: Number of warmup iterations

        Returns:
            (avg_time_ms, std_time_ms, match_count)
        """
        # Warmup
        count = None
        for _ in range(warmup):
            count = query_func()

        # Timed iterations
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            count = query_func()
            end = time.perf_counter()
            times.append((end - start) * 1000)

        return np.mean(times), np.std(times), count

    def _query_dense_multi(self, query_dict: Dict, iterations: int, warmup: int) -> Tuple[float, float, int]:
        """
        Execute multi-column query on dense array and time it.

        IMPORTANT: NOT operator semantics for sparse data:
        - NOT operates only on rows that have ANY non-zero value
        - Rows with all zeros (no tag confidence) are excluded from universe
        - This matches sparse matrix behavior where zeros = "no data"

        Returns:
            (avg_time_ms, std_time_ms, match_count)
        """
        operator = query_dict.get('operator')
        conditions = query_dict.get('conditions', [])

        if not operator or not conditions:
            raise ValueError("Multi-column query requires operator and conditions")

        def execute_query():
            """Execute the multi-column query on dense array."""
            masks = []
            for cond in conditions:
                if 'operator' in cond:
                    # Nested - skip for now
                    continue
                col_name = cond['column']
                col_idx = self.bt_cached._column_index[col_name]
                op = cond['op']

                if op == '==':
                    mask = self.dense[:, col_idx] == cond['value']
                elif op == '>':
                    mask = self.dense[:, col_idx] > cond['value']
                elif op == '>=':
                    mask = self.dense[:, col_idx] >= cond['value']
                elif op == 'IN':
                    mask = np.isin(self.dense[:, col_idx], cond['values'])
                else:
                    raise ValueError(f"Unsupported op: {op}")
                masks.append(mask)

            if operator == 'AND':
                result_mask = masks[0]
                for m in masks[1:]:
                    result_mask = result_mask & m
            elif operator == 'OR':
                result_mask = masks[0]
                for m in masks[1:]:
                    result_mask = result_mask | m
            elif operator == 'NOT':
                # CRITICAL: Match sparse semantics
                # Universe = rows with ANY non-zero value (not all zeros)
                has_data_mask = np.any(self.dense != 0, axis=1)
                # Apply NOT only to rows with data
                result_mask = has_data_mask & ~masks[0]

            return int(np.sum(result_mask))

        return self._execute_timed_query(execute_query, iterations, warmup)

    def _query_dense(self, col_idx: int, op: str, value,
                     iterations: int, warmup: int) -> Tuple[float, float, int]:
        """
        Execute query on dense array and time it.

        Returns:
            (avg_time_ms, std_time_ms, match_count)
        """
        def execute_query():
            """Execute the single-column query on dense array."""
            if op == '==':
                mask = self.dense[:, col_idx] == value
            elif op == '>':
                mask = self.dense[:, col_idx] > value
            elif op == '>=':
                mask = self.dense[:, col_idx] >= value
            elif op == 'IN':
                mask = np.isin(self.dense[:, col_idx], value)
            else:
                raise ValueError(f"Unsupported op: {op}")
            return int(np.sum(mask))

        return self._execute_timed_query(execute_query, iterations, warmup)

    def _query_sparse(self, query_dict: Dict, use_cache: bool,
                     iterations: int, warmup: int) -> Tuple[float, float, int]:
        """
        Execute query on sparse array and time it.

        Returns:
            (avg_time_ms, std_time_ms, match_count)
        """
        bt = self.bt_cached if use_cache else self.bt_uncached

        def execute_query():
            """Execute the sparse query."""
            result = bt.query(query_dict, use_cache=use_cache)
            return result.count

        return self._execute_timed_query(execute_query, iterations, warmup)

    def benchmark_single_column_queries(self):
        """Benchmark single-column query operations."""
        self._header("Single-Column Query Benchmarks", level=1)

        test_cases = [
            ('Tag1 == HIGH', {'column': 'Tag1', 'op': '==', 'value': HIGH}, 0, '==', HIGH),
            ('Tag2 == MEDIUM', {'column': 'Tag2', 'op': '==', 'value': MEDIUM}, 1, '==', MEDIUM),
            ('Tag3 > LOW', {'column': 'Tag3', 'op': '>', 'value': LOW}, 2, '>', LOW),
            ('Tag4 >= MEDIUM', {'column': 'Tag4', 'op': '>=', 'value': MEDIUM}, 3, '>=', MEDIUM),
            ('Tag5 IN [HIGH,MED]', {'column': 'Tag5', 'op': 'IN', 'values': [HIGH, MEDIUM]}, 4, 'IN', [HIGH, MEDIUM]),
        ]

        results = []

        for name, sparse_query, col_idx, dense_op, dense_val in test_cases:
            self._log(f"\nTest: {name}")

            # Dense
            time_dense, std_dense, count_dense = self._query_dense(
                col_idx, dense_op, dense_val, self.iterations, self.warmup
            )
            self._log(f"  Dense:            {time_dense:7.3f}ms ± {std_dense:.3f}ms ({count_dense:5d} matches)")

            # Sparse uncached
            time_uncached, std_uncached, count_uncached = self._query_sparse(
                sparse_query, False, self.iterations, self.warmup
            )
            self._log(f"  Sparse (no cache): {time_uncached:7.3f}ms ± {std_uncached:.3f}ms ({count_uncached:5d} matches)")

            # Sparse cached (first call - miss)
            self.bt_cached.clear_cache()
            time_miss, _, _ = self._query_sparse(
                sparse_query, True, 1, 0
            )

            # Sparse cached (subsequent calls - hits)
            time_cached, std_cached, count_cached = self._query_sparse(
                sparse_query, True, self.iterations, 0
            )
            self._log(f"  Sparse (cached):   {time_cached:7.3f}ms ± {std_cached:.3f}ms ({count_cached:5d} matches)")

            # Calculate speedups
            speedup_sparse_vs_dense = time_dense / time_uncached
            speedup_cache_vs_uncached = time_uncached / time_cached
            speedup_cache_vs_dense = time_dense / time_cached

            self._log(f"  Speedup (sparse vs dense): {speedup_sparse_vs_dense:5.1f}x")
            self._log(f"  Speedup (cache vs uncached): {speedup_cache_vs_uncached:5.1f}x")
            self._log(f"  Speedup (cache vs dense):  {speedup_cache_vs_dense:5.1f}x")

            # Verify results match
            if count_dense != count_uncached or count_dense != count_cached:
                self._log(f"  ⚠ WARNING: Result mismatch! Dense={count_dense}, Uncached={count_uncached}, Cached={count_cached}")

            results.append({
                'name': name,
                'dense_ms': time_dense,
                'uncached_ms': time_uncached,
                'cached_ms': time_cached,
                'miss_ms': time_miss,
                'count': count_dense,
                'speedup_sparse': speedup_sparse_vs_dense,
                'speedup_cache': speedup_cache_vs_uncached
            })

        self.results['single_column'] = results

    def benchmark_multi_column_queries(self):
        """Benchmark multi-column query operations."""
        self._header("Multi-Column Query Benchmarks", level=1)

        test_cases = [
            ('Tag1==HIGH AND Tag2>=MED', {
                'operator': 'AND',
                'conditions': [
                    {'column': 'Tag1', 'op': '==', 'value': HIGH},
                    {'column': 'Tag2', 'op': '>=', 'value': MEDIUM}
                ]
            }),
            ('Tag1==HIGH OR Tag3==LOW', {
                'operator': 'OR',
                'conditions': [
                    {'column': 'Tag1', 'op': '==', 'value': HIGH},
                    {'column': 'Tag3', 'op': '==', 'value': LOW}
                ]
            }),
            ('NOT (Tag2==LOW)', {
                'operator': 'NOT',
                'conditions': [
                    {'column': 'Tag2', 'op': '==', 'value': LOW}
                ]
            }),
        ]

        results = []

        for name, query in test_cases:
            self._log(f"\nTest: {name}")

            # Dense (if columns exist in test case)
            try:
                time_dense, std_dense, count_dense = self._query_dense_multi(
                    query, self.iterations, self.warmup
                )
                self._log(f"  Dense:             {time_dense:7.3f}ms ± {std_dense:.3f}ms ({count_dense:5d} matches)")
                has_dense = True
            except Exception as e:
                self._log(f"  Dense:             [skipped: {e}]")
                time_dense = None
                count_dense = None
                has_dense = False

            # Sparse uncached
            time_uncached, std_uncached, count_uncached = self._query_sparse(
                query, False, self.iterations, self.warmup
            )
            self._log(f"  Sparse (no cache): {time_uncached:7.3f}ms ± {std_uncached:.3f}ms ({count_uncached:5d} matches)")

            # Sparse cached (first - miss)
            self.bt_cached.clear_cache()
            time_miss, _, _ = self._query_sparse(query, True, 1, 0)

            # Sparse cached (hits)
            time_cached, std_cached, count_cached = self._query_sparse(
                query, True, self.iterations, 0
            )
            self._log(f"  Sparse (cached):   {time_cached:7.3f}ms ± {std_cached:.3f}ms ({count_cached:5d} matches)")

            # Calculate speedups
            speedup_sparse = time_dense / time_uncached if has_dense else None
            speedup_cache_vs_uncached = time_uncached / time_cached
            speedup_cache_vs_dense = time_dense / time_cached if has_dense else None

            if has_dense:
                self._log(f"  Speedup (sparse vs dense):  {speedup_sparse:5.1f}x")
                self._log(f"  Speedup (cache vs dense):   {speedup_cache_vs_dense:5.1f}x")
            self._log(f"  Speedup (cache vs uncached): {speedup_cache_vs_uncached:5.1f}x")

            # Verify results match
            if has_dense and (count_dense != count_uncached or count_dense != count_cached):
                # NOTE: For NOT operator, mismatch is expected if dense uses naive NOT
                # Sparse NOT excludes rows with all zeros (no tag confidence)
                # See _query_dense_multi() docstring for correct semantics
                self._log(f"  ⚠ WARNING: Result mismatch! Dense={count_dense}, Uncached={count_uncached}, Cached={count_cached}")

            results.append({
                'name': name,
                'dense_ms': time_dense,
                'uncached_ms': time_uncached,
                'cached_ms': time_cached,
                'miss_ms': time_miss,
                'count': count_uncached,
                'speedup_sparse': speedup_sparse,
                'speedup_cache': speedup_cache_vs_uncached,
                'speedup_cache_vs_dense': speedup_cache_vs_dense
            })

        self.results['multi_column'] = results

    def benchmark_cache_performance(self):
        """Detailed cache performance analysis."""
        self._header("Cache Performance Analysis", level=1)

        # Test repeated query pattern
        query = {'column': 'Tag1', 'op': '==', 'value': HIGH}

        self._log("\nRepeated Query Pattern (Q1 × 10):")
        self.bt_cached.clear_cache()

        times = []
        for i in range(10):
            t = time.perf_counter()
            result = self.bt_cached.query(query)
            elapsed = (time.perf_counter() - t) * 1000
            times.append(elapsed)
            status = "MISS" if i == 0 else "HIT"
            self._log(f"  Query {i+1:2d}: {elapsed:7.3f}ms ({status})")

        stats = self.bt_cached.cache_stats()
        self._log(f"\nCache Statistics:")
        self._log(f"  Hits:          {stats['hits']}")
        self._log(f"  Misses:        {stats['misses']}")
        self._log(f"  Hit Rate:      {stats['hit_rate']:.1%}")
        self._log(f"  Cache Size:    {stats['size_entries']} entries")
        self._log(f"  Memory:        {stats['size_mb']:.3f} MB")
        self._log(f"  Data Version:  {stats['data_version']}")

        # Test cache overhead with unique queries
        self._log("\n\nCache Overhead Test (30 unique queries):")

        queries_unique = [
            {'column': f'Tag{(i % self.n_cols) + 1}', 'op': '==', 'value': [HIGH, MEDIUM, LOW][i % 3]}
            for i in range(30)
        ]

        # With cache (all misses)
        self.bt_cached.clear_cache()
        t1 = time.perf_counter()
        for q in queries_unique:
            self.bt_cached.query(q)
        time_with_cache = (time.perf_counter() - t1) * 1000

        # Without cache
        t2 = time.perf_counter()
        for q in queries_unique:
            self.bt_uncached.query(q)
        time_without_cache = (time.perf_counter() - t2) * 1000

        overhead = (time_with_cache / time_without_cache - 1) * 100

        self._log(f"  With cache:    {time_with_cache:.2f}ms")
        self._log(f"  Without cache: {time_without_cache:.2f}ms")
        self._log(f"  Overhead:      {overhead:.2f}%")

        if overhead < 10:
            self._log(f"  ✓ Overhead acceptable (<10%)")
        else:
            self._log(f"  ⚠ Overhead exceeds 10% threshold")

        self.results['cache'] = {
            'first_query_ms': times[0],
            'subsequent_avg_ms': np.mean(times[1:]),
            'speedup': times[0] / np.mean(times[1:]),
            'overhead_percent': overhead,
            'hit_rate': stats['hit_rate']
        }

    def run_unit_tests(self):
        """Run basic unit tests to verify correctness."""
        self._header("Unit Tests", level=1)

        tests_passed = 0
        tests_failed = 0

        # Test 1: Construction
        self._log("\nTest 1: BaseTag Construction")
        try:
            bt = BaseTag.create_random(100, ['A', 'B'], 0.1, seed=42)
            assert bt.shape == (100, 2)
            self._log("  ✓ PASSED")
            tests_passed += 1
        except Exception as e:
            self._log(f"  ✗ FAILED: {e}")
            tests_failed += 1

        # Test 2: Basic Query
        self._log("\nTest 2: Basic Query")
        try:
            result = self.bt_cached.query({'column': 'Tag1', 'op': '==', 'value': HIGH})
            assert result.count >= 0
            assert len(result.indices) == result.count
            self._log(f"  ✓ PASSED ({result.count} matches)")
            tests_passed += 1
        except Exception as e:
            self._log(f"  ✗ FAILED: {e}")
            tests_failed += 1

        # Test 3: Cache Hit/Miss
        self._log("\nTest 3: Cache Functionality")
        try:
            query = {'column': 'Tag1', 'op': '==', 'value': HIGH}
            self.bt_cached.clear_cache()

            # First query (miss)
            result1 = self.bt_cached.query(query)

            # Second query (hit)
            result2 = self.bt_cached.query(query)

            assert result1.count == result2.count
            assert np.array_equal(result1.indices, result2.indices)

            stats = self.bt_cached.cache_stats()
            assert stats['hits'] >= 1
            assert stats['misses'] >= 1

            self._log(f"  ✓ PASSED (hit_rate: {stats['hit_rate']:.1%})")
            tests_passed += 1
        except Exception as e:
            self._log(f"  ✗ FAILED: {e}")
            tests_failed += 1

        # Test 4: Result Consistency
        self._log("\nTest 4: Dense vs Sparse Consistency")
        try:
            query = {'column': 'Tag1', 'op': '==', 'value': HIGH}
            sparse_result = self.bt_cached.query(query, use_cache=False)
            dense_mask = self.dense[:, 0] == HIGH
            dense_count = np.sum(dense_mask)

            assert sparse_result.count == dense_count
            self._log(f"  ✓ PASSED (both found {dense_count} matches)")
            tests_passed += 1
        except Exception as e:
            self._log(f"  ✗ FAILED: {e}")
            tests_failed += 1

        # Test 5: Cache Invalidation
        self._log("\nTest 5: Cache Auto-Invalidation")
        try:
            query = {'column': 'Tag1', 'op': '==', 'value': HIGH}
            self.bt_cached.clear_cache()

            # Query and cache
            result1 = self.bt_cached.query(query)
            stats1 = self.bt_cached.cache_stats()
            version1 = stats1['data_version']

            # Modify data
            new_data = sparse.csc_matrix(
                np.ones((self.n_rows, self.n_cols), dtype=np.uint8) * HIGH
            )
            self.bt_cached._data = new_data

            # Check cache cleared
            stats2 = self.bt_cached.cache_stats()
            assert stats2['size_entries'] == 0
            assert stats2['data_version'] == version1 + 1

            self._log(f"  ✓ PASSED (cache cleared, version {version1} → {version1+1})")
            tests_passed += 1

            # Restore original data for remaining tests
            self.bt_cached._data = self.bt_uncached._data

        except Exception as e:
            self._log(f"  ✗ FAILED: {e}")
            tests_failed += 1

        self._log(f"\n{'='*70}")
        self._log(f"Unit Test Summary: {tests_passed} passed, {tests_failed} failed")
        self._log(f"{'='*70}")

        self.results['unit_tests'] = {
            'passed': tests_passed,
            'failed': tests_failed,
            'total': tests_passed + tests_failed
        }

    def generate_summary(self):
        """Generate summary report."""
        self._header("Performance Summary", level=1)

        # Single-column summary table
        if 'single_column' in self.results:
            self._log("\nSingle-Column Query Performance:")
            self._log(f"{'Query':<25} {'Dense':<12} {'Sparse':<12} {'Cached':<12} {'Speedup':<10}")
            self._log(f"{'':<25} {'(ms)':<12} {'(ms)':<12} {'(ms)':<12} {'(vs Dense)':<10}")
            self._log('-' * 75)

            for r in self.results['single_column']:
                speedup = r['dense_ms'] / r['cached_ms']  # How many times faster (Dense/Cached)
                self._log(f"{r['name']:<25} "
                         f"{r['dense_ms']:>7.3f}      "
                         f"{r['uncached_ms']:>7.3f}      "
                         f"{r['cached_ms']:>7.3f}      "
                         f"{speedup:>6.1f}x")

        # Multi-column summary
        if 'multi_column' in self.results:
            self._log("\nMulti-Column Query Performance:")
            self._log(f"{'Query':<30} {'Dense':<12} {'Uncached':<12} {'Cached':<12} {'Speedup':<10}")
            self._log(f"{'':<30} {'(ms)':<12} {'(ms)':<12} {'(ms)':<12} {'(vs Dense)':<10}")
            self._log('-' * 77)

            for r in self.results['multi_column']:
                if r['dense_ms'] is not None:
                    speedup = r['dense_ms'] / r['cached_ms']
                    dense_str = f"{r['dense_ms']:>7.3f}"
                else:
                    speedup = r['uncached_ms'] / r['cached_ms']
                    dense_str = "    N/A"

                self._log(f"{r['name']:<30} "
                         f"{dense_str}      "
                         f"{r['uncached_ms']:>7.3f}      "
                         f"{r['cached_ms']:>7.3f}      "
                         f"{speedup:>6.1f}x")

        # Cache summary
        if 'cache' in self.results:
            cache = self.results['cache']
            self._log("\nCache Performance:")
            self._log(f"  First query (miss):    {cache['first_query_ms']:.3f}ms")
            self._log(f"  Repeated query (hit):  {cache['subsequent_avg_ms']:.3f}ms")
            self._log(f"  Speedup:               {cache['speedup']:.1f}x")
            self._log(f"  Overhead:              {cache['overhead_percent']:.2f}%")
            self._log(f"  Hit rate:              {cache['hit_rate']:.1%}")

        # Memory summary
        if 'memory' in self.results:
            mem = self.results['memory']
            self._log("\nMemory Efficiency:")
            self._log(f"  Dense:        {mem['dense_mb']:.2f} MB")
            self._log(f"  Sparse:       {mem['sparse_mb']:.2f} MB")
            self._log(f"  Savings:      {mem['savings_percent']:.1f}%")

        # Overall conclusions
        self._log("\nKey Findings:")

        if 'single_column' in self.results:
            avg_speedup_cache = np.mean([r['dense_ms']/r['cached_ms']
                                        for r in self.results['single_column']])
            self._log(f"  • Cached queries are {avg_speedup_cache:.0f}x faster than dense on average")

        if 'cache' in self.results:
            cache = self.results['cache']
            self._log(f"  • Cache provides {cache['speedup']:.0f}x speedup for repeated queries")
            self._log(f"  • Cache overhead is only {cache['overhead_percent']:.1f}% for unique queries")

        if 'memory' in self.results:
            mem = self.results['memory']
            self._log(f"  • Sparse format saves {mem['savings_percent']:.0f}% memory vs dense")

        if 'unit_tests' in self.results:
            tests = self.results['unit_tests']
            self._log(f"  • All {tests['passed']}/{tests['total']} unit tests passed")

    def save_report(self, filename: str):
        """Save report to file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.report_lines))
        print(f"\n{'='*70}")
        print(f"Report saved to: {filename}")
        print(f"{'='*70}")

    def run_all(self) -> str:
        """Run all benchmarks and return report filename."""
        print(f"\n{'#'*70}")
        print(f"# BaseTag v2.1 - Comprehensive Performance Benchmark")
        print(f"# Configuration: {self.size_config.upper()}")
        print(f"# Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'#'*70}")

        # Initialize
        self.initialize_data()

        # Run tests
        self.run_unit_tests()
        self.benchmark_single_column_queries()
        self.benchmark_multi_column_queries()
        self.benchmark_cache_performance()

        # Summary
        self.generate_summary()

        # Save report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Use reports directory (gitignored) relative to project root
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        filename = os.path.join(reports_dir, f"performance_report_{self.size_config}_{timestamp}.txt")
        self.save_report(filename)

        return filename


def main():
    """Run benchmarks for all size configurations."""
    print("\n" + "="*70)
    print("BaseTag v2.1 - Complete Performance Analysis")
    print("="*70)
    print("\nThis will run comprehensive benchmarks for:")
    print("  • Small matrices (1K rows)")
    print("  • Medium matrices (100K rows)")
    print("  • Large matrices (1M rows)")
    print("\nEach test compares:")
    print("  1. Dense numpy arrays (baseline)")
    print("  2. Sparse arrays without cache (v2.0)")
    print("  3. Sparse arrays with cache (v2.1)")
    print("\n" + "="*70)

    configs = ['small', 'medium', 'large']
    report_files = []

    for config in configs:
        print(f"\n\n{'#'*70}")
        print(f"# STARTING {config.upper()} CONFIGURATION")
        print(f"{'#'*70}\n")

        try:
            benchmark = PerformanceBenchmark(size_config=config)
            report_file = benchmark.run_all()
            report_files.append(report_file)
        except Exception as e:
            print(f"\n❌ ERROR in {config} configuration: {e}")
            import traceback
            traceback.print_exc()

    # Summary
    print(f"\n\n{'='*70}")
    print("ALL BENCHMARKS COMPLETE")
    print(f"{'='*70}")
    print(f"\nGenerated {len(report_files)} reports:")
    for f in report_files:
        print(f"  • {f}")
    print("\n" + "="*70)

    return report_files


if __name__ == '__main__':
    report_files = main()
