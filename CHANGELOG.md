# Changelog

All notable changes to BaseTag will be documented in this file.

## [2.4.0] - 2025-12-23

### Added
- **Complete type safety**: 100% type hint coverage with mypy enforcement
  - Added type hints to 12 methods missing return types
  - Created `_ensure_tag_confidence()` type guard for safe value conversion
  - All decorators and helpers fully typed
  - PEP 561 compliant with `py.typed` marker file
  - Configured mypy with strict mode in `mypy.ini`
- **Custom exception hierarchy**: Domain-specific exceptions for better error handling
  - Created 9 custom exception classes in `src/exceptions.py`
  - `BaseTagError` base class for all library exceptions
  - `ValidationError`, `QueryError` hierarchy with backward compatibility
  - All exceptions inherit from standard exceptions (ValueError, KeyError) for compatibility
  - 36 new tests for exception behavior and backward compatibility
- **QueryCacheManager class**: Dedicated cache management module
  - Extracted ~250 lines from BaseTag into `src/cache_manager.py`
  - MD5-based cache key generation
  - Memory-bounded storage with configurable limits
  - Hit/miss statistics tracking
  - Clean separation of concerns
- **Comprehensive documentation**:
  - `CONTRIBUTING.md`: Development setup, testing, PR guidelines
  - `docs/ARCHITECTURE.md`: Design principles, component overview, extension points
  - `docs/DEPLOYMENT.md`: Production deployment, performance tuning, troubleshooting
  - `LICENSE`: MIT License file
  - Enhanced docstrings for `_get_column_index()`, `get_value_counts()`, `_transform_comparison()`
- **Helper methods for better modularity**:
  - `_execute_timed_query()`: Eliminates ~100 lines of duplication in benchmark.py
  - `_get_rows_with_any_data()`: Simplifies NOT operator logic (35 lines → 8 lines)

### Changed
- **Refactored cache system**: BaseTag now delegates to QueryCacheManager
  - Removed 8 cache-related attributes from BaseTag.__init__()
  - Replaced with single `_cache_manager` optional instance
  - All cache operations delegated to manager class
  - Deleted 3 internal cache methods (`_query_to_key()`, `_should_cache_result()`, `_get_cache_memory_mb()`)
- **Refactored benchmark.py**: Eliminated code duplication
  - Created `_execute_timed_query()` helper method
  - Refactored `_query_dense()`, `_query_dense_multi()`, `_query_sparse()` to use helper
  - Reduced ~100 lines of duplicated timing logic
  - Benchmark reports now saved to `reports/` directory (gitignored)
- **Exception types**: All ValueError/KeyError replaced with custom exceptions
  - 17 exception sites updated to use specific exception types
  - Backward compatible: custom exceptions inherit from base exceptions
  - Better error context and messages
- **Updated pyproject.toml**: Production-grade configuration
  - Version bumped to 2.4.0
  - Comprehensive metadata (keywords, classifiers, URLs)
  - Optional dev dependencies group
  - Integrated mypy and pytest configuration
  - Python ≥3.9 requirement

### Fixed
- **Documentation**: Fixed LICENSE and AUTHORS placeholders in README.md
- **QUICKSTART.md**: Corrected path references and removed non-existent API mentions
  - Fixed `basetag_v2.1_package/` path reference
  - Updated `to_array()` → `to_basetag()` in examples

### Removed
- **Dated artifacts**: Removed timestamped performance report snapshots
  - Deleted 3 performance report files from docs/
  - Deleted test coverage report snapshot
  - Reports now generated to gitignored `reports/` directory
- **Old cache methods**: Removed from basetag.py after extraction
  - `_query_to_key()`, `_should_cache_result()`, `_get_cache_memory_mb()`
  - Now handled by QueryCacheManager class
- **Unused imports**: Removed `hashlib` and `json` from basetag.py
  - Moved to cache_manager.py where they're actually used

### Improved
- **Code organization**: Clear separation of concerns
  - Cache logic fully extracted to dedicated module
  - Benchmark timing logic centralized in helper method
  - NOT operator logic extracted to testable method
- **Type safety**: Zero mypy errors in strict mode
  - All functions fully typed with proper annotations
  - Custom types for NumPy arrays to avoid scipy typing issues
  - TYPE_CHECKING guards to prevent circular imports
- **Error messages**: Custom exceptions provide clearer context
  - InvalidColumnError shows available columns
  - InvalidOperatorError shows the invalid operator
  - InvalidValueError explains why value is invalid
- **Maintainability**: Reduced cognitive load
  - basetag.py reduced from 982 to ~730 lines
  - benchmark.py reduced from 808 to ~700 lines
  - Cleaner method signatures and responsibilities
- **Test coverage**: 173 tests (was 137), 36 new tests added
  - `tests/test_cache_manager.py`: 15 tests for cache manager functionality
  - `tests/test_exceptions.py`: 21 tests for exception hierarchy and usage
  - All tests passing with ≥85% coverage maintained
- **.gitignore**: Comprehensive ignore patterns
  - Generated reports directory
  - Python artifacts
  - Testing/coverage outputs
  - IDE and environment files

## [2.3.0] - 2025-12-22

### Fixed
- **Critical**: Index dtype optimization validates actual index values (prevents data corruption)
  - Added validation of max index values before converting to smaller dtypes
  - Validates both `.indices` and `.indptr` arrays to prevent overflow
  - Prevents silent data corruption when sparse data is concentrated in high row indices
- **Critical**: Integer overflow protection in `create_random()` for large matrices
  - Validates nnz against MAX_SAFE_NNZ (2.1 billion) with clear error messages
  - Uses float intermediates to detect overflow before it occurs
  - Validates matrix dimensions are positive
  - Handles zero nnz gracefully
- **Critical**: JSON serialization handles TagConfidence enums in cache keys
  - Added `QueryEncoder` custom JSON encoder for TagConfidence enums
  - Handles NumPy integer and floating types
  - Fallback to repr() for any remaining non-serializable types
  - Prevents cache system from crashing on enum values

### Performance
- **Fast path for simple query cache keys** (50-70% faster)
  - String-based hashing for single-column queries bypasses JSON serialization
  - Falls back to JSON for complex multi-column queries
  - Reduces cache key generation overhead significantly
- **O(1) cache memory tracking** (was O(n) iteration)
  - Incremental tracking of cache memory usage
  - Eliminates repeated iteration through all cached results
  - Faster cache decisions with no performance overhead
- **Thread-safe random generation** using local RNG
  - Uses `np.random.default_rng()` instead of global `np.random.seed()`
  - No side effects on global random state
  - Safe for concurrent use

### Improved
- **Constants for magic numbers**
  - Added `MAX_INT8_VALUE`, `MAX_INT16_VALUE`, `MAX_INT32_VALUE`
  - Added `INT8_THRESHOLD`, `INT16_THRESHOLD`
  - Added `DEFAULT_CACHE_MAX_ENTRIES`, `DEFAULT_CACHE_MAX_MEMORY_MB`
  - Added `CACHE_OVERHEAD_BYTES`, `MAX_SAFE_NNZ`
  - All magic numbers now have named constants with documentation
- **Enhanced validation messages**
  - Clear error messages for overflow conditions
  - Helpful context in validation failures
  - Better debugging information

### Added
- **Comprehensive test suite**
  - pytest framework configuration
  - 7 critical bug tests covering all fixes
  - 2 performance regression tests
  - 100% pass rate on all tests
  - Tests for thread safety, data integrity, and edge cases

### API Compatibility
- **No breaking changes** - All improvements are backward compatible
- Minor enhancement: `create_random()` now raises clearer errors for invalid inputs

---

## [2.2.0] - 2025-12-22

### Changed
- **Migrated to scipy.sparse array format** (from deprecated matrix format)
  - Replaced `sparse.csc_matrix` with `sparse.csc_array` throughout codebase
  - Updated all type hints to use `sparse.sparray` (with backward compatibility)
  - Replaced `isspmatrix_csc()` checks with `.format == 'csc'` pattern
  - Added `_ensure_csc_format()` helper for validation and conversion
  - **Backward compatible**: Still accepts sparse matrix input, converts to array internally
  - **No breaking changes**: API remains identical
  - **Performance**: Zero impact (identical speed and memory)

### Added
- `SparseType` type alias supporting both matrix and array formats during transition
- Comprehensive type checking with `_ensure_csc_format()` static method
- Automatic conversion from deprecated matrix to current array format

### Fixed
- Future-proofs codebase for SciPy 2.0 (which removes sparse matrix support)
- Eliminates deprecation warnings in SciPy 1.13+

### Migration Notes
- No code changes required for users
- Both matrix and array inputs are accepted and work identically
- Internally, everything now uses sparse arrays
- See SPARSE_MIGRATION_ANALYSIS.md for technical details

---

## [2.1.1] - 2025-12-19

### Fixed
- **NOT operator semantics**: Corrected to exclude all-zero rows (no tag confidence data)
  - NOT now operates only on rows with ANY non-zero value
  - Matches sparse data semantics where zero = "no data"
  - Dense benchmark implementation updated to match sparse behavior
  - Result consistency: dense and sparse NOT queries now return identical counts

### Added
- **Memory optimization**: New `optimize_indices_dtype()` method
  - Automatically reduces indices from int32 to int16 for matrices <65,536 rows
  - Saves 50% indices memory for applicable matrices
  - Example: 10K rows matrix reduces indices from 792 bytes → 396 bytes
  - Supports in-place or copy operations
- **Enhanced documentation**: Comprehensive comments explaining NOT operator semantics
- **Complete benchmark suite**: Updated with dense multi-column query implementations

### Changed
- Benchmark reports now show correct speedup calculations (fixed inverse ratio display)
- Memory usage reporting now includes all sparse matrix components
- Test framework updated with NOT operator semantic clarification

### Performance
- All benchmarks passing with consistent results
- 100% unit test pass rate maintained
- No performance regression from semantic fixes

---

## [2.1.0] - 2025-12-18

### Added
- **Query caching system**: Intelligent caching for repeated queries
  - 10-40x speedup for repeated queries
  - Automatic cache invalidation on data modification
  - Memory-bounded with configurable limits
  - Per-query cache enable/disable option
  - Cache statistics tracking (hits, misses, hit rate, memory)
- **Cache management API**:
  - `cache_stats()` - Get detailed cache statistics
  - `clear_cache()` - Manual cache clearing
  - `enable_cache` parameter in constructor
  - `use_cache` parameter in query method

### Performance
- Cached queries: 0.009ms typical (independent of matrix size)
- Cache overhead: <15% for unique queries at scale
- Memory efficient: ~26KB per cached 1M row query result
- Hit rates: 78-97% for typical workloads

### Changed
- Internal property setters now invalidate cache automatically
- Memory tracking includes cache overhead

---

## [2.0.0] - 2025-12-17

### Added
- **NumPy-optimized query engine**: 8-10x speedup over v1.0
  - Vectorized operations using NumPy boolean indexing
  - CSC sparse matrix format for efficient column access
  - Optimized multi-column query processing
- **Comprehensive query operators**:
  - Single-column: `==`, `!=`, `>`, `>=`, `<`, `<=`, `IN`
  - Multi-column: `AND`, `OR`, `NOT`
  - Nested query support
- **QueryResult object**: Rich result interface
  - Lazy mask computation
  - Filtered data extraction
  - Column-specific queries
- **Factory methods**:
  - `create_random()` - Generate test data
  - `from_array()` - From dense numpy
  - `from_sparse()` - From scipy sparse
  - `from_dict()` - From dictionary
- **Memory tracking**: Detailed memory usage reporting
- **Performance benchmarks**: Comprehensive test suite

### Performance
- Single-column queries: 0.2-0.4ms (100K rows, 1% sparsity)
- Multi-column queries: 0.5-2ms (100K rows)
- Memory: 95% reduction vs dense (1% sparsity)

---

## [1.0.0] - 2025-12-15

### Fixed
- **Critical bug fix**: Dense matrix fallback in sparse code paths
  - Caused 2000x performance regression for sparse data
  - Now properly uses scipy sparse matrices throughout

### Added
- Basic sparse matrix support
- Simple query interface
- TagConfidence enum

### Performance
- 2000x speedup vs v0.1 (after fixing dense fallback bug)

---

## [0.1.0] - 2025-12-10

### Added
- Initial prototype release
- Basic tag confidence storage
- Simple query interface
- Dense numpy implementation

### Known Issues
- Performance issues with sparse data (fixed in v1.0)

---

## Version Comparison

| Version | Query Speed (100K) | Memory (1M) | Key Feature |
|---------|-------------------|-------------|-------------|
| v2.1.1 | 0.009ms (cached) | 4.75MB | NOT fix + memory opt |
| v2.1.0 | 0.009ms (cached) | 4.75MB | Query caching |
| v2.0.0 | 0.2-0.4ms | 4.75MB | NumPy optimization |
| v1.0.0 | 2.0-4.0ms | 4.75MB | Sparse fix |
| v0.1.0 | ~100ms | 95MB | Initial release |

## Migration Guides

### Migrating from v2.1.0 to v2.1.1

**NOT operator behavior change:**
```python
# v2.1.0 (naive NOT - incorrect for sparse data)
result = bt.query({'operator': 'NOT', ...})  # Included all-zero rows

# v2.1.1 (correct sparse semantics)
result = bt.query({'operator': 'NOT', ...})  # Excludes all-zero rows
```

If you need the old behavior (including all-zero rows), use positive conditions instead:
```python
# Instead of NOT(Tag2 == LOW)
# Use: Tag2 IN [NONE, MEDIUM, HIGH]
bt.query({'column': 'Tag2', 'op': 'IN', 'values': [0, 2, 3]})
```

**New memory optimization:**
```python
# Optimize indices for smaller matrices
if bt.shape[0] < 65536:
    bt.optimize_indices_dtype()  # Saves 50% indices memory
```

### Migrating from v2.0.0 to v2.1.0

Fully backward compatible. Enable caching:
```python
# Old (still works)
bt = BaseTag.create_random(1000, ['Tag1'], 0.01)

# New (with caching)
bt = BaseTag.create_random(1000, ['Tag1'], 0.01, enable_cache=True)
```

### Migrating from v1.0.0 to v2.0.0

Mostly compatible. Query API unchanged. Main difference:
```python
# v1.0.0 - Limited operators
result = bt.query({'column': 'Tag1', 'op': '==', 'value': 3})

# v2.0.0 - Full operator support + multi-column
result = bt.query({
    'operator': 'AND',
    'conditions': [
        {'column': 'Tag1', 'op': '>=', 'value': 2},
        {'column': 'Tag2', 'op': 'IN', 'values': [2, 3]}
    ]
})
```
