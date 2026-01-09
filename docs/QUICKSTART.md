# SparseTagging Quick Start

Get started with SparseTagging in 5 minutes.

## Installation

```bash
# Install from PyPI
pip install sparsetagging

# Or install from source
git clone https://github.com/cgbraun/SparseTagging.git
cd SparseTagging
pip install -e .
```

## Basic Usage

```python
from src.sparsetag import SparseTag, TagConfidence

# Create a sparse tag matrix (1000 rows, 3 columns, 5% filled)
tags = SparseTag.create_random(
    n_rows=1000,
    column_names=['Tag1', 'Tag2', 'Tag3'],
    fill_percent=5.0,
    seed=42
)

# Query: Find rows where Tag1 has HIGH confidence
result = tags.query({
    'column': 'Tag1',
    'op': '==',
    'value': TagConfidence.HIGH
})

print(f"Found {result.count} rows with HIGH confidence in Tag1")
print(f"Row indices: {result.indices[:10]}")  # First 10 matches

# Multi-column query: Tag1 >= MEDIUM AND Tag2 == HIGH
result = tags.query({
    'operator': 'AND',
    'conditions': [
        {'column': 'Tag1', 'op': '>=', 'value': TagConfidence.MEDIUM},
        {'column': 'Tag2', 'op': '==', 'value': TagConfidence.HIGH}
    ]
})

print(f"Complex query found {result.count} rows")
```

## Key Features

- **95% memory savings** - Sparse storage for tag confidence data
- **100-170x speedups** - Intelligent query caching
- **Type-safe** - Full type hint coverage with mypy strict mode
- **Production-ready** - 177 tests with 85%+ coverage

## Next Steps

- **[Full Documentation](README.md)** - Complete guide to all features
- **[Architecture](ARCHITECTURE.md)** - Understand the design
- **[Docker Usage](docker-usage.md)** - Container deployment
- **[Performance Guide](PERFORMANCE.md)** - Benchmarks and optimization

## Common Queries

```python
# Single column equality
tags.query({'column': 'Tag1', 'op': '==', 'value': TagConfidence.LOW})

# Greater than or equal
tags.query({'column': 'Tag2', 'op': '>=', 'value': TagConfidence.MEDIUM})

# IN operator (multiple values)
tags.query({'column': 'Tag3', 'op': 'IN', 'values': [TagConfidence.HIGH, TagConfidence.MEDIUM]})

# NOT operator (excludes matching rows)
tags.query({'operator': 'NOT', 'conditions': [{'column': 'Tag1', 'op': '==', 'value': TagConfidence.LOW}]})

# OR operator
tags.query({
    'operator': 'OR',
    'conditions': [
        {'column': 'Tag1', 'op': '==', 'value': TagConfidence.HIGH},
        {'column': 'Tag2', 'op': '==', 'value': TagConfidence.HIGH}
    ]
})
```

## Support

- **Issues:** https://github.com/cgbraun/SparseTagging/issues
- **Security:** noreply@sparsetag.org

---

**Version:** 2.4.1
