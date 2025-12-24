"""Custom exceptions for SparseTag library."""


class SparseTagError(Exception):
    """Base exception for all SparseTag errors."""
    pass


class ValidationError(SparseTagError, ValueError):
    """Raised when input validation fails. Inherits from ValueError for backward compatibility."""
    pass


class QueryError(SparseTagError):
    """Raised when query execution fails."""
    pass


class InvalidQueryStructureError(QueryError, ValueError):
    """Raised when query dictionary structure is invalid."""
    pass


class InvalidColumnError(QueryError, KeyError):
    """Raised when column name not found. Inherits from KeyError for backward compatibility."""
    pass


class InvalidOperatorError(QueryError, ValueError):
    """Raised when unsupported operator is used."""
    pass


class InvalidValueError(QueryError, ValueError):
    """Raised when TagConfidence value is invalid."""
    pass


class MatrixSizeError(ValidationError):
    """Raised when matrix dimensions exceed safe limits."""
    pass


class DataIntegrityError(SparseTagError):
    """Raised when data validation fails."""
    pass
