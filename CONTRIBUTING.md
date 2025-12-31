# Contributing to SparseTag

## Development Setup

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate environment:
   - Windows: `.venv\Scripts\activate`
   - Unix/Mac: `source .venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Install dev dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
6. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

   This will automatically run quality checks before each commit:
   - Ruff formatting and linting
   - Mypy type checking
   - Pytest tests with coverage

   To run checks manually without committing:
   ```bash
   pre-commit run --all-files
   ```

   To skip pre-commit hooks (not recommended):
   ```bash
   git commit --no-verify
   ```

## Running Tests

```bash
# Run all tests
pytest tests/

# With coverage report
pytest --cov=src tests/

# Generate HTML coverage report
pytest --cov=src --cov-report=html tests/

# Open coverage report
# Windows: start htmlcov\index.html
# Mac: open htmlcov/index.html
# Linux: xdg-open htmlcov/index.html
```

## Type Checking

```bash
# Check core modules
mypy src/sparsetag.py src/cache_manager.py src/exceptions.py

# Check all source files
mypy src/
```

## Performance Testing

```bash
cd src
python benchmark.py
```

Benchmark results are saved to `reports/` directory (gitignored).

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Add docstrings to all public methods (Google style)
- Maximum line length: 100 characters
- Use custom exceptions from `src/exceptions.py`

### Example Docstring

```python
def example_method(self, value: int, name: str) -> Dict[str, Any]:
    """
    Brief one-line description.

    Longer description if needed, explaining the method's purpose,
    behavior, and any important implementation details.

    Args:
        value: Description of value parameter
        name: Description of name parameter

    Returns:
        Description of return value

    Raises:
        ValueError: When value is negative
        KeyError: When name is not found

    Example:
        >>> obj.example_method(42, "test")
        {'result': 'success'}
    """
```

## Testing Guidelines

- Maintain ≥85% test coverage
- Write tests for all new features
- Include edge cases and error conditions
- Use descriptive test names following pattern: `test_<method>_<scenario>`
- Group related tests in classes

### Test Structure

```python
class TestFeatureName:
    """Test suite for feature X."""

    def test_basic_functionality(self):
        """Test normal operation."""
        # Arrange
        bt = SparseTag.create_random(100, ['Tag1'], 0.1, seed=42)

        # Act
        result = bt.query({'column': 'Tag1', 'op': '==', 'value': TagConfidence.HIGH})

        # Assert
        assert result.count > 0

    def test_error_handling(self):
        """Test error conditions."""
        bt = SparseTag.create_random(100, ['Tag1'], 0.1)

        with pytest.raises(InvalidColumnError):
            bt.query({'column': 'NonExistent', 'op': '==', 'value': TagConfidence.HIGH})
```

## Quality Requirements

All pull requests must pass these automated checks:

### Code Quality (Pre-commit Hooks)
- ✅ Ruff linting (zero errors)
- ✅ Ruff formatting (black-compatible)
- ✅ Mypy type checking (strict mode, zero errors)
- ✅ Pytest (all 177 tests pass, ≥85% coverage)

### Code Quality (CI Pipeline)
- ✅ SonarCloud Quality Gate (must pass)
  - Security Rating: A (zero vulnerabilities)
  - Coverage: ≥90% for new code
  - Cognitive Complexity: ≤15 per function
  - Code Duplication: ≤3%

### Security
- ✅ No BLOCKER or CRITICAL issues
- ✅ All Security Hotspots reviewed
- ✅ No known CVEs in dependencies

### Pull Request Checklist

Before requesting review:
- [ ] Pre-commit hooks pass locally
- [ ] Tests added for new functionality
- [ ] Documentation updated (docstrings, README, etc.)
- [ ] CI pipeline passes (all jobs green)
- [ ] SonarCloud Quality Gate passes
- [ ] No merge conflicts with main

If SonarCloud reports issues:
1. Click "Details" on failed check
2. Review issues in SonarCloud dashboard
3. Fix BLOCKER/CRITICAL issues (required)
4. Fix or justify MAJOR issues
5. Consider fixing MINOR issues (optional)

## Submitting Changes

1. Create feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make changes with tests:
   - Add/modify code
   - Write/update tests
   - Update docstrings

3. Ensure quality checks pass:

   Pre-commit hooks will run automatically, but you can also run manually:

   ```bash
   # Run all pre-commit checks
   pre-commit run --all-files

   # Or run individual tools
   ruff check src/ tests/        # Linting
   ruff format src/ tests/        # Formatting
   mypy src/                      # Type checking
   pytest tests/ --cov=src        # Tests + coverage
   ```

   All checks must pass before merging.

4. Update CHANGELOG.md:
   - Add entry under `[Unreleased]` section
   - Follow format: `- [Added/Changed/Fixed/Removed]: Description (#issue)`

5. Commit changes:
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

6. Push and create pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

## Pull Request Guidelines

- Provide clear description of changes
- Reference related issues
- Include test results
- Update documentation
- Ensure CI passes

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Performance improvement
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] All tests pass
- [ ] Coverage maintained (≥85%)
- [ ] Type checking passes (mypy)

## Checklist
- [ ] Updated CHANGELOG.md
- [ ] Added/updated tests
- [ ] Added/updated docstrings
- [ ] Verified performance unchanged
```

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md with release date
3. Run full test suite
4. Create git tag: `git tag v2.4.0`
5. Push tag: `git push origin v2.4.0`

## Getting Help

- Check [CLAUDE.md](CLAUDE.md) for development guidelines
- Review [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for design decisions
- See [QUICKSTART.md](QUICKSTART.md) for usage examples

## Code of Conduct

- Be respectful and professional
- Provide constructive feedback
- Focus on code quality and maintainability
- Help others learn and grow
