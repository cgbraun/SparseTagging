"""Custom exceptions for SparseTag library."""


class SparseTagError(Exception):
    """Base exception for all SparseTag errors."""


class ValidationError(SparseTagError, ValueError):
    """Raised when input validation fails. Inherits from ValueError for backward compatibility."""


class QueryError(SparseTagError):
    """Raised when query execution fails."""


class InvalidQueryStructureError(QueryError, ValueError):
    """Raised when query dictionary structure is invalid."""


class InvalidColumnError(QueryError, KeyError):
    """Raised when column name not found. Inherits from KeyError for backward compatibility."""


class InvalidOperatorError(QueryError, ValueError):
    """Raised when unsupported operator is used."""


class InvalidValueError(QueryError, ValueError):
    """Raised when TagConfidence value is invalid."""


class MatrixSizeError(ValidationError):
    """Raised when matrix dimensions exceed safe limits."""


class DataIntegrityError(SparseTagError):
    """Raised when data validation fails."""
