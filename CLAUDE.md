# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BaseTag is a high-performance sparse array library for tag confidence data with intelligent query caching. It provides 95% memory savings and 100-170x speedups for sparse tag confidence queries through scipy sparse arrays and intelligent caching.

**Current Version:** v2.2.0

## Development Environment

```bash
# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Dependencies:
# - numpy>=1.20.0
# - scipy>=1.7.0
# - psutil>=5.8.0
```

## Running Tests and Benchmarks

```bash
# Run benchmarks (from project root)
cd src
python benchmark.py

# Benchmark outputs saved to docs/ directory
# Generates performance reports for small (1K), medium (100K), and large (1M) matrices
```

**Note:** There is currently a `tests/` directory but no test files. Tests should be added there when created.

## Core Architecture

### Data Model

The library is built around **sparse CSC arrays** (Compressed Sparse Column) from scipy.sparse. This format is critical for performance:

- **Storage**: Only non-zero values are stored (tag confidences 1-3)
- **Queries**: Column-wise access is O(nnz) not O(rows)
- **Memory**: 95% reduction vs dense arrays for 1% sparsity

### Key Components

**1. TagConfidence Enum** (`src/basetag.py:58-68`)
- IntEnum with values: NONE=0, LOW=1, MEDIUM=2, HIGH=3
- Sparse matrices only store non-zero values (1-3)
- Zero means "no data" not "data with value zero"

**2. BaseTag Class** (`src/basetag.py:127+`)
- Main sparse matrix container
- Stores data as `scipy.sparse.csc_array` (uint8 dtype)
- Column names mapped via `_column_index` dict
- Query caching system with automatic invalidation

**3. QueryResult Class** (`src/basetag.py:71-124`)
- Returns from query operations
- Stores row indices (not full boolean masks)
- Lazy mask computation for memory efficiency
- Provides `.count`, `.indices`, `.to_basetag()` methods

**4. Query Engine**
- Single-column queries: Direct sparse column access
- Multi-column queries: NumPy set operations (intersect1d, union1d, setdiff1d)
- Supported operators: ==, !=, >, >=, <, <=, IN
- Logical operators: AND, OR, NOT
- Queries work directly on sparse matrix internals (no dense conversion)

**5. Caching System** (`src/basetag.py:198-227`)
- SHA256 hash-based query cache
- Automatic invalidation via `@invalidates_cache` decorator
- Memory bounds: max_entries=256, max_memory_mb=10.0
- Large results (>1MB) not cached by default
- Statistics tracking: hits, misses, hit_rate, memory usage

### Critical Implementation Details

**Sparse Matrix Migration (v2.2.0)**
- Migrated from deprecated `sparse.spmatrix` to `sparse.sparray`
- `_ensure_csc_format()` handles backward compatibility
- Always converts to CSC array internally
- Type alias `SparseType` supports both formats during transition

**NOT Operator Semantics (v2.1.1 fix)**
- NOT operates ONLY on rows with non-zero data
- Excludes all-zero rows (rows with no tag confidence)
- Example: NOT(Tag==LOW) returns rows with data where Tag!=LOW
- This is correct sparse semantics: zero = "no data", not "data with value 0"
- Implementation: `np.setdiff1d(rows_with_any_data, matching_rows)`

**Query Optimization Patterns**
1. Never convert sparse columns to dense
2. Only examine non-zero elements via `.data`, `.indices`, `.indptr`
3. Build results using row indices, not boolean masks
4. Use NumPy set operations instead of Python sets
5. Short-circuit on empty intermediate results

**Memory Optimization**
- `optimize_indices_dtype()`: Converts int32→int16 for matrices <65K rows
- Saves 50% indices memory
- Safe because int16 max = 65,535 rows

## Code Patterns

### Creating BaseTag Instances

```python
# From random data (for testing)
bt = BaseTag.create_random(n_rows, column_names, fill_percent, seed, enable_cache=True)

# From numpy array
bt = BaseTag.from_array(dense_array, column_names)

# From sparse matrix
bt = BaseTag.from_sparse(sparse_matrix, column_names)

# From dictionary
bt = BaseTag.from_dict(data_dict, column_names, n_rows)
```

### Query Structure

Single-column queries use `column`, `op`, `value`/`values`.
Multi-column queries use `operator` and `conditions` list.

```python
# Single column
{'column': 'Tag1', 'op': '==', 'value': TagConfidence.HIGH}

# Multi-column AND
{
    'operator': 'AND',
    'conditions': [
        {'column': 'Tag1', 'op': '>=', 'value': TagConfidence.MEDIUM},
        {'column': 'Tag2', 'op': 'IN', 'values': [TagConfidence.HIGH, TagConfidence.MEDIUM]}
    ]
}

# NOT (operates only on rows with data)
{
    'operator': 'NOT',
    'conditions': [{'column': 'Tag1', 'op': '==', 'value': TagConfidence.LOW}]
}
```

### Adding Mutation Methods

When adding data modification methods (e.g., `set_column`, `add_rows`), use the `@invalidates_cache` decorator to auto-clear cache:

```python
@invalidates_cache
def set_column(self, column_name: str, values: np.ndarray) -> 'BaseTag':
    """Set values for a column (auto-invalidates cache)."""
    # ... modify self._data_internal ...
    return self  # Method chaining supported
```

## Performance Characteristics

### Scale Performance (1M rows, 100 cols, 99% sparse)

| Operation | Uncached | Cached | Speedup |
|-----------|----------|--------|---------|
| Single-column | 0.19ms | 0.009ms | 21x |
| Multi-column AND | 0.45ms | 0.012ms | 38x |
| Multi-column OR | 1.19ms | 0.012ms | 99x |

### When to Enable Caching

- ✅ Interactive queries (dashboards, exploration)
- ✅ Repeated query patterns
- ✅ Query batches with duplicates
- ❌ All-unique queries (cache overhead: ~15%)
- ❌ Extreme memory constraints (<5MB available)

## Future Development

Planned features (see CHANGELOG.md for v2.2+ roadmap):
- LRU cache eviction (currently simple limit-based)
- Persistent cache option
- Mutation methods (set_column, add_rows, delete_rows)
- Multi-threaded query execution
- Query plan optimization
- Custom cache configuration API

## Important Constraints

1. **Sparse CSC format is mandatory** - Never convert to dense for queries
2. **uint8 dtype required** - Tag confidence values are 0-3
3. **Column names must be unique** - Used for indexing
4. **Cache invalidation required** - Use decorator on mutation methods
5. **NOT operator semantics** - Excludes all-zero rows (sparse semantics)
6. **No current test suite** - Add tests to `tests/` directory when creating them