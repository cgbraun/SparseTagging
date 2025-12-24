# SparseTag v2.4.0

High-performance sparse array library for tag confidence data with intelligent query caching.

## What's New in v2.4.0

- ✅ **100% type safety**: Complete type hint coverage with mypy enforcement, PEP 561 compliant
- ✅ **Custom exceptions**: Domain-specific error hierarchy with backward compatibility
- ✅ **Refactored architecture**: Dedicated QueryCacheManager class, cleaner separation of concerns
- ✅ **Enhanced documentation**: CONTRIBUTING.md, ARCHITECTURE.md, DEPLOYMENT.md guides
- ✅ **173 comprehensive tests**: Added 36 new tests for cache manager and exception handling

## What's in v2.2.0

- ✅ **scipy.sparse array migration**: Modernized to use current array format (matrix format deprecated)
- ✅ **Backward compatible**: Still accepts matrix format, converts automatically
- ✅ **Future-proof**: Ready for SciPy 2.0
- ✅ **Zero performance impact**: Identical speed and memory usage

## What's in v2.1.1

- ✅ **NOT operator fix**: Correct semantics for sparse data (excludes all-zero rows)
- ✅ **Memory optimization**: `optimize_indices_dtype()` reduces indices memory by 50% for matrices <65K rows
- ✅ **Complete documentation**: Comprehensive benchmarks and usage guides
- ✅ **100% test pass rate**: All unit tests passing

## Performance Highlights

### At Scale (1M rows × 100 columns, 99% sparse)

| Operation | Dense | Sparse | Cached | Speedup |
|-----------|-------|--------|--------|---------|
| **Single-column** | 1.47ms | 0.19ms | 0.009ms | **169x** ⚡ |
| **Multi-column AND** | 1.90ms | 0.45ms | 0.012ms | **164x** ⚡ |
| **Multi-column OR** | 1.72ms | 1.19ms | 0.012ms | **145x** ⚡ |
| **Memory** | 95.37 MB | 4.75 MB | 4.75 MB | **95% savings** |

### Cache Performance

- **Repeated queries**: 24-36x speedup over uncached
- **Hit rate**: 78-97% (workload dependent)
- **Overhead**: <15% for unique queries at scale
- **Memory**: ~26KB per 1M row query result

## Installation

### For Users (Runtime Only)

```bash
pip install -r requirements.txt
```

### For Developers (Includes Testing Tools)

```bash
pip install -r requirements-dev.txt
```

### Requirements

**Runtime:**
- Python 3.9+
- NumPy ≥ 1.20 (2.0+ recommended)
- SciPy ≥ 1.8 (required for `sparse.csc_array`)
- psutil ≥ 5.8 (for memory tracking)

**Development (additional):**
- pytest ≥ 7.0
- pytest-cov ≥ 4.0
- mypy ≥ 1.0

See [REQUIREMENTS_GUIDE.md](docs/REQUIREMENTS_GUIDE.md) for detailed dependency information.

## Quick Start

```python
from src.sparsetag import SparseTag, TagConfidence

# Create sparse matrix (1M rows, 99% sparse)
bt = SparseTag.create_random(
    n_rows=1_000_000,
    column_names=['Tag1', 'Tag2', 'Tag3'],
    fill_percent=0.01,
    seed=42,
    enable_cache=True  # Enable query caching
)

# Simple query
result = bt.query({
    'column': 'Tag1',
    'op': '==',
    'value': TagConfidence.HIGH
})
print(f"Found {result.count} matches")  # ~3,300 matches

# Multi-column query
result = bt.query({
    'operator': 'AND',
    'conditions': [
        {'column': 'Tag1', 'op': '==', 'value': TagConfidence.HIGH},
        {'column': 'Tag2', 'op': '>=', 'value': TagConfidence.MEDIUM}
    ]
})

# Memory optimization for smaller matrices
if bt.shape[0] < 65536:
    bt.optimize_indices_dtype()  # Saves 50% indices memory

# Check cache statistics
stats = bt.cache_stats()
print(f"Hit rate: {stats['hit_rate']:.1%}")
print(f"Cache memory: {stats['size_mb']:.3f} MB")
```

## Core Features

### 1. Tag Confidence Enum

```python
class TagConfidence(IntEnum):
    NONE = 0    # No confidence / no data
    LOW = 1     # Low confidence
    MEDIUM = 2  # Medium confidence  
    HIGH = 3    # High confidence
```

### 2. Query Operations

**Single-column queries:**
```python
# Equality
bt.query({'column': 'Tag1', 'op': '==', 'value': TagConfidence.HIGH})

# Comparison
bt.query({'column': 'Tag1', 'op': '>', 'value': TagConfidence.LOW})

# IN operator
bt.query({'column': 'Tag1', 'op': 'IN', 'values': [TagConfidence.HIGH, TagConfidence.MEDIUM]})
```

**Multi-column queries:**
```python
# AND
bt.query({
    'operator': 'AND',
    'conditions': [
        {'column': 'Tag1', 'op': '==', 'value': TagConfidence.HIGH},
        {'column': 'Tag2', 'op': '>=', 'value': TagConfidence.MEDIUM}
    ]
})

# OR
bt.query({
    'operator': 'OR',
    'conditions': [
        {'column': 'Tag1', 'op': '==', 'value': TagConfidence.HIGH},
        {'column': 'Tag3', 'op': '==', 'value': TagConfidence.LOW}
    ]
})

# NOT (operates only on rows with data)
bt.query({
    'operator': 'NOT',
    'conditions': [
        {'column': 'Tag2', 'op': '==', 'value': TagConfidence.LOW}
    ]
})
```

### 3. NOT Operator Semantics

**IMPORTANT**: NOT operates only on rows with ANY non-zero value (rows with tag confidence data).

```python
# NOT(Tag2 == LOW) returns:
#   - Include: rows where Tag2 = MEDIUM or HIGH (has data, doesn't match)
#   - Exclude: rows where Tag2 = LOW (matches condition)
#   - Exclude: rows with all zeros (no tag confidence anywhere)

# This differs from naive NOT which would include all-zero rows.
# Zero in sparse matrix = "no data", not "data with value zero".
```

### 4. Query Caching

```python
# Enable/disable at construction
bt = SparseTag.create_random(1000, ['Tag1'], 0.01, enable_cache=True)

# Disable per query
result = bt.query(query_dict, use_cache=False)

# Manual cache management
bt.clear_cache()
stats = bt.cache_stats()

# Automatic invalidation on data modification
bt._data = new_sparse_matrix  # Cache auto-cleared
```

### 5. Memory Optimization

```python
# Check memory usage
mem = bt.memory_usage()
print(f"Data: {mem['data']/1024:.1f} KB")
print(f"Indices: {mem['indices']/1024:.1f} KB")
print(f"Total: {mem['total']/1024:.1f} KB")

# Optimize indices dtype (for matrices <65K rows)
bt.optimize_indices_dtype()  # Converts int32 → int16, saves 50%

# Non-destructive optimization
bt_optimized = bt.optimize_indices_dtype(inplace=False)
```

### 6. Type Safety & Quality (v2.4+)

```python
# 100% type hint coverage with mypy enforcement
from src.sparsetag import SparseTag, TagConfidence
from src.exceptions import ValidationError, InvalidColumnError

# PEP 561 compliant - includes py.typed marker
# Type checkers will recognize all types automatically

# Custom exception hierarchy with backward compatibility
try:
    bt.query({'column': 'NonExistent', 'op': '==', 'value': TagConfidence.HIGH})
except InvalidColumnError as e:  # Also catchable as KeyError
    print(f"Column error: {e}")

# 173 comprehensive tests with ≥85% coverage
# Modular architecture with dedicated QueryCacheManager
# Production docs: CONTRIBUTING.md, ARCHITECTURE.md, DEPLOYMENT.md
```

## Factory Methods

```python
# From random data
bt = SparseTag.create_random(n_rows, column_names, fill_percent, seed)

# From numpy array
bt = SparseTag.from_array(dense_array, column_names)

# From sparse matrix
bt = SparseTag.from_sparse(sparse_matrix, column_names)

# From dictionary
bt = SparseTag.from_dict(data_dict, column_names, n_rows)
```

## API Reference

### SparseTag Class

**Properties:**
- `shape` - (n_rows, n_columns)
- `column_names` - List of column names
- `sparsity` - Percentage of zero elements

**Methods:**
- `query(query_dict, use_cache=True)` - Execute query
- `cache_stats()` - Get cache statistics
- `clear_cache()` - Manually clear cache
- `memory_usage()` - Get memory breakdown
- `optimize_indices_dtype(inplace=True)` - Optimize memory
- `to_dense()` - Convert to dense numpy array

### QueryResult Class

**Properties:**
- `count` - Number of matching rows
- `indices` - Array of row indices
- `mask` - Sparse boolean mask

**Methods:**
- `to_array(dense=False)` - Get filtered data as array
- `get_column(column_name, dense=False)` - Get specific column

## Benchmarking

Run comprehensive benchmarks:

```bash
cd src
python benchmark.py
```

This generates detailed reports for small (1K), medium (100K), and large (1M) matrices comparing:
- Dense numpy arrays (baseline)
- Sparse arrays without cache
- Sparse arrays with cache

Reports saved to `docs/` directory.

## Use Cases

### Ideal For ✅

- Tag confidence queries (0-3 values)
- Sparse categorical data (>90% zeros)
- Interactive data exploration
- Dashboard backends
- Repeated query patterns
- Memory-constrained environments

### Not Recommended ❌

- Dense data (<50% sparse)
- Every query unique (no cache benefit)
- Extremely memory-limited (<5MB)
- Real-time microsecond requirements

## Configuration

Default cache settings:

```python
# Enable cache with defaults
bt = SparseTag.create_random(100000, ['Tag1'], 0.01, enable_cache=True)

# Default cache limits:
# - max_entries: 256
# - max_memory_mb: 10.0
# - large_result_threshold_mb: 1.0
```

For custom cache configuration, modify the cache parameters in the SparseTag constructor (future enhancement).

## Performance Tips

1. **Enable caching** for interactive workloads
2. **Use indices optimization** for matrices <65K rows
3. **Batch queries** when possible to improve cache hit rate
4. **Monitor cache stats** to tune configuration
5. **Clear cache** periodically if memory constrained

## Examples

See `docs/` for:
- Performance benchmarks (small/medium/large)
- Detailed usage examples
- Memory optimization guides

## Known Limitations

- Cache eviction: Simple limit-based (not LRU)
- No persistence: Cache cleared on restart
- Single-threaded: No parallel queries
- NOT operator: Excludes all-zero rows (correct sparse semantics)

## Planned Features (v2.2+)

- LRU cache eviction
- Persistent cache option
- Mutation methods (set_column, add_rows)
- Multi-threaded query execution
- Query plan optimization
- Custom cache configuration API

## Contributing

This is a research/prototype library. For production use, thorough testing is recommended.

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Authors

SparseTag development team

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.
