# Changelog

All notable changes to BaseTag will be documented in this file.

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
