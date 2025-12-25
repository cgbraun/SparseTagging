"""SparseTagging - High-performance sparse array library for tag confidence data."""

from .exceptions import (
    DataIntegrityError,
    InvalidColumnError,
    InvalidOperatorError,
    InvalidQueryStructureError,
    InvalidValueError,
    MatrixSizeError,
    QueryError,
    SparseTagError,
    ValidationError,
)
from .sparsetag import QueryResult, SparseTag, TagConfidence

__all__ = [
    "DataIntegrityError",
    "InvalidColumnError",
    "InvalidOperatorError",
    "InvalidQueryStructureError",
    "InvalidValueError",
    "MatrixSizeError",
    "QueryError",
    "QueryResult",
    "SparseTag",
    "SparseTagError",
    "TagConfidence",
    "ValidationError",
]
