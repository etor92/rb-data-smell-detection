import json
from typing import Optional

from datasmelldetection.core import DataSmellType
from datasmelldetection.detectors.great_expectations.datasmell import DataSmell, DataSmellMetadata

from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.expectations.expectation import ColumnMapExpectation
from great_expectations.profile.base import ProfilerDataType


class ExpectColumnValuesToNotContainDateAsStringSmell(ColumnMapExpectation, DataSmell):
    """
    Detect if a date is stored as a string.

    The presence of a date as string smell is checked by using regex
    matching. Currently no parameters are defined.

    Keyword Args:
        mostly:
            See the documentation regarding the `mostly` concept regarding
            expectations in Great Expectations.
    """

    data_smell_metadata = DataSmellMetadata(
        data_smell_type=DataSmellType.DATE_AS_STRING_SMELL,
        profiler_data_types={ProfilerDataType.STRING}
    )

    # NOTE: The examples are used to perform tests
    examples = [
        {
            "data": {
                "valid_strings": ["2023-01-01", "01/01/2023", "01-01-2023", "2023/01/01"],
                "invalid_strings": ["January 1, 2023", "2023.01.01", "01-2023", "1/1/23", "abcd", "12345"],
                "mixed_strings": ["2023-01-01", "01/01/2023", "random text", "2023-01-01 10:00:00"],
                "no_dates": ["abcd", "efgh", "ijkl"],
                "empty_strings": ["", "", ""],
                "whitespace_strings": ["    ", "   ", " "],
                "dates_with_text": ["date: 2023-01-01", "01/01/2023 and text", "text 01-01-2023", "date: 2023/01/01"],
                "long_strings": ["This is a long string with no date", "Another long string without any date"],
                "dates_in_different_formats": ["01/01/2023", "2023-01-01", "01-01-2023", "2023/01/01"],
                "strings_with_special_characters": ["!@# $%^ &*()", ")(*&^%$#@!", "!@#$%^&*()", "(1234-56-78)", "(12/34/5678)"],
                "alphanumeric_mixed": ["abc123", "123abc", "a1b2c3", "1a2b3c"],
                "edge_case_dates": ["9999-12-31", "0001-01-01", "31/12/9999", "01/01/0001"],
                "multiple_dates_in_one_string": ["2023-01-01 and 2024-01-01", "01/01/2023 01-01-2024", "2023/01/01 and 2024/01/01"],
                "dates_with_different_separators": ["2023.01.01", "01.01.2023", "01-01.2023", "2023/01.01"],
                "non_date_numeric_strings": ["123456", "654321", "789012", "345678"],
                "non_date_alpha_strings": ["alpha", "beta", "gamma", "delta"],
            },
            "tests": [
                {
                    "title": "test_valid_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "valid_strings"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["2023-01-01", "01/01/2023", "01-01-2023", "2023/01/01"],
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
                        "partial_unexpected_list": ["2023-01-01", "01/01/2023"],
                    },
                },
                {
                    "title": "test_no_dates",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "no_dates"},
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
                    "title": "test_dates_with_text",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "dates_with_text"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["date: 2023-01-01", "01/01/2023 and text", "text 01-01-2023", "date: 2023/01/01"],
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
                    "title": "test_dates_in_different_formats",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "dates_in_different_formats"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["01/01/2023", "2023-01-01", "01-01-2023", "2023/01/01"],
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
                    "title": "test_edge_case_dates",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "edge_case_dates"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["9999-12-31", "0001-01-01", "31/12/9999", "01/01/0001"],
                    },
                },
                {
                    "title": "test_multiple_dates_in_one_string",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "multiple_dates_in_one_string"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["2023-01-01 and 2024-01-01", "01/01/2023 01-01-2024", "2023/01/01 and 2024/01/01"],
                    },
                },
                {
                    "title": "test_dates_with_different_separators",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "dates_with_different_separators"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_non_date_numeric_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "non_date_numeric_strings"},
                    "out": {
                        "success": True,
                        "partial_unexpected_list": [],
                    },
                },
                {
                    "title": "test_non_date_alpha_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "non_date_alpha_strings"},
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
        "regex": r'^(\d{4}-\d{2}-\d{2})$|^(\d{2}/\d{2}/\d{4})$|^(\d{2}-\d{2}-\d{4})$|^(\d{4}/\d{2}/\d{2})$',
        "mostly": 0.1
    }

    def validate_configuration(self, configuration: Optional[ExpectationConfiguration]):
        super().validate_configuration(configuration)
        assert configuration is not None
        assert "regex" not in configuration.kwargs, "regex cannot be altered"


expectation = ExpectColumnValuesToNotContainDateAsStringSmell()
expectation.register_data_smell()
del expectation
