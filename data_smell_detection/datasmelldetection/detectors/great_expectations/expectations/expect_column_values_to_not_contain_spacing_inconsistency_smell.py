from typing import List, Dict, Any, Optional

from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.execution_engine import PandasExecutionEngine
from great_expectations.expectations.expectation import ColumnMapExpectation
from great_expectations.expectations.metrics import (
    ColumnMapMetricProvider,
    column_condition_partial,
)
from great_expectations.profile.base import ProfilerDataType
import re

from datasmelldetection.core.datasmells import DataSmellType
from datasmelldetection.detectors.great_expectations.datasmell import (
    DataSmell,
    DataSmellMetadata
)


class ColumnValuesDontContainSpacingInconsistencySmell(ColumnMapMetricProvider):
    condition_metric_name = "column_values.custom.not_contains_spacing_inconsistency_smell"
    condition_value_keys = ()

    @classmethod
    def _contains_spacing_inconsistency_smell(cls, element: str) -> bool:
        """
        Check if a string contains spacing inconsistencies.

        Args:
            element (str): The string to check.

        Returns:
            bool: True if spacing inconsistencies are detected, False otherwise.
        """
        # Regex patterns for different types of spacing issues
        leading_spaces_pattern = re.compile(r'^\s+')
        multiple_spaces_pattern = re.compile(r'\s{2,}')
        trailing_spaces_pattern = re.compile(r'\s+$')

        # Check for spacing issues
        if (leading_spaces_pattern.search(element) or
                multiple_spaces_pattern.search(element) or
                trailing_spaces_pattern.search(element)):
            return True
        return False

    @column_condition_partial(engine=PandasExecutionEngine)
    def _pandas(cls, column, _metrics, **kwargs):
        """
        Apply the spacing inconsistency check to each element in the column.

        Args:
            column (pandas.Series): The column to check.

        Returns:
            pandas.Series: Boolean series where True indicates the value is not suspect.
        """
        def not_contains_spacing_inconsistency_smell(element: str) -> bool:
            return not cls._contains_spacing_inconsistency_smell(element)
        return column.map(not_contains_spacing_inconsistency_smell)


class ExpectColumnValuesToNotContainSpacingInconsistencySmell(ColumnMapExpectation, DataSmell):
    """
    Detect the presence of a Spacing Smell.

    The detection of a Spacing Smell is performed for string columns. Strings are analyzed
    to estimate whether a data smell is present based on the presence of multiple spaces at 
    the beginning, between words, or at the end of the string.

    Keyword Args:
        mostly:
            See the documentation regarding the `mostly` concept regarding
            expectations in Great Expectations.
    """

    data_smell_metadata = DataSmellMetadata(
        data_smell_type=DataSmellType.SPACING_INCONSISTENCY_SMELL,
        profiler_data_types={ProfilerDataType.STRING}
    )

    # NOTE: The examples are used to perform tests
    examples = [
        {
            "data": {
                "valid_strings": ["abc", "abc def", "abc def ghi", "abc def ghi jkl", ""],
                "invalid_strings": [" abc", "abc  def", "abc def ghi  ", " abc def", "abc def  ", "abc  def ghi"]
            },
            "tests": [
                {
                    "title": "test_valid_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "valid_strings"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_invalid_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "invalid_strings"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": [" abc", "abc  def", "abc def ghi  ", " abc def", "abc def  ", "abc  def ghi"],
                    },
                },
                {
                    "title": "test_mixed_spacing_issues",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "mixed_spacing_issues"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": [" abc", " abc def", "abc  def  ghi ", "abc def  "],
                    },
                },
                {
                    "title": "test_leading_spaces",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "leading_spaces"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": [" abc", "  abc", "   abc"],
                    },
                },
                {
                    "title": "test_trailing_spaces",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "trailing_spaces"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["abc ", "abc  ", "abc   "],
                    },
                },
                {
                    "title": "test_multiple_spaces_between_words",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "multiple_spaces_between_words"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["abc  def", "abc   def", "abc    def"],
                    },
                },
                {
                    "title": "test_combined_spacing_issues",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "combined_spacing_issues"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": [" abc def ", "  abc  def  ", " abc  def ghi  "],
                    },
                },
                {
                    "title": "test_no_spacing_issues",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "no_spacing_issues"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
            ],
        }
    ]

    # This dictionary contains metadata for display in the public gallery
    library_metadata = {
        "maturity": "experimental",
        "tags": [
            "experimental"
        ],
        "contributors": [
            "@mkerschbaumer",
        ],
        "package": "experimental_expectations",
    }

    map_metric = "column_values.custom.not_contains_spacing_inconsistency_smell"

    success_keys = ("mostly",)

    default_kwarg_values: Dict[str, Any] = {
        "mostly": 0.95
    }

    def validate_configuration(self, configuration: Optional[ExpectationConfiguration]):
        super().validate_configuration(configuration)
        assert configuration is not None


expectation = ExpectColumnValuesToNotContainSpacingInconsistencySmell()
expectation.register_data_smell()
del expectation
