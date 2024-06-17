from typing import Optional, Dict, Any
import pandas as pd

from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.execution_engine import PandasExecutionEngine
from great_expectations.expectations.expectation import ColumnMapExpectation
from great_expectations.expectations.metrics import ColumnMapMetricProvider, column_condition_partial
from great_expectations.profile.base import ProfilerDataType

from datasmelldetection.core.datasmells import DataSmellType
from datasmelldetection.detectors.great_expectations.datasmell import DataSmell, DataSmellMetadata


class ColumnValuesDontContainPrecisionInconsistencies(ColumnMapMetricProvider):
    condition_metric_name = "column_values.custom.not_contains_precision_inconsistencies"
    condition_value_keys = ()

    @classmethod
    def _contains_precision_inconsistencies(cls, element: str) -> bool:
        """
        Check if a float value has a different number of decimal places compared to others.

        Args:
            element (str): The float string to check.

        Returns:
            bool: True if precision inconsistency is detected, False otherwise.
        """
        def count_decimal_places(value: float) -> int:
            if '.' in str(value):
                return len(str(value).split('.')[1])
            return 0
        
        # Extract the number of decimal places
        decimal_places = count_decimal_places(element)
        cls.decimal_places_set.add(decimal_places)
        
        # Check if there are multiple unique decimal places
        return len(cls.decimal_places_set) > 1

    @column_condition_partial(engine=PandasExecutionEngine)
    def _pandas(cls, column, _metrics, **kwargs):
        """
        Apply the precision inconsistency check to each element in the column.

        Args:
            column (pandas.Series): The column to check.

        Returns:
            pandas.Series: Boolean series where True indicates the value is not suspect.
        """
        cls.decimal_places_set = set()

        def not_contains_precision_inconsistencies(element: str) -> bool:
            return not cls._contains_precision_inconsistencies(element)
        return column.map(not_contains_precision_inconsistencies)


class ExpectColumnValuesToNotContainPrecisionInconsistencies(ColumnMapExpectation, DataSmell):
    """
    Detect the presence of precision inconsistencies in float values.

    This expectation checks if the number of decimal places varies significantly across the column.

    Keyword Args:
        mostly:
            See the documentation regarding the `mostly` concept in Great Expectations.
    """

    data_smell_metadata = DataSmellMetadata(
        data_smell_type=DataSmellType.PRECISION_INCONSISTENCY_SMELL,
        profiler_data_types={ProfilerDataType.FLOAT}
    )

    # Examples for tests
    examples = [
        {
            "data": {
                "consistent_precision": [1.234, 2.345, 3.456],
                "inconsistent_precision": [1.2, 2.345, 3.4567],
                "integers": [1, 2, 3],
                "mixed": [1, 2.345, 3.4567],
            },
            "tests": [
                {
                    "title": "test_consistent_precision",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "consistent_precision"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_inconsistent_precision",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "inconsistent_precision"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": [1.2, 2.345, 3.4567],
                    },
                },
                {
                    "title": "test_integers",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "integers"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_mixed",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "mixed"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": [1, 2.345, 3.4567],
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

    map_metric = "column_values.custom.not_contains_precision_inconsistencies"

    success_keys = ("mostly",)

    default_kwarg_values: Dict[str, Any] = {
        "mostly": 0.95
    }

    def validate_configuration(self, configuration: Optional[ExpectationConfiguration]):
        """
        Validate the configuration of the expectation.

        Args:
            configuration (Optional[ExpectationConfiguration]): Expectation configuration.

        Raises:
            AssertionError: If the configuration is invalid.
        """
        super().validate_configuration(configuration)
        assert configuration is not None, "Configuration must be provided"


# Instantiate and register the expectation
expectation = ExpectColumnValuesToNotContainPrecisionInconsistencies()
expectation.register_data_smell()
del expectation
