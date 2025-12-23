"""SparseTagging - High-performance sparse array library for tag confidence data."""

from .basetag import BaseTag, TagConfidence, QueryResult
from .exceptions import (
    BaseTagError,
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
    'BaseTag',
    'TagConfidence',
    'QueryResult',
    'BaseTagError',
    'ValidationError',
    'QueryError',
    'InvalidQueryStructureError',
    'InvalidColumnError',
    'InvalidOperatorError',
    'InvalidValueError',
    'MatrixSizeError',
    'DataIntegrityError',
]
