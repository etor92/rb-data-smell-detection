import json
from typing import Optional

from datasmelldetection.core import DataSmellType
from datasmelldetection.detectors.great_expectations.datasmell import DataSmell, DataSmellMetadata

from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.expectations.expectation import ColumnMapExpectation
from great_expectations.profile.base import ProfilerDataType


class ExpectColumnValuesToNotContainDummyValueSmell(ColumnMapExpectation, DataSmell):
    """
    Detect if a column contains dummy values.

    The presence of a dummy value smell is checked by using regex
    matching. Currently no parameters are defined.

    Keyword Args:
        mostly:
            See the documentation regarding the `mostly` concept regarding
            expectations in Great Expectations.
    """

    data_smell_metadata = DataSmellMetadata(
        data_smell_type=DataSmellType.DUMMY_VALUE_SMELL,
        profiler_data_types={ProfilerDataType.STRING, ProfilerDataType.INT, ProfilerDataType.FLOAT, ProfilerDataType.NUMERIC}
    )

    # NOTE: The examples are used to perform tests
    examples = [
        {
            "data": {
                "valid_values": ["apple", "banana", "cherry", "42", "3.14"],
                "dummy_values_string": ["UNK", "N/A", "UNKNOWN", "apple", "banana"],
                "dummy_values_numeric": ["0", "1", "999", "9999", "8888"],
                "mixed_values": ["0", "apple", "999", "banana", "3.14"],
                "empty_strings": ["", "", ""],
                "invalid_values": ["dummy", "NAN", "null", "none"],
            },
            "tests": [
                {
                    "title": "test_valid_values",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "valid_values"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_dummy_values_string",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "dummy_values_string"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["UNK", "N/A"],
                    },
                },
                {
                    "title": "test_dummy_values_numeric",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "dummy_values_numeric"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["0", "1", "999", "9999", "8888"],
                    },
                },
                {
                    "title": "test_mixed_values",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "mixed_values"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["0", "999"],
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
                    "title": "test_invalid_values",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "invalid_values"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
            ],
        }
    ]

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

    map_metric = "column_values.not_match_regex"
    success_keys = (
        "mostly",
        "regex"
    )

    default_kwarg_values = {
        "catch_exceptions": True,
        "regex": r'^(0|1|999|9999|8888|UNK|N/A)$',
        "mostly": 0.1
    }

    def validate_configuration(self, configuration: Optional[ExpectationConfiguration]):
        super().validate_configuration(configuration)
        assert configuration is not None
        assert "regex" not in configuration.kwargs, "regex cannot be altered"


expectation = ExpectColumnValuesToNotContainDummyValueSmell()
expectation.register_data_smell()
del expectation
