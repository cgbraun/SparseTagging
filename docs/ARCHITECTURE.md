# SparseTag Architecture

## Design Principles

1. **Performance First**: Direct sparse matrix operations, no dense conversion
2. **Memory Efficient**: CSC format + intelligent caching
3. **Type Safe**: Complete type hint coverage with mypy validation
4. **Maintainable**: Clear separation of concerns with modular design

## Core Components

### SparseTag Class
- **Purpose**: Main sparse matrix container for tag confidence data
- **Location**: `src/sparsetag.py:171-900`
- **Responsibilities**:
  - Data storage in sparse CSC format
  - Query execution and optimization
  - Data validation and integrity
  - Cache invalidation coordination

**Key Methods**:
- `query()`: Execute queries with optional caching
- `create_random()`: Factory for test data
- `from_array()`, `from_sparse()`: Data conversion
- `optimize_indices_dtype()`: Memory optimization

### QueryCacheManager
- **Purpose**: Query result caching with memory bounds
- **Location**: `src/cache_manager.py`
- **Features**:
  - MD5-based cache key generation
  - Memory-bounded storage (256 entries, 10MB max)
  - Hit/miss statistics tracking
  - Automatic size calculation

**Key Methods**:
- `get()`: Retrieve cached result
- `put()`: Store result if within bounds
- `clear()`: Invalidate all cached entries
- `stats()`: Performance metrics

### QueryResult Class
- **Purpose**: Encapsulates query results with lazy evaluation
- **Location**: `src/sparsetag.py:115-169`
- **Pattern**: Lazy mask computation for memory efficiency
- **Properties**:
  - `indices`: Matching row indices (primary storage)
  - `count`: Number of matches
  - `mask`: Boolean array (computed on demand)
- **Methods**:
  - `to_sparsetag()`: Convert result to new SparseTag instance

### TagConfidence Enum
- **Purpose**: Type-safe confidence levels
- **Location**: `src/sparsetag.py:102-113`
- **Values**:
  - `NONE = 0`: No tag confidence (implicit zero in sparse)
  - `LOW = 1`: Low confidence
  - `MEDIUM = 2`: Medium confidence
  - `HIGH = 3`: High confidence

**Design Choice**: IntEnum allows direct numeric comparisons while maintaining type safety.

## Query Engine

### Architecture Overview

```
Query Dict → Parse → Optimize → Execute → Cache → QueryResult
             │        │          │         │
             │        │          │         └─ QueryCacheManager
             │        │          └─ _evaluate_query_optimized()
             │        └─ _transform_comparison()
             └─ Validation (exceptions.py)
```

### Single-Column Queries
- **Implementation**: Direct CSC sparse column access
- **Time Complexity**: O(nnz_column) where nnz = non-zero count
- **Pattern**: Extract column → Filter values → Return row indices

**Example**:
```python
query = {'column': 'Tag1', 'op': '==', 'value': TagConfidence.HIGH}
# Accesses: self._data.data[col_start:col_end]
# Filters: col_values == HIGH
# Returns: col_row_indices[matching_mask]
```

### Multi-Column Queries
- **Implementation**: NumPy set operations (intersect1d, union1d, setdiff1d)
- **Optimization**: Recursive evaluation with short-circuit
- **Operators**:
  - `AND`: Intersection of result sets
  - `OR`: Union of result sets (concatenate + unique)
  - `NOT`: Difference from universe of rows with data

**Example**:
```python
query = {
    'operator': 'AND',
    'conditions': [
        {'column': 'Tag1', 'op': '>=', 'value': TagConfidence.MEDIUM},
        {'column': 'Tag2', 'op': '==', 'value': TagConfidence.HIGH}
    ]
}
# Step 1: Evaluate both conditions → [array1, array2]
# Step 2: Intersect: np.intersect1d(array1, array2)
# Step 3: Return sorted unique indices
```

### NOT Operator Semantics

**Critical Design Decision**: NOT operates only on rows with ANY non-zero value.

**Rationale**:
- Zero in sparse matrix = "no data" or "no tag confidence"
- `NOT(condition)` = "has data but doesn't match condition"
- Rows with all zeros are excluded (they have no tag confidence)

**Implementation**:
```python
universe = self._get_rows_with_any_data()  # Rows with ≥1 non-zero
result = np.setdiff1d(universe, matching_rows)
```

**Example**:
```python
# Matrix with 5 rows:
# Row 0: [0, 0] → all zeros, excluded from NOT
# Row 1: [LOW, NONE] → has data
# Row 2: [HIGH, MEDIUM] → has data
# Row 3: [0, 0] → all zeros, excluded from NOT
# Row 4: [NONE, LOW] → has data

# Query: NOT(Tag1 == HIGH)
# Universe: [1, 2, 4] (rows with data)
# Matches Tag1==HIGH: [2]
# Result: [1, 4] (universe - matches)
```

This differs from naive NOT which would incorrectly include all-zero rows [0, 3].

### Query Optimization

**Comparison → IN Transformation**:
```python
# Query: Tag1 >= MEDIUM
# Transformed to: Tag1 IN {MEDIUM, HIGH}
# Benefit: Single isin() operation instead of multiple comparisons
```

**Empty Result Short-Circuit**:
```python
if operator == 'AND':
    for arr in row_arrays:
        if len(result) == 0:
            break  # No need to continue
        result = np.intersect1d(result, arr)
```

## Cache System

### Caching Strategy

**Key Generation**:
- Simple queries: Fast string-based hashing (`"col|op|value"`)
- Complex queries: JSON serialization with custom encoder
- Result: MD5 hash (32-character hex string)

**Storage**:
- Dictionary: `{cache_key: QueryResult}`
- Memory tracking: Incremental O(1) updates
- Bounds: Max 256 entries OR 10MB total

**Eviction**: None (fills to limit then stops caching new results)

### Cache Invalidation

**Automatic Triggers**:
- Data property setter: `self._data = new_data`
- Methods decorated with `@invalidates_cache`
- Version counter: `self._data_version` increments

**Implementation**:
```python
@invalidates_cache
def some_mutation_method(self):
    # ... modify data ...
    # Decorator automatically calls self._invalidate_cache()
```

**Design Trade-off**: Simple invalidate-all strategy preferred over complex cache coherence.

## Memory Management

### Sparse Format (CSC - Compressed Sparse Column)

**Data Structure**:
```python
_data = sparse.csc_array([
    data:    [1, 3, 2, 1, ...]  # uint8, non-zero values only
    indices: [0, 5, 7, 10, ...] # int32/int16, row indices
    indptr:  [0, 2, 5, 7, ...]  # int32/int16, column pointers
])
```

**Memory Calculation**:
```
Total = data.nbytes + indices.nbytes + indptr.nbytes + metadata
      = (nnz × 1) + (nnz × 2) + (ncols+1 × 2) + overhead
```

### Optimization: Index Dtype Conversion

**Trigger**: `optimize_indices_dtype()`

**Logic**:
```python
if n_rows < 256:
    dtype = int8  # Saves 75% indices memory
elif n_rows < 65536:
    dtype = int16  # Saves 50% indices memory
else:
    dtype = int32  # No optimization
```

**Safety**: Validates actual index values before conversion to prevent overflow.

## Extension Points

### 1. Custom Cache Backend
```python
class RedisCacheManager(QueryCacheManager):
    def __init__(self, redis_client):
        self.redis = redis_client

    def get(self, query_dict):
        key = self._generate_key(query_dict)
        return self.redis.get(key)

# Usage:
bt = SparseTag(..., enable_cache=False)
bt._cache_manager = RedisCacheManager(redis_client)
```

### 2. Custom Query Operators
```python
# In _transform_comparison():
elif op == 'BETWEEN':
    result = {v for v in valid if low <= v <= high}
```

### 3. Additional Factory Methods
```python
@classmethod
def from_parquet(cls, path: str, column_names: List[str]) -> 'SparseTag':
    """Load from Parquet file."""
    # ... implementation ...
```

### 4. Custom Serialization
```python
def to_hdf5(self, path: str) -> None:
    """Save to HDF5 format."""
    import h5py
    with h5py.File(path, 'w') as f:
        f.create_dataset('data', data=self._data.data)
        # ... save other components ...
```

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Single-column query | O(nnz_col) | Direct sparse access |
| Multi-column AND | O(nnz_total) | Intersection operations |
| Multi-column OR | O(nnz_total) | Union + unique |
| NOT operator | O(nnz_total) | Universe calculation |
| Cache lookup | O(1) | Dict access |
| Cache key gen (simple) | O(1) | String concatenation |
| Cache key gen (complex) | O(n) | JSON serialization |

### Space Complexity

| Component | Size | Formula |
|-----------|------|---------|
| Sparse data | nnz × 1 byte | uint8 values |
| Sparse indices | nnz × 2-4 bytes | int16/int32 |
| Sparse indptr | (ncols+1) × 2-4 bytes | int16/int32 |
| Cache | varies | ≤10MB (configurable) |
| Metadata | ~1KB | Column names, dicts |

### Scaling Behavior

**Tested Configurations**:
- 1M rows × 100 cols × 1% sparsity = ~1M non-zeros
- Query time: 0.19ms (uncached), 0.009ms (cached)
- Memory: 10MB sparse vs 950MB dense (95% savings)

## Error Handling

### Exception Hierarchy

```
SparseTagError
├── ValidationError (ValueError)
│   ├── MatrixSizeError
│   └── DataIntegrityError
└── QueryError
    ├── InvalidQueryStructureError (ValueError)
    ├── InvalidColumnError (KeyError)
    ├── InvalidOperatorError (ValueError)
    └── InvalidValueError (ValueError)
```

**Design**: Multiple inheritance from base exceptions (ValueError, KeyError) ensures backward compatibility.

## Thread Safety

**Current State**: Not thread-safe

**Concerns**:
- Cache dictionary: Concurrent puts could corrupt state
- Data version counter: Race conditions
- Query execution: Read-only (thread-safe)

**Future**: Consider adding locks for cache operations if needed.

## Testing Strategy

### Test Categories

1. **Critical Bugs** (`test_critical_bugs.py`):
   - Index dtype overflow protection
   - Thread-safe random generation
   - JSON serialization edge cases

2. **Data Integrity** (`test_data_integrity.py`):
   - Immutability guarantees
   - Cache invalidation correctness
   - Sparsity consistency

3. **Edge Cases** (`test_edge_cases.py`):
   - Empty matrices
   - Single row/column
   - Extreme sparsity/density
   - Dtype boundaries

4. **Error Handling** (`test_error_handling.py`):
   - Invalid inputs
   - Malformed queries
   - Exception types

5. **Integration** (`test_integration.py`):
   - End-to-end workflows
   - Real-world scenarios
   - Performance validation

6. **Query Operations** (`test_query_operations.py`):
   - All operators (==, !=, >, >=, <, <=, IN)
   - Logical operations (AND, OR, NOT)
   - Nested queries

### Coverage Target

- **Minimum**: 85%
- **Current**: ~88%
- **Strategy**: Focus on critical paths and error conditions

## Future Improvements

### Short-Term
- LRU cache eviction policy
- Persistent cache option (disk/Redis)
- Parallel query execution (ThreadPoolExecutor)

### Medium-Term
- Mutation methods (set_column, add_rows, delete_rows)
- Query plan optimization (reorder AND conditions)
- Compressed indices (bit packing)

### Long-Term
- Distributed query execution
- GPU acceleration (CuPy)
- Incremental updates with version vectors
- SIMD optimizations

## References

- **Sparse Matrix Format**: [scipy.sparse documentation](https://docs.scipy.org/doc/scipy/reference/sparse.html)
- **NumPy Set Operations**: [numpy.intersect1d](https://numpy.org/doc/stable/reference/generated/numpy.intersect1d.html)
- **Type Hints**: [PEP 484](https://peps.python.org/pep-0484/)
- **Packaging**: [PEP 561](https://peps.python.org/pep-0561/)
