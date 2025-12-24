"""Tests for custom exception hierarchy."""
import pytest
from src.exceptions import (
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
from src.sparsetag import SparseTag, TagConfidence


class TestExceptionHierarchy:
    """Test exception inheritance and backward compatibility."""

    def test_sparse_tag_error_is_exception(self):
        """Ensure SparseTagError inherits from Exception."""
        assert issubclass(SparseTagError, Exception)

        try:
            raise SparseTagError("test")
        except Exception:
            pass  # Should catch as Exception

    def test_validation_error_is_value_error(self):
        """Ensure backward compatibility with ValueError."""
        assert issubclass(ValidationError, ValueError)
        assert issubclass(ValidationError, SparseTagError)

        try:
            raise ValidationError("test")
        except ValueError:
            pass  # Should catch as ValueError

    def test_invalid_column_error_is_key_error(self):
        """Ensure backward compatibility with KeyError."""
        assert issubclass(InvalidColumnError, KeyError)
        assert issubclass(InvalidColumnError, QueryError)

        try:
            raise InvalidColumnError("test")
        except KeyError:
            pass  # Should catch as KeyError

    def test_query_error_hierarchy(self):
        """Test QueryError subclass hierarchy."""
        assert issubclass(QueryError, SparseTagError)
        assert issubclass(InvalidQueryStructureError, QueryError)
        assert issubclass(InvalidColumnError, QueryError)
        assert issubclass(InvalidOperatorError, QueryError)
        assert issubclass(InvalidValueError, QueryError)

    def test_matrix_size_error_hierarchy(self):
        """Test MatrixSizeError is a ValidationError."""
        assert issubclass(MatrixSizeError, ValidationError)
        assert issubclass(MatrixSizeError, SparseTagError)


class TestExceptionUsage:
    """Test that exceptions are raised correctly in SparseTag."""

    def test_invalid_column_error_raised(self):
        """Test InvalidColumnError is raised for nonexistent columns."""
        bt = SparseTag.create_random(100, ['Tag1'], 0.1, seed=42)

        with pytest.raises(InvalidColumnError) as exc_info:
            bt.query({'column': 'NonExistent', 'op': '==', 'value': TagConfidence.HIGH})

        assert 'NonExistent' in str(exc_info.value)
        assert 'not found' in str(exc_info.value).lower()

    def test_invalid_operator_error_raised(self):
        """Test InvalidOperatorError is raised for invalid operators."""
        bt = SparseTag.create_random(100, ['Tag1'], 0.1, seed=42)

        with pytest.raises(InvalidOperatorError) as exc_info:
            bt.query({'column': 'Tag1', 'op': '===', 'value': TagConfidence.HIGH})

        assert '===' in str(exc_info.value)

    def test_invalid_value_error_for_none_comparison(self):
        """Test InvalidValueError is raised for NONE value queries."""
        bt = SparseTag.create_random(100, ['Tag1'], 0.1, seed=42)

        with pytest.raises(InvalidValueError) as exc_info:
            bt.query({'column': 'Tag1', 'op': '==', 'value': TagConfidence.NONE})

        assert 'NONE' in str(exc_info.value) or 'zero' in str(exc_info.value).lower()

    def test_invalid_value_error_for_none_in_operator(self):
        """Test InvalidValueError is raised for NONE in IN operator."""
        bt = SparseTag.create_random(100, ['Tag1'], 0.1, seed=42)

        with pytest.raises(InvalidValueError):
            bt.query({
                'column': 'Tag1',
                'op': 'IN',
                'values': [TagConfidence.NONE, TagConfidence.HIGH]
            })

    def test_invalid_query_structure_error_missing_field(self):
        """Test InvalidQueryStructureError for missing query fields."""
        bt = SparseTag.create_random(100, ['Tag1'], 0.1, seed=42)

        # Missing 'value' field
        with pytest.raises(InvalidQueryStructureError):
            bt.query({'column': 'Tag1', 'op': '=='})

    def test_invalid_query_structure_error_missing_conditions(self):
        """Test InvalidQueryStructureError for logical operator without conditions."""
        bt = SparseTag.create_random(100, ['Tag1'], 0.1, seed=42)

        with pytest.raises(InvalidQueryStructureError):
            bt.query({'operator': 'AND', 'conditions': []})

    def test_invalid_query_structure_error_not_operator(self):
        """Test InvalidQueryStructureError for NOT with multiple conditions."""
        bt = SparseTag.create_random(100, ['Tag1', 'Tag2'], 0.1, seed=42)

        with pytest.raises(InvalidQueryStructureError) as exc_info:
            bt.query({
                'operator': 'NOT',
                'conditions': [
                    {'column': 'Tag1', 'op': '==', 'value': TagConfidence.HIGH},
                    {'column': 'Tag2', 'op': '==', 'value': TagConfidence.LOW}
                ]
            })

        assert 'NOT' in str(exc_info.value)
        assert 'one condition' in str(exc_info.value).lower()

    def test_validation_error_for_invalid_input(self):
        """Test ValidationError is raised for invalid array inputs."""
        import numpy as np

        # Out of range values
        with pytest.raises(ValidationError):
            invalid_array = np.array([[0, 1, 2, 4]])  # 4 is out of range
            SparseTag.from_dense(invalid_array, ['Tag1'])

    def test_validation_error_for_column_mismatch(self):
        """Test ValidationError for column count mismatch."""
        import numpy as np

        with pytest.raises(ValidationError) as exc_info:
            array = np.array([[1, 2]])
            SparseTag.from_dense(array, ['Tag1', 'Tag2', 'Tag3'])  # 2 cols vs 3 names

        assert 'column' in str(exc_info.value).lower()


class TestBackwardCompatibility:
    """Test that custom exceptions maintain backward compatibility."""

    def test_catch_validation_error_as_value_error(self):
        """Test ValidationError can be caught as ValueError."""
        import numpy as np

        try:
            # Trigger ValidationError
            invalid_array = np.array([[0, 1, 2, 5]])  # 5 is out of range
            SparseTag.from_dense(invalid_array, ['Tag1'])
        except ValueError as e:
            # Should be catchable as ValueError
            assert isinstance(e, ValidationError)
            assert isinstance(e, ValueError)

    def test_catch_invalid_column_as_key_error(self):
        """Test InvalidColumnError can be caught as KeyError."""
        bt = SparseTag.create_random(100, ['Tag1'], 0.1, seed=42)

        try:
            bt.query({'column': 'NonExistent', 'op': '==', 'value': TagConfidence.HIGH})
        except KeyError as e:
            # Should be catchable as KeyError
            assert isinstance(e, InvalidColumnError)
            assert isinstance(e, KeyError)

    def test_catch_query_errors_as_value_error(self):
        """Test query-related errors can be caught as ValueError where appropriate."""
        bt = SparseTag.create_random(100, ['Tag1'], 0.1, seed=42)

        # InvalidOperatorError
        try:
            bt.query({'column': 'Tag1', 'op': 'INVALID', 'value': TagConfidence.HIGH})
        except ValueError as e:
            assert isinstance(e, InvalidOperatorError)
            assert isinstance(e, ValueError)

        # InvalidValueError
        try:
            bt.query({'column': 'Tag1', 'op': '==', 'value': TagConfidence.NONE})
        except ValueError as e:
            assert isinstance(e, InvalidValueError)
            assert isinstance(e, ValueError)


class TestExceptionMessages:
    """Test that exception messages are informative."""

    def test_invalid_column_message_shows_available(self):
        """Test InvalidColumnError shows available columns."""
        bt = SparseTag.create_random(100, ['Tag1', 'Tag2', 'Tag3'], 0.1, seed=42)

        with pytest.raises(InvalidColumnError) as exc_info:
            bt.query({'column': 'InvalidTag', 'op': '==', 'value': TagConfidence.HIGH})

        error_msg = str(exc_info.value)
        assert 'InvalidTag' in error_msg
        assert 'Tag1' in error_msg or 'Available' in error_msg

    def test_invalid_operator_message_shows_operator(self):
        """Test InvalidOperatorError shows the invalid operator."""
        bt = SparseTag.create_random(100, ['Tag1'], 0.1, seed=42)

        with pytest.raises(InvalidOperatorError) as exc_info:
            bt.query({'column': 'Tag1', 'op': 'BADOP', 'value': TagConfidence.HIGH})

        assert 'BADOP' in str(exc_info.value)

    def test_invalid_value_message_explains_issue(self):
        """Test InvalidValueError explains the issue clearly."""
        bt = SparseTag.create_random(100, ['Tag1'], 0.1, seed=42)

        with pytest.raises(InvalidValueError) as exc_info:
            bt.query({'column': 'Tag1', 'op': '==', 'value': TagConfidence.NONE})

        error_msg = str(exc_info.value).lower()
        # Should mention why NONE is invalid
        assert 'none' in error_msg or 'zero' in error_msg or 'dense' in error_msg

    def test_validation_error_message_specific(self):
        """Test ValidationError messages are specific to the issue."""
        import numpy as np

        # Out of range value
        with pytest.raises(ValidationError) as exc_info:
            invalid_array = np.array([[5]])  # 5 is out of range
            SparseTag.from_dense(invalid_array, ['Tag1'])

        error_msg = str(exc_info.value).lower()
        assert 'range' in error_msg or 'valid' in error_msg
