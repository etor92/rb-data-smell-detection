from typing import Optional, Dict, Any
import re

from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.execution_engine import PandasExecutionEngine
from great_expectations.expectations.expectation import ColumnMapExpectation
from great_expectations.expectations.metrics import ColumnMapMetricProvider, column_condition_partial
from great_expectations.profile.base import ProfilerDataType
import pandas as pd

from datasmelldetection.core.datasmells import DataSmellType
from datasmelldetection.detectors.great_expectations.datasmell import DataSmell, DataSmellMetadata


unique_types = set()


class ColumnValuesDontContainIntermingledDataTypes(ColumnMapMetricProvider):
    condition_metric_name = "column_values.custom.not_contains_intermingled_data_types"
    condition_value_keys = ()

    @classmethod
    def _contains_intermingled_types(cls, element: str) -> bool:
        """
        Check if a column contains intermingled data types.

        Args:
            column (pandas.Series): The column to check.

        Returns:
            bool: True (needed for great_expectations) if intermingled data types are detected,
              False otherwise.
        """
        string_pattern = re.compile(r'^[a-zA-Z\s]+$')
        numeric_pattern = re.compile(r'^-?\d+(\.\d+)?$')
        date_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2})$|^(\d{2}/\d{2}/\d{4})$|^(\d{2}-\d{2}-\d{4})$|^(\d{4}/\d{2}/\d{2})$')
        datetime_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})|(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})|(\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2})|(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})')
        if (type(element) == int or type(element) == float):
            unique_types.add('numeric')
        elif bool(string_pattern.match(element)):
            unique_types.add("string")
        elif bool(numeric_pattern.match(element)):
            unique_types.add("numeric")
        elif bool(date_pattern.match(element)):
            unique_types.add('date')
        elif bool(datetime_pattern.match(element)):
            unique_types.add('datetime')

        if len(unique_types) > 1:
            return True  # True if more than one unique data type is found
        else:
            return False

    @column_condition_partial(engine=PandasExecutionEngine)
    def _pandas(cls, column, _metrics, **kwargs):
        """
        Apply the intermingled data types check to each element in the column.

        Args:
            column (pandas.Series): The column to check.

        Returns:
            pandas.Series: Boolean series where True indicates the value is not suspect.
        """
        # Negate the result of _contains_casing_smell since Great Expectations
        # assumes that False is returned if a value is faulty
        # (a data smell is present).
        unique_types.clear()
        def not_contains_intermingled_data_types(element: str) -> bool:
            return not cls._contains_intermingled_types(element)
        return column.map(not_contains_intermingled_data_types)


class ExpectColumnValuesToNotContainIntermingledDataTypes(ColumnMapExpectation, DataSmell):
    """
    Expect column values to not contain intermingled data types.

    This expectation checks if the column contains more than one unique data type.
    """

    data_smell_metadata = DataSmellMetadata(
        data_smell_type=DataSmellType.INTERMINGLED_DATA_TYPE_SMELL,
        profiler_data_types={ProfilerDataType.STRING, ProfilerDataType.INT, ProfilerDataType.FLOAT, ProfilerDataType.NUMERIC}
    )

    # Examples for tests
    examples = [
        {
            "data": {
                "all_strings": ["a", "b", "c"],
                "all_ints": [1, 2, 3],
                "mixed_types": ["a", 1, 3.5],
                "all_floats": [1.1, 2.2, 3.3],
                "all_dates": ["2023-01-01", "2023-02-01", "2023-03-01"],
                "all_datetimes": ["2023-01-01 10:00:00", "2023-02-01 12:00:00", "2023-03-01 14:00:00"],
                "mixed_with_date": ["a", "2023-01-01", 3.5],
                "mixed_with_datetime": ["a", "2023-01-01 10:00:00", 3.5],
                "mixed_with_int": ["a", 1, "2023-01-01"],
                "mixed_with_float": ["a", 1.1, "2023-01-01 10:00:00"],
                "all_empty_strings": ["", "", ""],
                "mixed_with_empty_strings": ["", 1, "2023-01-01"],
                "mixed_types2": [1, "b", "2023-01-01"],
                "all_booleans": [True, False, True],
            },
            "tests": [
                {
                    "title": "test_all_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "all_strings"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_all_ints",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "all_ints"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_mixed_types",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "mixed_types"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["a", 1, 3.5],
                    },
                },
                {
                    "title": "test_all_floats",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "all_floats"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_all_dates",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "all_dates"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_all_datetimes",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "all_datetimes"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_mixed_with_date",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "mixed_with_date"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["a", "2023-01-01", 3.5],
                    },
                },
                {
                    "title": "test_mixed_with_datetime",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "mixed_with_datetime"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["a", "2023-01-01 10:00:00", 3.5],
                    },
                },
                {
                    "title": "test_mixed_with_int",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "mixed_with_int"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["a", 1, "2023-01-01"],
                    },
                },
                {
                    "title": "test_mixed_with_float",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "mixed_with_float"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["a", 1.1, "2023-01-01 10:00:00"],
                    },
                },
                {
                    "title": "test_all_empty_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "all_empty_strings"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_mixed_with_empty_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "mixed_with_empty_strings"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["", 1, "2023-01-01"],
                    },
                },
                {
                    "title": "test_mixed_types2",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "mixed_types2"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": [1, "b", "2023-01-01"],
                    },
                },
                {
                    "title": "test_all_booleans",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "all_booleans"},
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

    map_metric = "column_values.custom.not_contains_intermingled_data_types"

    success_keys = ("mostly",)

    default_kwarg_values: Dict[str, Any] = {
        "mostly": 0.1
    }

    #def validate_configuration(self, configuration: Optional[ExpectationConfiguration]):
    #    """
    #    Validate the configuration of the expectation.

    #    Args:
    #        configuration (Optional[ExpectationConfiguration]): Expectation configuration.

     #   Raises:
     #       AssertionError: If the configuration is invalid.
     #   """
     #   super().validate_configuration(configuration)
     #   assert configuration is not None, "Configuration must be provided"


# Instantiate and register the expectation
expectation = ExpectColumnValuesToNotContainIntermingledDataTypes()
expectation.register_data_smell()
del expectation
