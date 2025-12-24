"""
Type protocols for scipy sparse arrays.

This module defines Protocol interfaces for scipy sparse arrays to work around
incomplete type stubs in scipy. These protocols explicitly declare the attributes
and methods we use, enabling full type safety without `type: ignore` comments.

Why this is needed:
- scipy's type stubs don't declare attributes like .data, .indices, .indptr
- Using Protocol is more type-safe than using Any or broad type ignores
- Explicitly documents the sparse array interface we depend on
"""

from typing import Protocol, Any, Tuple
import numpy as np
from numpy.typing import NDArray


class CSCArrayProtocol(Protocol):
    """
    Protocol defining the CSC sparse array interface used by SparseTag.

    This protocol captures the attributes and methods we actually use from
    scipy.sparse.csc_array, enabling proper type checking without relying
    on scipy's incomplete type stubs.

    CSC (Compressed Sparse Column) format stores:
    - data: Non-zero values
    - indices: Row indices of non-zero values
    - indptr: Column pointer array
    """

    # Array properties
    @property
    def shape(self) -> Tuple[int, int]:
        """Shape of the sparse array (rows, cols)."""
        ...

    @property
    def dtype(self) -> np.dtype[Any]:
        """Data type of stored values."""
        ...

    @property
    def nnz(self) -> int:
        """Number of non-zero elements."""
        ...

    @property
    def format(self) -> str:
        """Sparse format string (e.g., 'csc', 'csr')."""
        ...

    # CSC format internals (these are read-write, not read-only properties)
    data: NDArray[Any]
    """Array of non-zero values."""

    indices: NDArray[np.int32]
    """Array of row indices for non-zero values."""

    indptr: NDArray[np.int32]
    """Column pointer array (length = ncols + 1)."""

    # Methods
    def astype(self, dtype: Any) -> 'CSCArrayProtocol':
        """Convert to different dtype."""
        ...

    def copy(self) -> 'CSCArrayProtocol':
        """Create a deep copy."""
        ...

    def toarray(self) -> NDArray[Any]:
        """Convert to dense numpy array."""
        ...

    def __getitem__(self, key: Any) -> Any:
        """Support indexing."""
        ...


class SparseInputProtocol(Protocol):
    """
    Protocol for sparse matrix/array inputs (broader than CSCArrayProtocol).

    This protocol accepts any scipy sparse format for input validation and
    conversion. Protocol for sparse arrays used in SparseTag factory methods and validation functions.
    """

    @property
    def format(self) -> str:
        """Sparse format string."""
        ...

    @property
    def shape(self) -> Tuple[int, int]:
        """Shape of the sparse array."""
        ...

    @property
    def dtype(self) -> np.dtype[Any]:
        """Data type of stored values."""
        ...

    @property
    def nnz(self) -> int:
        """Number of non-zero elements."""
        ...

    @property
    def data(self) -> NDArray[Any]:
        """Array of non-zero values."""
        ...
