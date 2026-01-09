# Requirements Guide

## Overview

SparseTag has two requirements files to separate runtime and development dependencies:

1. **requirements.txt** - Runtime dependencies (minimal, production-ready)
2. **requirements-dev.txt** - Development dependencies (testing, type checking, etc.)

---

## Runtime Dependencies (requirements.txt)

### Installation

```bash
pip install -r requirements.txt
```

### Packages

#### NumPy >= 1.20.0
- **Purpose**: Array operations and numerical computing
- **Why 1.20.0+**: Modern array API, improved performance
- **Recommended**: 2.0+ for better performance and type hints
- **Used for**:
  - Row index arrays in QueryResult
  - Dense array conversions
  - Set operations (intersect1d, union1d, setdiff1d)
  - Random number generation

#### SciPy >= 1.8.0
- **Purpose**: Sparse matrix operations
- **Why 1.8.0+**: Required for `sparse.csc_array` support (new sparse array API)
- **Recommended**: 1.14+ for complete sparse array API
- **Used for**:
  - CSC (Compressed Sparse Column) array storage
  - Sparse matrix operations
  - Backward compatibility with `sparse.spmatrix`
  - Efficient column-wise queries

#### psutil >= 5.8.0
- **Purpose**: System and process utilities
- **Why 5.8.0+**: Cross-platform memory monitoring
- **Used for**:
  - Memory usage tracking (`memory_usage()` method)
  - Cache size monitoring
  - Performance benchmarking

---

## Development Dependencies (requirements-dev.txt)

### Installation

```bash
pip install -r requirements-dev.txt
```

This automatically installs runtime dependencies plus development tools.

### Packages

#### pytest >= 7.0.0
- **Purpose**: Testing framework
- **Used for**:
  - Running 173+ unit tests
  - Test discovery and execution
  - Fixture management

#### pytest-cov >= 4.0.0
- **Purpose**: Code coverage reporting
- **Used for**:
  - Measuring test coverage (currently 85%+)
  - Generating coverage reports
  - Identifying untested code paths

#### mypy >= 1.0.0
- **Purpose**: Static type checking
- **Used for**:
  - Enforcing type safety
  - Catching type errors before runtime
  - Validating Protocol implementations
  - Ensuring scipy sparse array types are correct

---

## Optional Dependencies

### scipy-stubs (Commented in requirements-dev.txt)

```bash
pip install scipy-stubs>=1.14.0
```

- **Purpose**: Type stubs for scipy
- **Note**: We use custom Protocol types instead (see `src/sparse_protocol.py`)
- **When to use**: If you want additional scipy type checking beyond our Protocols

### Code Quality Tools (Commented in requirements-dev.txt)

```bash
pip install black ruff isort
```

- **black**: Code formatter
- **ruff**: Fast Python linter
- **isort**: Import statement organizer

---

## Version Constraints Explained

### Why Minimum Versions?

We use **minimum version constraints** (>=) rather than exact versions to:
1. Allow users to upgrade packages for security patches
2. Maintain compatibility with other packages
3. Avoid dependency conflicts in larger projects

### Why These Specific Minimums?

- **numpy 1.20.0**: First version with modern array API we use
- **scipy 1.8.0**: First version with `sparse.csc_array` (critical for our architecture)
- **psutil 5.8.0**: Stable version with cross-platform memory monitoring
- **pytest 7.0.0**: Modern pytest with improved fixture handling
- **mypy 1.0.0**: Stable mypy release with good Protocol support

### Tested Versions

The library is actively tested with:
- Python 3.10, 3.11, 3.12, 3.13
- NumPy 1.20+ through 2.4+
- SciPy 1.8+ through 1.16+
- psutil 5.8+ through 7.2+

---

## Compatibility Notes

### Python Version

- **Minimum**: Python 3.10
- **Recommended**: Python 3.10+
- **Tested**: Up to Python 3.13

### NumPy 2.0 Compatibility

SparseTag is fully compatible with NumPy 2.0+. The minimum version (1.20.0) allows use with older NumPy if needed, but NumPy 2.0+ is recommended for better performance.

### SciPy Sparse Array Migration

We use both old (`sparse.spmatrix`) and new (`sparse.sparray`) APIs for backward compatibility:
- Input: Accepts both formats
- Internal: Always converts to `sparse.csc_array`
- Output: Returns new sparse array format

---

## Installation Methods

### Method 1: Runtime Only (Minimal)

```bash
# For using SparseTag in your project
pip install -r requirements.txt
```

### Method 2: Development (Full)

```bash
# For developing SparseTag
pip install -r requirements-dev.txt
```

### Method 3: From pyproject.toml

```bash
# Install package with dependencies
pip install .

# Install with dev dependencies
pip install ".[dev]"
```

### Method 4: Editable Install (Development)

```bash
# Install in editable mode for development
pip install -e ".[dev]"
```

---

## Verifying Installation

### Check Runtime Dependencies

```bash
python -c "import numpy; import scipy; import psutil; print('Runtime dependencies OK')"
```

### Check Development Dependencies

```bash
python -c "import pytest; import mypy; print('Dev dependencies OK')"
```

### Run Full Verification

```bash
# Run tests
pytest tests/

# Run type checking
mypy src/

# Check versions
pip list | grep -E "numpy|scipy|psutil|pytest|mypy"
```

---

## Troubleshooting

### Issue: scipy.sparse.csc_array not found

**Solution**: Upgrade scipy to 1.8.0+
```bash
pip install --upgrade scipy>=1.8.0
```

### Issue: mypy errors with scipy types

**Solution**: We handle this with custom Protocols in `src/sparse_protocol.py`. No action needed.

### Issue: NumPy 2.0 compatibility warnings

**Solution**: Update code to use new NumPy API or downgrade to NumPy 1.x if needed. SparseTag supports both.

---

## Adding New Dependencies

### When to Add a Runtime Dependency

Only add to `requirements.txt` if:
1. Required for core functionality
2. No viable standard library alternative
3. Well-maintained and stable
4. Small impact on installation size

### When to Add a Dev Dependency

Add to `requirements-dev.txt` if:
1. Only needed for development/testing
2. Not required by end users
3. Improves development workflow

### Process

1. Test locally with the new dependency
2. Update `requirements.txt` or `requirements-dev.txt`
3. Update `pyproject.toml` dependencies
4. Update this guide
5. Run full test suite
6. Update CI/CD if needed

---

## Related Files

- `requirements.txt` - Runtime dependencies
- `requirements-dev.txt` - Development dependencies
- `pyproject.toml` - Package metadata and dependencies
- `CLAUDE.md` - Development setup instructions
- `CONTRIBUTING.md` - Contribution guidelines
