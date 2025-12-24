"""SparseTagging - High-performance sparse array library for tag confidence data."""

from .sparsetag import SparseTag, TagConfidence, QueryResult
from .exceptions import (
    SparseTagError,
    ValidationError,
    QueryError,
    InvalidQueryStructureError,
    InvalidColumnError,
    InvalidOperatorError,
    InvalidValueError,
    MatrixSizeError,
    DataIntegrityError
)

__all__ = [
    'SparseTag',
    'TagConfidence',
    'QueryResult',
    'SparseTagError',
    'ValidationError',
    'QueryError',
    'InvalidQueryStructureError',
    'InvalidColumnError',
    'InvalidOperatorError',
    'InvalidValueError',
    'MatrixSizeError',
    'DataIntegrityError',
]
