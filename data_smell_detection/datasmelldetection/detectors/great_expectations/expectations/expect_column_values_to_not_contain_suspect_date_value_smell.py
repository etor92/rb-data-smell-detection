from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.execution_engine import PandasExecutionEngine
from great_expectations.expectations.expectation import ColumnMapExpectation
from great_expectations.expectations.metrics import ColumnMapMetricProvider, column_condition_partial
from great_expectations.profile.base import ProfilerDataType

from datasmelldetection.core.datasmells import DataSmellType
from datasmelldetection.detectors.great_expectations.datasmell import DataSmell, DataSmellMetadata


class ColumnValuesDontContainSuspectDateValueSmell(ColumnMapMetricProvider):
    condition_metric_name = "column_values.custom.not_contains_suspect_date_value_smell"
    condition_value_keys = ("past_threshold_date", "future_threshold_date")

    @classmethod
    def _contains_suspect_date(cls, element: str) -> bool:
        """
        Check if a date value is suspect by being before the past threshold date (1950-01-01) 
        or after the future threshold date (tomorrow).

        Args:
            element (str): The date string to check.

        Returns:
            bool: True if the date is suspect, False otherwise.
        """
        past_threshold_date = datetime.strptime("1950-01-01", "%Y-%m-%d")
        future_threshold_date = datetime.now() + timedelta(days=1)
        try:
            date_value = datetime.strptime(element, "%Y-%m-%d")
            return date_value < past_threshold_date or date_value > future_threshold_date
        except ValueError:
            # If the date is not in the expected format, consider it suspect
            #print("ERROR: in suspect date value. not expected format.")
            return False

    @column_condition_partial(engine=PandasExecutionEngine)
    def _pandas(cls, column, _metrics, **kwargs):
        """
        Apply the suspect date check to each element in the column.

        Args:
            column (pandas.Series): The column to check.

        Returns:
            pandas.Series: Boolean series where True indicates the value is not suspect.
        """
        def not_contains_suspect_date(element: str) -> bool:
            return not cls._contains_suspect_date(element)
        return column.map(not_contains_suspect_date)


class ExpectColumnValuesToNotContainSuspectDateValueSmell(ColumnMapExpectation, DataSmell):
    """
    Expectation to detect the presence of suspect date values.

    This expectation checks if date values in a column are before a given past threshold date
    or after a given future threshold date, marking them as suspect.

    Keyword Args:
        mostly: See the documentation regarding the `mostly` concept in Great Expectations.
    """

    data_smell_metadata = DataSmellMetadata(
        data_smell_type=DataSmellType.SUSPECT_DATE_VALUE_SMELL,
        profiler_data_types={ProfilerDataType.STRING}
    )

    # Examples for tests
    examples = [
        {
            "data": {
                "valid_dates": ["2023-06-01", "2024-01-01", "2024-12-31"],
                "suspect_dates_past": ["1949-12-31", "1800-01-01", "1920-05-15"],
                "suspect_dates_future": ["2099-01-01", "3000-12-31", "2500-07-20"],
                "invalid_dates": ["2023-13-01", "2024-01-32", "2024-12-31 00:00:00"],
                "mixed_valid_suspect": ["2023-06-01", "1949-12-31", "2099-01-01"],
                "empty_strings": ["", "", ""],
                "non_date_values": ["hello", "world", "test"],
            },
            "tests": [
                {
                    "title": "test_valid_dates",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "valid_dates"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_suspect_dates_past",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "suspect_dates_past"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["1949-12-31", "1800-01-01", "1920-05-15"],
                    },
                },
                {
                    "title": "test_suspect_dates_future",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "suspect_dates_future"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["2099-01-01", "3000-12-31", "2500-07-20"],
                    },
                },
                {
                    "title": "test_invalid_dates",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "invalid_dates"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_mixed_valid_suspect",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "mixed_valid_suspect"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["1949-12-31", "2099-01-01"],
                    },
                },
                {
                    "title": "test_empty_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "empty_strings"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_non_date_values",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "non_date_values"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
            ],
        }
    ]

    # Metadata for display in the public gallery
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

    map_metric = "column_values.custom.not_contains_suspect_date_value_smell"

    success_keys = ("mostly")

    default_kwarg_values: Dict[str, Any] = {
        "mostly": 0.1
    }


# Instantiate and register the expectation
expectation = ExpectColumnValuesToNotContainSuspectDateValueSmell()
expectation.register_data_smell()
del expectation
