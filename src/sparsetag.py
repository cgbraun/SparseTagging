"""
Optimized SparseTag Implementation v2
======================================
This version works directly with sparse matrix internals for maximum performance.

Key optimizations:
1. Never convert sparse columns to dense
2. Only examine non-zero elements
3. Build results using row indices, not boolean masks
4. Use NumPy set operations (intersect1d, union, setdiff1d) instead of Python sets
5. Short-circuit empty results for efficiency

Performance improvements over v1:
- Single-column queries: 700-900x faster than original buggy implementation
- Multi-column queries: 5-10x faster than v1 (via NumPy operations)
"""

import enum
import logging
from functools import wraps
from typing import Any, Callable, Optional, Union

import numpy as np
from scipy import sparse

from .cache_manager import QueryCacheManager
from .exceptions import (
    InvalidColumnError,
    InvalidOperatorError,
    InvalidQueryStructureError,
    InvalidValueError,
    ValidationError,
)
from .sparse_protocol import CSCArrayProtocol, SparseInputProtocol

logger = logging.getLogger(__name__)

# Type alias for backward compatibility during sparse matrix → array migration
# Supports both deprecated sparse.spmatrix and current sparse.sparray formats
# Note: We use SparseInputProtocol for type hints to work around scipy's incomplete type stubs
SparseType = Union[sparse.spmatrix, sparse.sparray]


# ========================================================================
# Constants
# ========================================================================

# Integer type limits
MAX_INT8_VALUE = 127
MAX_INT16_VALUE = 32767
MAX_INT32_VALUE = 2147483647

# Matrix size thresholds for dtype optimization
INT8_THRESHOLD = 256  # Matrices with <256 rows can use int8 indices
INT16_THRESHOLD = 65536  # Matrices with <65,536 rows can use int16 indices

# Cache configuration defaults
DEFAULT_CACHE_MAX_ENTRIES = 256
DEFAULT_CACHE_MAX_MEMORY_MB = 10
DEFAULT_LARGE_RESULT_THRESHOLD_MB = 1.0
CACHE_OVERHEAD_BYTES = 200  # Estimated overhead per cached QueryResult

# Random generation limits
MAX_SAFE_NNZ = MAX_INT32_VALUE  # Maximum safe nnz value

# TagConfidence valid range
TAG_CONFIDENCE_MAX = 3
TAG_CONFIDENCE_MIN = 0


def invalidates_cache(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator that automatically invalidates cache when data is modified.

    Apply to any method that modifies self._data_internal or self._column_names.
    The decorated method can return self for method chaining.

    Example:
        @invalidates_cache
        def set_column(self, name, values):
            # ... modify data ...
            return self
    """

    @wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        result = func(self, *args, **kwargs)
        self._invalidate_cache()
        logger.debug(f"{func.__name__} invalidated cache (version {self._data_version})")
        return result

    return wrapper


class TagConfidence(enum.IntEnum):
    """Enumerated confidence levels for tags."""

    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    @classmethod
    def get_valid_values(cls) -> set:
        """Return set of valid non-zero confidence values."""
        return {cls.LOW, cls.MEDIUM, cls.HIGH}


class QueryResult:
    """Result object from SparseTag query operations."""

    def __init__(self, indices: np.ndarray, parent: "SparseTag"):
        """
        Initialize QueryResult from row indices.

        Args:
            indices: Array of matching row indices
            parent: Parent SparseTag instance
        """
        self._indices = np.asarray(indices, dtype=np.int64)
        self._parent = parent
        self._mask_cache: Optional[CSCArrayProtocol] = None

    @property
    def mask(self) -> CSCArrayProtocol:
        """Get sparse boolean mask of matching rows."""
        if self._mask_cache is None:
            # Create sparse mask from indices
            n_rows = self._parent.shape[0]
            mask: np.ndarray = np.zeros(n_rows, dtype=bool)
            if len(self._indices) > 0:
                mask[self._indices] = True
            # Return as sparse column vector
            mask_csc: CSCArrayProtocol = sparse.csc_array(mask.reshape(-1, 1), dtype=bool)
            self._mask_cache = mask_csc
        return self._mask_cache

    @property
    def indices(self) -> np.ndarray:
        """Get array of row indices where match."""
        return self._indices

    @property
    def count(self) -> int:
        """Get count of matching rows."""
        return len(self._indices)

    def __len__(self) -> int:
        """Return count of matches."""
        return self.count

    def to_sparsetag(self) -> "SparseTag":
        """Create new SparseTag containing only matching rows."""
        if self.count == 0:
            logger.warning("Creating empty SparseTag from zero matches")
            return SparseTag.create_empty(0, self._parent.column_names)

        # Extract matching rows efficiently
        filtered_data = self._parent._data[self._indices, :]
        return SparseTag.from_sparse(filtered_data, self._parent.column_names)

    def __repr__(self) -> str:
        return f"QueryResult(matches={self.count})"


class SparseTag:
    """
    OPTIMIZED sparse matrix container for tag confidence data.

    This version works directly with sparse matrix internals for maximum speed.
    """

    @staticmethod
    def _ensure_csc_format(data: SparseInputProtocol) -> CSCArrayProtocol:
        """
        Ensure data is in CSC sparse array format.

        Accepts both sparse matrix (deprecated) and sparse array formats
        for backward compatibility, but always returns sparse array.

        Args:
            data: Sparse matrix or array

        Returns:
            CSC sparse array

        Raises:
            ValueError: If data is not sparse
        """
        if not sparse.issparse(data):
            raise ValidationError("Data must be a scipy sparse matrix or array")

        # Convert to CSC array if needed (handles both matrix and wrong format)
        if data.format != "csc" or isinstance(data, sparse.spmatrix):
            logger.debug(
                f"Converting sparse {type(data).__name__} (format={data.format}) to CSC array"
            )
            result: CSCArrayProtocol = sparse.csc_array(data)
            return result

        return data  # type: ignore[return-value]

    def __init__(
        self, data: SparseInputProtocol, column_names: list[str], *, enable_cache: bool = True
    ):
        """
        Initialize SparseTag with optional query caching.

        Args:
            data: Sparse matrix (will convert to CSC if needed)
            column_names: List of column names
            enable_cache: Enable query result caching (default: True)

        Raises:
            ValueError: If data validation fails
        """
        # Validate and convert to CSC array format
        data = self._ensure_csc_format(data)

        if data.dtype != np.uint8:
            logger.debug(f"Converting data from {data.dtype} to uint8")
            data = data.astype(np.uint8)

        if len(column_names) != data.shape[1]:
            raise ValidationError(
                f"Column count mismatch: {len(column_names)} names for {data.shape[1]} columns"
            )

        # Validate all values are 0-3
        if data.data.size > 0 and np.any(data.data > 3):
            raise ValidationError("All values must be 0-3 (TagConfidence range)")

        # Store data using internal variable (property provides access with auto-invalidation)
        self._data_internal = data
        self._column_names = list(column_names)
        self._column_index = {name: idx for idx, name in enumerate(column_names)}

        # Cache infrastructure - delegate to QueryCacheManager
        self._cache_manager: Optional[QueryCacheManager] = (
            QueryCacheManager() if enable_cache else None
        )
        self._data_version = 0  # Track modifications (increments on changes)

        logger.info(
            f"Created SparseTag: shape={data.shape}, "
            f"nnz={data.nnz}, sparsity={1 - data.nnz / (data.shape[0] * data.shape[1]):.2%}, "
            f"cache_enabled={enable_cache}"
        )

    @property
    def _data(self) -> CSCArrayProtocol:
        """Get sparse array data."""
        return self._data_internal

    @_data.setter
    def _data(self, new_data: SparseInputProtocol) -> None:
        """
        Set sparse array data.
        Automatically invalidates cache on direct assignment.

        Args:
            new_data: New sparse matrix or array (will convert to CSC array)

        Example:
            >>> bt = SparseTag.create_random(1000, ['Tag1'], 0.01)
            >>> bt._data = sparse.csc_array(...)  # Cache auto-cleared
        """
        # Validate and convert to CSC array
        new_data = self._ensure_csc_format(new_data)

        if new_data.dtype != np.uint8:
            logger.debug(f"Converting from {new_data.dtype} to uint8")
            new_data = new_data.astype(np.uint8)

        self._data_internal = new_data
        self._invalidate_cache()
        logger.info(f"Data directly assigned - cache invalidated (version {self._data_version})")

    @classmethod
    def from_sparse(
        cls, sparse_matrix: SparseInputProtocol, column_names: list[str], **kwargs: Any
    ) -> "SparseTag":
        """Create SparseTag from existing sparse matrix or array."""
        return cls(sparse_matrix, column_names, **kwargs)

    @classmethod
    def from_dense(
        cls,
        dense_array: np.ndarray,
        column_names: list[str],
        sparsity_threshold: float = 0.1,
        **kwargs: Any,
    ) -> "SparseTag":
        """Create SparseTag from dense numpy array."""
        if not isinstance(dense_array, np.ndarray):
            dense_array = np.array(dense_array)

        dense_array = dense_array.astype(np.uint8)

        total_elements = dense_array.size
        nonzero_elements = np.count_nonzero(dense_array)
        sparsity = 1 - (nonzero_elements / total_elements)

        if sparsity < sparsity_threshold:
            logger.warning(f"Low sparsity ({sparsity:.2%}). Sparse format may not be efficient.")

        sparse_matrix = sparse.csc_array(dense_array, dtype=np.uint8)
        return cls(sparse_matrix, column_names, **kwargs)

    @classmethod
    def create_empty(cls, n_rows: int, column_names: list[str], **kwargs: Any) -> "SparseTag":
        """Create empty SparseTag with all zeros."""
        n_cols = len(column_names)
        sparse_matrix = sparse.csc_array((n_rows, n_cols), dtype=np.uint8)
        return cls(sparse_matrix, column_names, **kwargs)

    @classmethod
    def create_random(
        cls,
        n_rows: int,
        column_names: list[str],
        fill_percent: float = 0.1,
        seed: Optional[int] = None,
        enable_cache: bool = True,
    ) -> "SparseTag":
        """Create SparseTag with random test data."""
        if not 0 <= fill_percent <= 1:
            raise ValidationError("fill_percent must be between 0 and 1")

        n_cols = len(column_names)

        # Use local RNG instead of global state (thread-safe, no side effects)
        rng = np.random.default_rng(seed=seed)

        # Calculate nnz with overflow protection
        nnz_float = float(n_rows) * float(n_cols) * fill_percent
        nnz = int(nnz_float)

        # Validate against safe limits
        if nnz > MAX_SAFE_NNZ:
            raise ValidationError(
                f"Matrix too large: nnz={nnz:,} exceeds safe limit {MAX_SAFE_NNZ:,}. "
                f"Reduce size or fill_percent (rows={n_rows:,}, cols={n_cols}, fill={fill_percent:.2%})"
            )

        if nnz < 0:
            raise ValidationError(
                "Integer overflow detected in nnz calculation. Matrix dimensions too large."
            )

        if n_rows <= 0 or n_cols <= 0:
            raise ValidationError(
                f"Matrix dimensions must be positive: rows={n_rows}, cols={n_cols}"
            )

        if nnz == 0:
            logger.warning("Creating empty matrix: nnz=0")
            return cls.create_empty(n_rows, column_names, enable_cache=enable_cache)

        # Generate random data using local RNG
        rows = rng.integers(0, n_rows, size=nnz, dtype=np.int64)
        cols = rng.integers(0, n_cols, size=nnz, dtype=np.int64)
        values = rng.integers(1, 4, size=nnz, dtype=np.uint8)

        sparse_matrix = sparse.csc_array(
            (values, (rows, cols)), shape=(n_rows, n_cols), dtype=np.uint8
        )

        sparse_matrix.sum_duplicates()
        sparse_matrix.data = np.clip(sparse_matrix.data, 0, 3)

        logger.debug(f"Created random matrix: actual_nnz={sparse_matrix.nnz}")

        return cls(sparse_matrix, column_names, enable_cache=enable_cache)

    @property
    def shape(self) -> tuple[int, int]:
        """Get (n_rows, n_cols) shape."""
        return self._data.shape

    @property
    def column_names(self) -> list[str]:
        """Get list of column names."""
        return self._column_names.copy()

    @property
    def nnz(self) -> int:
        """Get number of non-zero elements."""
        return self._data.nnz

    @property
    def sparsity(self) -> float:
        """Get sparsity ratio (0-1, higher is more sparse)."""
        return 1 - (self.nnz / (self.shape[0] * self.shape[1]))

    def _get_column_index(self, column_name: str) -> int:
        """
        Get column index from name with validation.

        Args:
            column_name: Name of the column to look up

        Returns:
            Column index (0-based integer)

        Raises:
            InvalidColumnError: If column name is not found in the matrix

        Example:
            >>> bt = SparseTag.create_random(100, ['Tag1', 'Tag2'], 0.1)
            >>> bt._get_column_index('Tag1')
            0
            >>> bt._get_column_index('NonExistent')
            InvalidColumnError: Column 'NonExistent' not found
        """
        if column_name not in self._column_index:
            raise InvalidColumnError(
                f"Column '{column_name}' not found. Available: {', '.join(self._column_names)}"
            )
        return self._column_index[column_name]

    def _ensure_tag_confidence(self, value: Union[int, TagConfidence]) -> TagConfidence:
        """
        Type-safe conversion to TagConfidence with validation.

        Args:
            value: Integer (0-3) or TagConfidence enum value

        Returns:
            TagConfidence enum value

        Raises:
            ValueError: If value is not valid TagConfidence (must be 0-3)
        """
        if isinstance(value, TagConfidence):
            return value
        if isinstance(value, int) and 0 <= value <= 3:
            return TagConfidence(value)
        raise InvalidValueError(f"Invalid TagConfidence value: {value} (must be 0-3)")

    def get_value_counts(
        self, columns: Optional[Union[str, list[str]]] = None
    ) -> dict[str, dict[TagConfidence, int]]:
        """
        Get distribution of TagConfidence values per column.

        Counts the number of rows with each confidence level (NONE, LOW, MEDIUM, HIGH)
        for the specified columns. NONE values are implicit zeros in the sparse matrix.

        Args:
            columns: Column name(s) to analyze. If None, analyzes all columns.
                    Can be a single string or list of strings.

        Returns:
            Dictionary mapping column names to dictionaries of value counts.
            Inner dictionaries map TagConfidence values to integer counts.

        Example:
            >>> bt = SparseTag.create_random(100, ['Tag1', 'Tag2'], 0.1, seed=42)
            >>> counts = bt.get_value_counts('Tag1')
            >>> counts['Tag1'][TagConfidence.HIGH]
            3
            >>> counts['Tag1'][TagConfidence.NONE]  # Rows with no Tag1 value
            89

            >>> # Multiple columns
            >>> counts = bt.get_value_counts(['Tag1', 'Tag2'])
            >>> sum(counts['Tag1'].values())
            100
        """
        if columns is None:
            columns = self._column_names
        elif isinstance(columns, str):
            columns = [columns]

        results = {}

        for col_name in columns:
            col_idx = self._get_column_index(col_name)

            # Work with sparse column data directly
            col_start = self._data.indptr[col_idx]
            col_end = self._data.indptr[col_idx + 1]
            col_values = self._data.data[col_start:col_end]

            # Count non-zero values
            counts = {
                TagConfidence.HIGH: int(np.sum(col_values == TagConfidence.HIGH)),
                TagConfidence.MEDIUM: int(np.sum(col_values == TagConfidence.MEDIUM)),
                TagConfidence.LOW: int(np.sum(col_values == TagConfidence.LOW)),
                TagConfidence.NONE: int(self.shape[0] - len(col_values)),  # Implicit zeros
            }

            results[col_name] = counts

        return results

    def _transform_comparison(self, op: str, value: TagConfidence) -> set[int]:
        """
        Transform comparison operators to value sets for efficient IN-style queries.

        Converts comparison operators (==, !=, >, >=, <, <=) to sets of matching values.
        This optimization allows treating comparisons as IN operations on the sparse matrix.

        Args:
            op: Comparison operator string (==, !=, >, >=, <, <=)
            value: TagConfidence value to compare against (LOW, MEDIUM, or HIGH)

        Returns:
            Set of integer values (1-3) that satisfy the comparison

        Raises:
            InvalidValueError: If value is NONE/zero (would create dense matrix)
            InvalidOperatorError: If operator is unknown

        Example:
            >>> bt = SparseTag.create_random(100, ['Tag1'], 0.1)
            >>> bt._transform_comparison('>=', TagConfidence.MEDIUM)
            {2, 3}  # MEDIUM and HIGH
            >>> bt._transform_comparison('!=', TagConfidence.LOW)
            {2, 3}  # MEDIUM and HIGH (excludes LOW)
        """
        if value == TagConfidence.NONE:
            raise InvalidValueError(
                "Cannot compare to NONE/zero value. This would create dense matrix."
            )

        valid = {int(v) for v in TagConfidence.get_valid_values()}
        value_int = int(value)

        # Map operators to their filter functions
        operators = {
            "==": lambda v: {value_int},
            "!=": lambda v: valid - {value_int},
            ">": lambda v: {x for x in valid if x > value_int},
            ">=": lambda v: {x for x in valid if x >= value_int},
            "<": lambda v: {x for x in valid if x < value_int},
            "<=": lambda v: {x for x in valid if x <= value_int},
        }

        if op not in operators:
            raise InvalidOperatorError(f"Unknown operator: {op}")

        result = operators[op](value_int)

        if op == "!=":
            logger.debug(f"Transformed '!= {value.name}' to 'IN {result}'")

        return result

    def _evaluate_condition_optimized(self, condition: dict) -> np.ndarray:
        """
        OPTIMIZED: Evaluate condition and return row indices directly.

        Works with sparse matrix internals - only examines non-zero values.

        Args:
            condition: Dictionary with 'column', 'op', and 'value'/'values'

        Returns:
            Array of row indices that match the condition
        """
        col_name = condition["column"]
        col_idx = self._get_column_index(col_name)

        # Extract sparse column data using CSC internals
        col_start = self._data.indptr[col_idx]
        col_end = self._data.indptr[col_idx + 1]
        col_values = self._data.data[col_start:col_end]  # Only non-zero values!
        col_row_indices = self._data.indices[col_start:col_end]  # Their row positions

        op = condition.get("op", "==")

        if op == "IN":
            # Handle IN operator
            values = condition.get("values", [])
            if not values:
                raise InvalidQueryStructureError("IN operator requires 'values' list")

            # Check which non-zero values match
            value_ints = {int(v) for v in values}
            if TagConfidence.NONE in values:
                raise InvalidValueError("Cannot use NONE in IN operator")

            # Only check the non-zero values!
            matching_mask = np.isin(col_values, list(value_ints))
            matching_rows = col_row_indices[matching_mask]

        else:
            # Handle comparison operators
            value = condition.get("value")
            if value is None:
                raise InvalidQueryStructureError(f"Operator '{op}' requires 'value' field")

            # Type-safe conversion to TagConfidence
            value = self._ensure_tag_confidence(value)

            # Transform to value set
            value_set = self._transform_comparison(op, value)

            if not value_set:
                # Empty set - no matches
                logger.debug(f"Condition {col_name} {op} {value.name} yields empty set")
                matching_rows = np.array([], dtype=np.int64)
            else:
                # Check membership - only among non-zero values!
                matching_mask = np.isin(col_values, list(value_set))
                matching_rows = col_row_indices[matching_mask]

        return matching_rows

    def _get_rows_with_any_data(self) -> np.ndarray:
        """
        Get universe of rows containing ANY non-zero value.

        This is used for NOT operator semantics where we only consider rows that have
        at least one non-zero tag confidence value. Rows with all zeros (no tag data)
        are excluded from the NOT operation.

        Returns:
            Sorted array of row indices that have at least one non-zero value

        Example:
            Matrix with 5 rows:
            - Row 0: all zeros → excluded
            - Row 1: [LOW, NONE, NONE] → included
            - Row 2: all zeros → excluded
            - Row 3: [NONE, MEDIUM, NONE] → included
            - Row 4: all zeros → excluded
            Returns: [1, 3]
        """
        all_indices_list = []
        for col_idx in range(self.shape[1]):
            col_start = self._data.indptr[col_idx]
            col_end = self._data.indptr[col_idx + 1]
            if col_end > col_start:  # Column has data
                all_indices_list.append(self._data.indices[col_start:col_end])

        if all_indices_list:
            return np.unique(np.concatenate(all_indices_list))
        return np.array([], dtype=np.int64)

    def _apply_and_operator(self, row_arrays: list[np.ndarray]) -> np.ndarray:
        """
        Apply AND logic to multiple row arrays.

        Args:
            row_arrays: List of row index arrays from sub-conditions

        Returns:
            Array of row indices present in all input arrays
        """
        result = row_arrays[0]
        for arr in row_arrays[1:]:
            if len(result) == 0:
                break
            result = np.intersect1d(result, arr, assume_unique=True)
        return result

    def _apply_or_operator(self, row_arrays: list[np.ndarray]) -> np.ndarray:
        """
        Apply OR logic to multiple row arrays.

        Args:
            row_arrays: List of row index arrays from sub-conditions

        Returns:
            Array of row indices present in any input array
        """
        result = np.concatenate(row_arrays)
        return np.unique(result)

    def _apply_not_operator(self, row_arrays: list[np.ndarray]) -> np.ndarray:
        """
        Apply NOT logic to a single row array.

        Args:
            row_arrays: List with exactly one row index array

        Returns:
            Array of row indices in universe but not in input

        Raises:
            InvalidQueryStructureError: If row_arrays doesn't have exactly one element
        """
        if len(row_arrays) != 1:
            raise InvalidQueryStructureError("NOT operator requires exactly one condition")

        universe = self._get_rows_with_any_data()
        return np.setdiff1d(universe, row_arrays[0], assume_unique=True)

    def _evaluate_query_optimized(self, query: dict) -> np.ndarray:
        """
        OPTIMIZED v2: Recursively evaluate query using NumPy operations.

        Uses NumPy set operations instead of Python sets for 5-10x speedup.

        Returns:
            Array of row indices that match the query
        """
        if "operator" not in query:
            return self._evaluate_condition_optimized(query)

        operator = query["operator"].upper()
        conditions = query.get("conditions", [])

        if not conditions:
            raise InvalidQueryStructureError(f"{operator} operator requires 'conditions' list")

        row_arrays = [self._evaluate_query_optimized(cond) for cond in conditions]

        operator_handlers = {
            "AND": self._apply_and_operator,
            "OR": self._apply_or_operator,
            "NOT": self._apply_not_operator,
        }

        if operator not in operator_handlers:
            raise InvalidOperatorError(f"Unknown operator: {operator}")

        return operator_handlers[operator](row_arrays)

    def query(self, query_dict: dict, *, use_cache: bool = True) -> QueryResult:
        """
        Execute query and return results.

        OPTIMIZED: Works directly with sparse matrix internals.
        CACHED: Results are cached for repeated queries (v2.1).

        Args:
            query_dict: Query specification dictionary
            use_cache: Whether to use/populate cache (default: True)

        Returns:
            QueryResult with matching rows

        Raises:
            ValueError: If query structure is invalid

        Example:
            >>> bt = SparseTag.create_random(1000, ['Tag1'], 0.01)
            >>> # First call - cache miss (~0.4ms)
            >>> result1 = bt.query({'column': 'Tag1', 'op': '==', 'value': HIGH})
            >>> # Second call - cache hit (~0.01ms, 40x faster!)
            >>> result2 = bt.query({'column': 'Tag1', 'op': '==', 'value': HIGH})
            >>> # Disable cache for specific query
            >>> result3 = bt.query({'column': 'Tag1', 'op': '>', 'value': LOW}, use_cache=False)

        Note:
            Cache is automatically invalidated when data is modified.
            Cache overhead is <5% even for uncached queries.
        """
        logger.debug(f"Executing query: {query_dict}")

        if not isinstance(query_dict, dict):
            raise InvalidQueryStructureError("Query must be a dictionary")

        # Check if caching is enabled
        if not use_cache or not self._cache_manager:
            # Execute without cache
            matching_indices = self._evaluate_query_optimized(query_dict)
            return QueryResult(matching_indices, self)

        # Try to get from cache
        cached_result = self._cache_manager.get(query_dict)
        if cached_result is not None:
            return cached_result

        # Cache miss - execute query
        matching_indices = self._evaluate_query_optimized(query_dict)
        result = QueryResult(matching_indices, self)

        # Store in cache
        self._cache_manager.put(query_dict, result)

        return result

    # ========================================================================
    # Cache Management Methods
    # ========================================================================

    def _invalidate_cache(self) -> None:
        """
        Clear query cache when data is modified.

        Called automatically by:
        - Property setter (_data.setter)
        - @invalidates_cache decorator on mutating methods

        Note:
            This method is safe to call even if cache is disabled.
        """
        if self._cache_manager:
            self._cache_manager.clear()
        self._data_version += 1
        logger.debug(f"Cache invalidated (version → {self._data_version})")

    def clear_cache(self) -> None:
        """
        Manually clear query cache.

        Useful for:
        - Memory management
        - Testing
        - When you know queries won't repeat

        Example:
            >>> bt = SparseTag.create_random(1000, ['Tag1'], 0.01)
            >>> result = bt.query({'column': 'Tag1', 'op': '==', 'value': HIGH})
            >>> bt.clear_cache()
            >>> stats = bt.cache_stats()
            >>> stats['size_entries']
            0
        """
        if self._cache_manager:
            self._cache_manager.clear()

    def cache_stats(self) -> dict[str, Union[int, float, bool]]:
        """
        Get cache performance statistics.

        Returns:
            Dictionary with cache metrics:
            - hits: Number of cache hits
            - misses: Number of cache misses
            - hit_rate: Ratio of hits to total queries (0-1)
            - size_entries: Number of cached queries
            - size_bytes: Approximate memory usage (bytes)
            - size_mb: Memory usage in megabytes
            - data_version: Current data version (increments on modifications)
            - enabled: Whether caching is enabled

        Example:
            >>> bt = SparseTag.create_random(1000, ['Tag1'], 0.01)
            >>> for _ in range(10):
            ...     bt.query({'column': 'Tag1', 'op': '==', 'value': HIGH})
            >>> stats = bt.cache_stats()
            >>> stats['hits']
            9
            >>> stats['hit_rate']
            0.9
            >>> stats['size_mb']
            0.002
        """
        if self._cache_manager:
            stats = self._cache_manager.stats()
            stats["data_version"] = self._data_version
            stats["enabled"] = True
            return stats
        return {
            "hits": 0,
            "misses": 0,
            "hit_rate": 0.0,
            "size_entries": 0,
            "size_bytes": 0,
            "size_mb": 0.0,
            "data_version": self._data_version,
            "enabled": False,
        }

    def filter(self, query_dict: dict) -> "SparseTag":
        """Filter SparseTag and return new SparseTag with matching rows."""
        result = self.query(query_dict)
        return result.to_sparsetag()

    def to_dense(self) -> np.ndarray:
        """Convert to dense numpy array. WARNING: Memory intensive!"""
        logger.warning("Converting sparse matrix to dense - memory intensive!")
        return self._data.toarray()

    def memory_usage(self) -> dict[str, int]:
        """
        Calculate memory usage in bytes.

        Returns:
            Dict with breakdown: data, indices, indptr, column_names, total

        Note:
            Indices typically use int32 (4 bytes) per element, which is 4x larger
            than uint8 data. For matrices <65K rows, indices can be optimized to
            int16 (2 bytes) using optimize_indices_dtype() to save 50% memory.
        """
        data_bytes = self._data.data.nbytes
        indices_bytes = self._data.indices.nbytes
        indptr_bytes = self._data.indptr.nbytes
        column_names_bytes = sum(len(s.encode()) for s in self._column_names)

        return {
            "data": data_bytes,
            "indices": indices_bytes,
            "indptr": indptr_bytes,
            "column_names": column_names_bytes,
            "total": data_bytes + indices_bytes + indptr_bytes + column_names_bytes,
        }

    def optimize_indices_dtype(self, inplace: bool = True) -> Optional["SparseTag"]:
        """
        Optimize indices dtype to reduce memory usage.

        CSC sparse matrices use int32 (4 bytes) for indices by default.
        For smaller matrices, we can use smaller dtypes:
        - int16 (2 bytes): matrices with <65,536 rows
        - int8 (1 byte): matrices with <256 rows

        This can reduce indices memory by 50-75%.

        Args:
            inplace: If True, modify in place. If False, return new SparseTag.

        Returns:
            None if inplace=True, new SparseTag if inplace=False

        Example:
            >>> bt = SparseTag.create_random(10000, ['Tag1'], 0.01)
            >>> mem_before = bt.memory_usage()
            >>> bt.optimize_indices_dtype()
            >>> mem_after = bt.memory_usage()
            >>> savings = (mem_before['indices'] - mem_after['indices']) / mem_before['indices']
            >>> print(f"Indices memory reduced by {savings:.1%}")
            Indices memory reduced by 50.0%
        """
        n_rows = self._data.shape[0]

        # Determine optimal dtype based on matrix dimensions
        if n_rows < INT8_THRESHOLD:
            target_dtype: Any = np.int8
            max_value = MAX_INT8_VALUE
        elif n_rows < INT16_THRESHOLD:
            target_dtype = np.int16
            max_value = MAX_INT16_VALUE
        else:
            # Already optimal (int32 needed)
            if inplace:
                return None
            return SparseTag(
                self._data.copy(), self._column_names, enable_cache=self._cache_manager is not None
            )

        # CRITICAL: Validate actual index values fit in target dtype
        # This prevents data corruption when sparse data is concentrated in high row indices
        if len(self._data.indices) > 0:
            max_index: Any = np.max(self._data.indices)
            if max_index > max_value:
                logger.warning(
                    f"Cannot optimize to {target_dtype}: max index {max_index} exceeds {max_value}. "
                    f"Matrix has {n_rows} rows but data exists in row indices beyond {target_dtype} range."
                )
                if inplace:
                    return None
                return SparseTag(
                    self._data.copy(),
                    self._column_names,
                    enable_cache=self._cache_manager is not None,
                )

        # Validate indptr values (column pointers can also overflow)
        if len(self._data.indptr) > 0:
            max_indptr: Any = np.max(self._data.indptr)
            if max_indptr > max_value:
                logger.warning(
                    f"Cannot optimize to {target_dtype}: max indptr {max_indptr} exceeds {max_value}"
                )
                if inplace:
                    return None
                return SparseTag(
                    self._data.copy(),
                    self._column_names,
                    enable_cache=self._cache_manager is not None,
                )

        # Check if already optimal
        if self._data.indices.dtype == target_dtype:
            if inplace:
                return None
            return SparseTag(
                self._data.copy(), self._column_names, enable_cache=self._cache_manager is not None
            )

        # Safe to convert - all validation passed
        old_mem = self._data.indices.nbytes
        new_data = self._data.copy()
        new_data.indices = new_data.indices.astype(target_dtype)
        new_data.indptr = new_data.indptr.astype(target_dtype)
        new_mem = new_data.indices.nbytes
        savings = (old_mem - new_mem) / old_mem * 100

        logger.info(
            f"Optimized indices dtype: {self._data.indices.dtype} → {target_dtype}, "
            f"saved {savings:.1f}% indices memory"
        )

        if inplace:
            self._data = new_data
            return None
        return SparseTag(new_data, self._column_names, enable_cache=self._cache_manager is not None)

    def __repr__(self) -> str:
        return (
            f"SparseTag(shape={self.shape}, nnz={self.nnz}, "
            f"sparsity={self.sparsity:.2%}, columns={len(self._column_names)})"
        )
