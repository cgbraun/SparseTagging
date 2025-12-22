# BaseTag Quick Start Guide

Get started with BaseTag in 5 minutes.

## Installation (30 seconds)

```bash
pip install numpy scipy psutil
cd basetag_v2.1_package/src
```

## Your First Query (2 minutes)

```python
from basetag import BaseTag, TagConfidence

# Create a sparse matrix with tag confidence data
bt = BaseTag.create_random(
    n_rows=100_000,           # 100K rows
    column_names=['Toxicity', 'Spam', 'Profanity'],
    fill_percent=0.01,        # 99% sparse
    seed=42,
    enable_cache=True         # Enable caching
)

print(f"Matrix shape: {bt.shape}")
print(f"Sparsity: {bt.sparsity:.1f}%")

# Simple query: Find high toxicity
result = bt.query({
    'column': 'Toxicity',
    'op': '==',
    'value': TagConfidence.HIGH
})

print(f"Found {result.count} rows with high toxicity")
print(f"Row indices: {result.indices[:10]}")  # First 10 matches
```

## Multi-Column Query (1 minute)

```python
# Find rows that are high toxicity AND medium+ spam
result = bt.query({
    'operator': 'AND',
    'conditions': [
        {'column': 'Toxicity', 'op': '==', 'value': TagConfidence.HIGH},
        {'column': 'Spam', 'op': '>=', 'value': TagConfidence.MEDIUM}
    ]
})

print(f"High toxicity + medium+ spam: {result.count} rows")
```

## Cache Performance Demo (1 minute)

```python
import time

# First query (cache miss)
t1 = time.perf_counter()
result = bt.query({'column': 'Toxicity', 'op': '==', 'value': TagConfidence.HIGH})
time_miss = (time.perf_counter() - t1) * 1000

# Second query (cache hit)
t2 = time.perf_counter()
result = bt.query({'column': 'Toxicity', 'op': '==', 'value': TagConfidence.HIGH})
time_hit = (time.perf_counter() - t2) * 1000

print(f"First query (miss): {time_miss:.3f}ms")
print(f"Second query (hit): {time_hit:.3f}ms")
print(f"Speedup: {time_miss/time_hit:.1f}x")

# Check cache statistics
stats = bt.cache_stats()
print(f"Cache hit rate: {stats['hit_rate']:.1%}")
```

## Memory Optimization (30 seconds)

```python
# Check memory usage
mem = bt.memory_usage()
print(f"Total memory: {mem['total']/1024:.1f} KB")
print(f"Indices: {mem['indices']/1024:.1f} KB")

# Optimize for smaller matrices (<65K rows)
if bt.shape[0] < 65536:
    bt.optimize_indices_dtype()  # Saves 50% indices memory
    mem_after = bt.memory_usage()
    print(f"Optimized indices: {mem_after['indices']/1024:.1f} KB")
```

## Common Operations Reference

### Query Operators

```python
# Equality
bt.query({'column': 'Toxicity', 'op': '==', 'value': TagConfidence.HIGH})

# Comparison
bt.query({'column': 'Spam', 'op': '>', 'value': TagConfidence.LOW})
bt.query({'column': 'Spam', 'op': '>=', 'value': TagConfidence.MEDIUM})

# IN operator
bt.query({'column': 'Toxicity', 'op': 'IN', 'values': [TagConfidence.HIGH, TagConfidence.MEDIUM]})
```

### Multi-Column Queries

```python
# AND
bt.query({
    'operator': 'AND',
    'conditions': [
        {'column': 'Toxicity', 'op': '==', 'value': TagConfidence.HIGH},
        {'column': 'Spam', 'op': '>=', 'value': TagConfidence.MEDIUM}
    ]
})

# OR
bt.query({
    'operator': 'OR',
    'conditions': [
        {'column': 'Toxicity', 'op': '==', 'value': TagConfidence.HIGH},
        {'column': 'Profanity', 'op': '==', 'value': TagConfidence.HIGH}
    ]
})

# NOT (excludes rows with all zeros)
bt.query({
    'operator': 'NOT',
    'conditions': [
        {'column': 'Spam', 'op': '==', 'value': TagConfidence.LOW}
    ]
})
```

### Working with Results

```python
result = bt.query({'column': 'Toxicity', 'op': '==', 'value': TagConfidence.HIGH})

# Get count
print(f"Matches: {result.count}")

# Get row indices
print(f"Indices: {result.indices}")

# Get filtered data as array
filtered_data = result.to_array(dense=False)  # Sparse
filtered_data = result.to_array(dense=True)   # Dense

# Get specific column from results
toxicity_values = result.get_column('Toxicity', dense=True)
```

### Cache Management

```python
# Check cache statistics
stats = bt.cache_stats()
print(f"Hits: {stats['hits']}")
print(f"Misses: {stats['misses']}")
print(f"Hit rate: {stats['hit_rate']:.1%}")
print(f"Memory: {stats['size_mb']:.3f} MB")

# Clear cache manually
bt.clear_cache()

# Disable cache for specific query
result = bt.query(query_dict, use_cache=False)
```

## Tag Confidence Values

```python
from basetag import TagConfidence

TagConfidence.NONE = 0      # No confidence / no data
TagConfidence.LOW = 1       # Low confidence
TagConfidence.MEDIUM = 2    # Medium confidence
TagConfidence.HIGH = 3      # High confidence
```

## Next Steps

- Read [README.md](README.md) for complete API documentation
- Run benchmarks: `python src/benchmark.py`
- Check [CHANGELOG.md](CHANGELOG.md) for version history
- Review performance reports in `docs/` directory

## Quick Reference Card

| Operation | Code |
|-----------|------|
| Create | `BaseTag.create_random(n, cols, 0.01, enable_cache=True)` |
| Query | `bt.query({'column': 'Tag1', 'op': '==', 'value': 3})` |
| Cache stats | `bt.cache_stats()` |
| Clear cache | `bt.clear_cache()` |
| Memory | `bt.memory_usage()` |
| Optimize | `bt.optimize_indices_dtype()` |
| To dense | `bt.to_dense()` |

## Common Pitfalls

### NOT Operator Semantics

```python
# ❌ Wrong assumption: NOT includes all rows
# NOT(Tag == LOW) returns ALL rows where Tag != LOW, including zeros

# ✅ Correct: NOT excludes rows with all zeros
# NOT(Tag == LOW) returns rows WITH DATA where Tag != LOW
# Rows with all zeros (no tag confidence) are excluded
```

### Cache Overhead

```python
# ❌ Enabling cache for all-unique queries hurts performance
bt = BaseTag.create_random(1000, ['Tag1'], 0.01, enable_cache=True)
for i in range(1000):
    bt.query({'column': 'Tag1', 'op': '==', 'value': i})  # All unique

# ✅ Disable cache if queries don't repeat
bt = BaseTag.create_random(1000, ['Tag1'], 0.01, enable_cache=False)
```

### Memory for Large Result Sets

```python
# ⚠️ Large results (>1MB) aren't cached by default
result = bt.query({'operator': 'NOT', ...})  # Returns 600K+ rows
# This won't be cached even with cache enabled

# ✓ Use specific conditions for cacheable results
result = bt.query({'column': 'Tag1', 'op': '==', 'value': 3})  # ~3K rows
```

## Performance Tips

1. **Enable caching** for interactive workloads
2. **Use indices optimization** for matrices <65K rows
3. **Batch similar queries** to improve cache hit rate
4. **Monitor memory** with `memory_usage()`
5. **Benchmark first** - run on your data before deploying

---

**Ready to dive deeper?** Check out [README.md](README.md) for the complete documentation.
