# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BaseTag is a high-performance sparse array library for tag confidence data with intelligent query caching. It provides 95% memory savings and 100-170x speedups for sparse tag confidence queries through scipy sparse arrays and intelligent caching.

**Current Version:** v2.4.0

**Key Features** (v2.4.0):
- 100% type hint coverage with mypy strict mode
- Custom exception hierarchy for better error handling
- Modular architecture with dedicated cache manager
- 173 comprehensive tests with ≥85% coverage
- Production-grade documentation

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
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Generate HTML coverage report
pytest --cov=src --cov-report=html tests/

# Run type checking
mypy src/basetag.py src/cache_manager.py src/exceptions.py

# Run benchmarks (from project root)
cd src
python benchmark.py

# Benchmark outputs saved to reports/ directory (gitignored)
# Generates performance reports for small (1K), medium (100K), and large (1M) matrices
```

**Test Suite**: 173 tests across 9 test files with ≥85% coverage
- `test_cache_manager.py`: Cache manager functionality
- `test_exceptions.py`: Exception hierarchy and usage
- `test_critical_bugs.py`: Critical bug fixes validation
- `test_data_integrity.py`: Data consistency and immutability
- `test_edge_cases.py`: Boundary conditions
- `test_error_handling.py`: Error scenarios
- `test_integration.py`: End-to-end workflows
- `test_performance.py`: Performance validation
- `test_query_operations.py`: Query operators

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

## Type Checking (v2.4+)

This project enforces type safety with mypy strict mode:

```bash
# Check core modules
mypy src/basetag.py src/cache_manager.py src/exceptions.py

# Check all source files
mypy src/
```

**Configuration**: `mypy.ini` with strict settings
- `disallow_untyped_defs = True`: All functions must have type hints
- `check_untyped_defs = True`: Type check untyped definitions
- `no_implicit_optional = True`: Explicit Optional[] required
- `warn_redundant_casts = True`: Detect unnecessary casts
- `strict_equality = True`: Stricter equality checks

**Type Patterns**:
```python
# Use TYPE_CHECKING to avoid circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .basetag import QueryResult

# Use Any for NumPy types to avoid scipy typing issues
from typing import Any
target_dtype: Any = np.int8

# Type annotations on all functions
def method_name(self, param: int) -> Optional[str]:
    """Docstring."""
    pass
```

## Custom Exceptions (v2.4+)

Use domain-specific exceptions from `src/exceptions.py`:

**Exception Hierarchy**:
```
BaseTagError (Exception)
├── ValidationError (ValueError) - Input validation failures
│   └── MatrixSizeError - Dimensions exceed limits
└── QueryError (BaseException)
    ├── InvalidQueryStructureError (ValueError) - Malformed query dict
    ├── InvalidColumnError (KeyError) - Column name not found
    ├── InvalidOperatorError (ValueError) - Unsupported operator
    └── InvalidValueError (ValueError) - Invalid TagConfidence value
```

**Usage**:
```python
from src.exceptions import InvalidColumnError, InvalidValueError

# Raise specific exceptions
if column_name not in self._column_index:
    raise InvalidColumnError(f"Column '{column_name}' not found")

if value == TagConfidence.NONE:
    raise InvalidValueError("Cannot compare to NONE/zero value")
```

**Backward Compatibility**: All custom exceptions inherit from standard exceptions (ValueError, KeyError), so existing `except ValueError:` blocks still work.

## Cache System (v2.4+)

Cache logic is managed by `QueryCacheManager` class in `src/cache_manager.py`:

**Architecture**:
- MD5-based cache keys for consistent hashing
- Memory-bounded storage (256 entries, 10MB max by default)
- Hit/miss statistics tracking
- Automatic invalidation on data changes

**Accessing Cache Manager**:
```python
# Check if caching is enabled
if bt._cache_manager:
    stats = bt._cache_manager.stats()
    print(f"Hit rate: {stats['hit_rate']:.1%}")

# Custom cache configuration
from src.cache_manager import QueryCacheManager
bt._cache_manager = QueryCacheManager(
    max_entries=512,
    max_memory_mb=20.0,
    large_result_threshold_mb=2.0
)
```

**Key Generation**:
- Simple queries: Fast string-based hashing (`"col|op|val"`)
- Complex queries: JSON serialization with `QueryEncoder`
- Result: 32-character MD5 hex string

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
6. **Test suite exists** - Run `pytest tests/` to execute 9 tests (7 critical + 2 performance)
7. **Integer limits validated** - `create_random()` validates against MAX_SAFE_NNZ (2.1B)
8. **Index optimization safety** - `optimize_indices_dtype()` validates actual index values before conversion
9. **Thread-safe random generation** - Uses `np.random.default_rng()` not global seed