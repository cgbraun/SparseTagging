"""Custom exceptions for BaseTag library."""


class BaseTagError(Exception):
    """Base exception for all BaseTag errors."""
    pass


class ValidationError(BaseTagError, ValueError):
    """Raised when input validation fails. Inherits from ValueError for backward compatibility."""
    pass


class QueryError(BaseTagError):
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


class DataIntegrityError(BaseTagError):
    """Raised when data validation fails."""
    pass
