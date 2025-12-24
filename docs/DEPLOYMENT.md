# Deployment Guide

## Production Installation

### Standard Installation

```bash
pip install sparsetagging
```

### Development Installation

```bash
git clone https://github.com/your-org/sparsetagging.git
cd sparsetagging
pip install -e .
```

### With Optional Dependencies

```bash
# Testing tools
pip install sparsetagging[dev]

# Specific versions
pip install "sparsetagging>=2.4.0,<3.0.0"
```

## Requirements

- **Python**: ≥3.9
- **NumPy**: ≥1.20.0
- **SciPy**: ≥1.7.0
- **psutil**: ≥5.8.0 (for memory monitoring)

## Performance Tuning

### Cache Configuration

**Interactive Dashboards** (enable caching):
```python
bt = SparseTag.create_random(
    n_rows=1000000,
    column_names=['Tag1', 'Tag2', 'Tag3'],
    fill_percent=0.01,
    enable_cache=True  # Enable for repeated queries
)
```

**Batch Processing** (disable caching to save memory):
```python
bt = SparseTag.from_array(
    data_array,
    column_names=['Tag1', 'Tag2'],
    enable_cache=False  # Disable for one-time queries
)
```

**Custom Cache Limits**:
```python
from src.cache_manager import QueryCacheManager

bt = SparseTag.from_sparse(sparse_matrix, column_names)
bt._cache_manager = QueryCacheManager(
    max_entries=512,        # Double default
    max_memory_mb=20.0,     # Double default
    large_result_threshold_mb=2.0  # Larger results cached
)
```

### Memory Optimization

**Optimize Index Dtype** (for datasets with <65K rows):
```python
bt = SparseTag.create_random(50000, ['Tag1', 'Tag2'], 0.01)

# Check potential savings
memory_before = bt.memory_usage()['indices']

# Optimize in-place
bt.optimize_indices_dtype(inplace=True)

memory_after = bt.memory_usage()['indices']
savings = (memory_before - memory_after) / memory_before * 100
print(f"Saved {savings:.1f}% indices memory")
```

**Memory Monitoring**:
```python
# Track memory usage
stats = bt.memory_usage()
print(f"Total: {stats['total'] / 1024**2:.2f} MB")
print(f"Data: {stats['data'] / 1024**2:.2f} MB")
print(f"Indices: {stats['indices'] / 1024**2:.2f} MB")

# Check cache memory
cache_stats = bt.cache_stats()
print(f"Cache: {cache_stats['size_mb']:.2f} MB")
```

**Sparsity Threshold**:
```python
# Only use sparse format if sparsity > 50%
if bt.sparsity > 0.5:
    # Use sparse operations
    result = bt.query(query_dict)
else:
    # Consider dense format for very dense data
    dense = bt.to_dense()
```

### Query Optimization

**Use IN operator** for multi-value queries:
```python
# GOOD: Single IN operation
query = {
    'column': 'Tag1',
    'op': 'IN',
    'values': [TagConfidence.HIGH, TagConfidence.MEDIUM]
}

# AVOID: Multiple OR conditions
query = {
    'operator': 'OR',
    'conditions': [
        {'column': 'Tag1', 'op': '==', 'value': TagConfidence.HIGH},
        {'column': 'Tag1', 'op': '==', 'value': TagConfidence.MEDIUM}
    ]
}
```

**Combine conditions efficiently**:
```python
# GOOD: AND before OR for faster short-circuit
query = {
    'operator': 'AND',
    'conditions': [
        {'column': 'Tag1', 'op': '>=', 'value': TagConfidence.MEDIUM},  # Selective
        {'column': 'Tag2', 'op': '==', 'value': TagConfidence.HIGH}      # Very selective
    ]
}

# AVOID: OR of ANDs (slower)
query = {
    'operator': 'OR',
    'conditions': [
        {
            'operator': 'AND',
            'conditions': [...]
        },
        # ...
    ]
}
```

**Avoid querying for NONE values**:
```python
# AVOID: Creates dense matrix in memory
query = {'column': 'Tag1', 'op': '==', 'value': TagConfidence.NONE}

# GOOD: Query for non-zero values instead
query = {'column': 'Tag1', 'op': 'IN', 'values': [
    TagConfidence.LOW, TagConfidence.MEDIUM, TagConfidence.HIGH
]}
```

## Monitoring

### Key Metrics to Track

**Cache Performance**:
```python
stats = bt.cache_stats()

# Target hit rate: >60% for interactive workloads
if stats['hit_rate'] < 0.6:
    print("Warning: Low cache hit rate")

# Monitor cache size
if stats['size_mb'] > 8.0:
    print("Info: Cache approaching limit")
```

**Memory Growth**:
```python
import psutil
import os

process = psutil.Process(os.getpid())

# Before operation
mem_before = process.memory_info().rss / 1024**2

# Perform operations
result = bt.query(query_dict)

# After operation
mem_after = process.memory_info().rss / 1024**2
growth = mem_after - mem_before

if growth > 100:  # 100MB threshold
    print(f"Warning: Memory grew by {growth:.1f} MB")
```

**Query Performance**:
```python
import time

# Time query execution
start = time.perf_counter()
result = bt.query(query_dict)
elapsed_ms = (time.perf_counter() - start) * 1000

print(f"Query time: {elapsed_ms:.2f}ms")
print(f"Matches: {result.count}")

# Target: <1ms for cached queries, <10ms for uncached
if elapsed_ms > 10:
    print("Warning: Slow query detected")
```

## Troubleshooting

### High Memory Usage

**Symptom**: Process memory growing unexpectedly

**Solutions**:
1. Clear cache periodically:
   ```python
   bt.clear_cache()
   ```

2. Optimize index dtype:
   ```python
   bt.optimize_indices_dtype(inplace=True)
   ```

3. Disable caching for one-time queries:
   ```python
   result = bt.query(query_dict, use_cache=False)
   ```

4. Reduce cache limits:
   ```python
   bt._cache_manager = QueryCacheManager(
       max_entries=128,     # Halve default
       max_memory_mb=5.0    # Halve default
   )
   ```

### Slow Queries

**Symptom**: Queries taking >10ms uncached

**Diagnosis**:
```python
print(f"Sparsity: {bt.sparsity:.2%}")
print(f"Non-zeros: {bt.nnz:,}")
print(f"Shape: {bt.shape}")

# Low sparsity = slower queries
if bt.sparsity < 0.5:
    print("Warning: Low sparsity, consider dense format")
```

**Solutions**:
1. Enable caching for repeated queries:
   ```python
   bt = SparseTag(..., enable_cache=True)
   ```

2. Simplify query structure:
   ```python
   # Use simpler operators when possible
   # Avoid deep nesting
   ```

3. Check if data is too dense:
   ```python
   if bt.sparsity < 0.3:
       # Consider using dense arrays instead
       dense = bt.to_dense()
   ```

### Type Errors

**Symptom**: mypy or runtime type errors

**Solutions**:
1. Run mypy to catch issues early:
   ```bash
   mypy src/sparsetag.py src/cache_manager.py
   ```

2. Use type guard for conversions:
   ```python
   value = bt._ensure_tag_confidence(raw_value)
   ```

3. Check query dictionary structure:
   ```python
   # GOOD: Properly structured
   query = {
       'column': 'Tag1',
       'op': '==',
       'value': TagConfidence.HIGH
   }

   # BAD: Missing required fields
   query = {'column': 'Tag1'}  # Missing 'op' and 'value'
   ```

## Scaling Considerations

### Large Datasets (1M+ rows)

**Recommendations**:
- Use `fill_percent < 0.01` for create_random
- Call `optimize_indices_dtype()` if rows < 65K
- Monitor memory with `memory_usage()`
- Consider batching queries

**Example**:
```python
# Large sparse dataset
bt = SparseTag.create_random(
    n_rows=10_000_000,
    column_names=['Tag1', 'Tag2', 'Tag3'],
    fill_percent=0.001,  # 0.1% density
    seed=42,
    enable_cache=True
)

# Optimize if possible
if bt.shape[0] < 65536:
    bt.optimize_indices_dtype(inplace=True)

# Check memory footprint
print(f"Memory: {bt.memory_usage()['total'] / 1024**3:.2f} GB")
```

### High Query Volume

**Strategies**:
1. **Enable caching**:
   ```python
   enable_cache=True
   ```

2. **Increase cache limits** (if memory available):
   ```python
   bt._cache_manager = QueryCacheManager(
       max_entries=1024,
       max_memory_mb=50.0
   )
   ```

3. **Monitor cache hit rate**:
   ```python
   stats = bt.cache_stats()
   if stats['hit_rate'] < 0.5:
       print("Consider increasing cache limits")
   ```

### Distributed Systems

**Serialization**:
```python
import pickle

# Serialize SparseTag
with open('sparsetag.pkl', 'wb') as f:
    pickle.dump(bt, f)

# Deserialize in another process
with open('sparsetag.pkl', 'rb') as f:
    bt = pickle.load(f)
```

**Considerations**:
- Use process-local SparseTag instances (not thread-safe)
- Consider readonly cache for workers
- Serialize data separately from cache

**Multi-Process Example**:
```python
from multiprocessing import Pool

def process_partition(data_slice):
    bt = SparseTag.from_array(data_slice, column_names)
    results = []
    for query in queries:
        result = bt.query(query)
        results.append(result.count)
    return results

# Partition data and process in parallel
with Pool(processes=4) as pool:
    results = pool.map(process_partition, data_partitions)
```

## Production Checklist

### Before Deployment

- [ ] All tests pass (`pytest tests/`)
- [ ] Type checking passes (`mypy src/`)
- [ ] Coverage ≥85% (`pytest --cov=src tests/`)
- [ ] Performance benchmarks run (`python src/benchmark.py`)
- [ ] Memory profiling completed
- [ ] Cache strategy determined
- [ ] Monitoring configured

### Configuration Review

- [ ] Cache enabled/disabled appropriately
- [ ] Memory limits set based on available resources
- [ ] Index dtype optimization applied if applicable
- [ ] Logging configured (see below)

### Logging Configuration

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sparsetag.log'),
        logging.StreamHandler()
    ]
)

# Adjust SparseTag logging level
logging.getLogger('src.sparsetag').setLevel(logging.DEBUG)
logging.getLogger('src.cache_manager').setLevel(logging.INFO)
```

## Environment Variables

**Optional environment variables** for tuning:

```bash
# Set Python hash seed for reproducibility
export PYTHONHASHSEED=42

# NumPy thread control
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4

# Memory allocation
export MALLOC_TRIM_THRESHOLD_=100000
```

## Security Considerations

1. **Input Validation**: All inputs validated before processing
2. **No SQL Injection**: Pure Python operations, no SQL
3. **No Code Execution**: Queries are data, not code
4. **Pickle Security**: Be cautious with unpickle from untrusted sources

## Support

For production issues:
1. Check [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) (if exists)
2. Review logs for warnings/errors
3. Run diagnostics:
   ```python
   print(bt.memory_usage())
   print(bt.cache_stats())
   print(f"Sparsity: {bt.sparsity:.2%}")
   ```
4. Open issue on GitHub with:
   - Python version
   - Package versions (`pip freeze`)
   - Reproducible example
   - Error messages/stack traces
