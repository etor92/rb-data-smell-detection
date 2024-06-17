import json
from typing import Optional

from datasmelldetection.core import DataSmellType
from datasmelldetection.detectors.great_expectations.datasmell import DataSmell, DataSmellMetadata

from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.expectations.expectation import ColumnMapExpectation
from great_expectations.profile.base import ProfilerDataType


class ExpectColumnValuesToNotContainTimeAsStringSmell(ColumnMapExpectation, DataSmell):
    """
    Detect if a time value is stored as a string.

    The presence of a time as string smell is checked by using regex
    matching. This includes time formats "HH:MM" and "HH:MM:SS".

    Keyword Args:
        mostly:
            See the documentation regarding the `mostly` concept regarding
            expectations in Great Expectations.
    """

    data_smell_metadata = DataSmellMetadata(
        data_smell_type=DataSmellType.TIME_AS_STRING_SMELL,
        profiler_data_types={ProfilerDataType.STRING}
    )

    # NOTE: The examples are used to perform tests
    examples = [
        {
            "data": {
                "valid_time_strings": ["23:59", "12:34:56", "00:00", "01:23:45"],
                "invalid_strings": ["25:00", "12:60:00", "random text", "24:00:00", "abcd", "12345"],
                "mixed_strings": ["23:59", "12:34:56", "random text", "01:23:45"],
                "no_time_strings": ["abcd", "efgh", "ijkl"],
                "empty_strings": ["", "", ""],
                "whitespace_strings": ["    ", "   ", " "],
                "times_with_text": ["time: 23:59", "12:34:56 and text", "text 01:23:45"],
                "long_strings": ["This is a long string with no time", "Another long string without any time"],
                "times_in_different_formats": ["23:59", "12:34:56"],
                "strings_with_special_characters": ["!@# $%^ &*()", ")(*&^%$#@!", "!@#$%^&*()"],
                "alphanumeric_mixed": ["abc123", "123abc", "a1b2c3", "1a2b3c"],
                "edge_case_times": ["00:00", "23:59", "00:00:00", "23:59:59"],
                "multiple_times_in_one_string": ["23:59 and 01:23:45", "12:34:56 23:59"],
                "times_with_different_separators": ["23:59", "12:34:56"],
                "non_time_numeric_strings": ["123456", "654321", "789012", "345678"],
                "non_time_alpha_strings": ["alpha", "beta", "gamma", "delta"],
            },
            "tests": [
                {
                    "title": "test_valid_time_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "valid_time_strings"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["23:59", "12:34:56", "00:00", "01:23:45"],
                    },
                },
                {
                    "title": "test_invalid_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "invalid_strings"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_mixed_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "mixed_strings"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["23:59", "12:34:56"],
                    },
                },
                {
                    "title": "test_no_time_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "no_time_strings"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
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
                    "title": "test_whitespace_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "whitespace_strings"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_times_with_text",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "times_with_text"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["time: 23:59", "12:34:56 and text", "text 01:23:45"],
                    },
                },
                {
                    "title": "test_long_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "long_strings"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_times_in_different_formats",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "times_in_different_formats"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["23:59", "12:34:56"],
                    },
                },
                {
                    "title": "test_strings_with_special_characters",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "strings_with_special_characters"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_alphanumeric_mixed",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "alphanumeric_mixed"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_edge_case_times",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "edge_case_times"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["00:00", "23:59", "00:00:00", "23:59:59"],
                    },
                },
                {
                    "title": "test_multiple_times_in_one_string",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "multiple_times_in_one_string"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["23:59 and 01:23:45", "12:34:56 23:59"],
                    },
                },
                {
                    "title": "test_times_with_different_separators",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "times_with_different_separators"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_non_time_numeric_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "non_time_numeric_strings"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_non_time_alpha_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "non_time_alpha_strings"},
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
        "regex": r'^(\d{2}:\d{2}:\d{2})$|^(\d{2}:\d{2})$',
        "mostly": 0.1
    }

    def validate_configuration(self, configuration: Optional[ExpectationConfiguration]):
        super().validate_configuration(configuration)
        assert configuration is not None
        assert "regex" not in configuration.kwargs, "regex cannot be altered"


expectation = ExpectColumnValuesToNotContainTimeAsStringSmell()
expectation.register_data_smell()
del expectation
