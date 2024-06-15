import json
from typing import Optional

from datasmelldetection.core import DataSmellType
from datasmelldetection.detectors.great_expectations.datasmell import DataSmell, DataSmellMetadata

from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.expectations.expectation import ColumnMapExpectation
from great_expectations.profile.base import ProfilerDataType


class ExpectColumnValuesToNotContainSpacingSmell(ColumnMapExpectation, DataSmell):
    """
    Detect if a string contains spacing smells (multiple occurrences of whitespaces).

    The presence of a spacing smell is checked by using regex matching. This includes:
    - Multiple spaces at the beginning
    - Multiple spaces between words
    - Multiple spaces at the end

    Keyword Args:
        mostly:
            See the documentation regarding the `mostly` concept regarding
            expectations in Great Expectations.
    """

    data_smell_metadata = DataSmellMetadata(
        data_smell_type=DataSmellType.SPACING_SMELL,
        profiler_data_types={ProfilerDataType.STRING}
    )

    # NOTE: The examples are used to perform tests
    examples = [
        {
            "data": {
                "valid_strings": ["abc", "abc def", "abc def ghi", "abc def ghi jkl", ""],
                "invalid_strings": [" abc", "abc  def", "abc def ghi  ", " abc def", "abc def  ", "abc  def ghi"],
                "leading_spaces": [" abc", "  abc", "   abc"],
                "trailing_spaces": ["abc ", "abc  ", "abc   "],
                "multiple_spaces_between_words": ["abc  def", "abc   def", "abc    def"],
                "combined_spacing_issues": [" abc def ", "  abc  def  ", " abc  def ghi  "],
                "no_spacing_issues": ["abcdef", "abcd efgh", "abcdefgh", "abcdef ghi", "abcdefghij"],
                "mix_valid_and_invalid": ["abc def", " abc", "abc  def", "abc def ", "def ghi"],
                "mixed_case_spaces": ["Abc  Def", "aBC   dEF", "Ab C  Def"],
                "text_with_numbers": ["123 abc", "abc 123", "abc  123", " 123 abc "],
                "special_characters": ["abc!@#", "abc  !@#", "abc!  @#", "abc !@#  "],
                "long_strings": ["This is a very long string without any spacing issues at all.", 
                                 "This is a  very long string with multiple spaces in between words.",
                                 "Another long string    with multiple issues    in between."],
                "multiple_sentences": ["This is a sentence.  This is another sentence.", 
                                       "Sentence one.   Sentence two.", 
                                       "   Leading space. Trailing space.   "],
                "new_lines_and_tabs": ["abc\ndef", "abc\tdef", "abc  \ndef", "\tabc def", "abc def\t"],
                "all_spaces": ["     ", "  ", " "],
                "mix_spaces_and_valid": ["    ", "abc", " abc ", "def", "  ghi  "],
                "edge_case_spaces": [" ", "abc def ", " abc def"],
                "non_ascii_characters": ["abc äöü", "abc  äöü", " äöü", "äöü  ", "äö ü"],
                "punctuation_with_spaces": ["abc, def", "abc , def", "abc ,def", "abc,def  "],
                "quotes_with_spaces": ['"abc"', ' "abc"', '"abc" ', '" abc "', ' " abc " '],
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
                {
                    "title": "test_mix_valid_and_invalid",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "mix_valid_and_invalid"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": [" abc", "abc  def", "abc def "],
                    },
                },
                {
                    "title": "test_mixed_case_spaces",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "mixed_case_spaces"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["Abc  Def", "aBC   dEF", "Ab C  Def"],
                    },
                },
                {
                    "title": "test_text_with_numbers",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "text_with_numbers"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["abc 123", " 123 abc "],
                    },
                },
                {
                    "title": "test_special_characters",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "special_characters"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["abc  !@#", "abc!  @#", "abc !@#  "],
                    },
                },
                {
                    "title": "test_long_strings",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "long_strings"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["This is a  very long string with multiple spaces in between words.", 
                                                    "Another long string    with multiple issues    in between."],
                    },
                },
                {
                    "title": "test_multiple_sentences",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "multiple_sentences"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["This is a sentence.  This is another sentence.", 
                                                    "Sentence one.   Sentence two.", 
                                                    "   Leading space. Trailing space.   "],
                    },
                },
                {
                    "title": "test_new_lines_and_tabs",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "new_lines_and_tabs"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["abc  \ndef", "\tabc def", "abc def\t"],
                    },
                },
                {
                    "title": "test_all_spaces",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "all_spaces"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["     ", "  ", " "],
                    },
                },
                {
                    "title": "test_mix_spaces_and_valid",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "mix_spaces_and_valid"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["    ", " abc ", "  ghi  "],
                    },
                },
                {
                    "title": "test_edge_case_spaces",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "edge_case_spaces"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": [" ", "abc def ", " abc def"],
                    },
                },
                {
                    "title": "test_non_ascii_characters",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "non_ascii_characters"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["abc  äöü", " äöü", "äöü  "],
                    },
                },
                {
                    "title": "test_punctuation_with_spaces",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "punctuation_with_spaces"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": ["abc , def", "abc ,def", "abc,def  "],
                    },
                },
                {
                    "title": "test_quotes_with_spaces",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "quotes_with_spaces"},
                    "out": {
                        "success": False,
                        "partial_unexpected_list": [' "abc"', '"abc" ', '" abc "', ' " abc " '],
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
        "regex": r'(^\s+)|(\s{2,})|(\s+$)',
        "mostly": 0.9
    }

    def validate_configuration(self, configuration: Optional[ExpectationConfiguration]):
        super().validate_configuration(configuration)
        assert configuration is not None
        assert "regex" not in configuration.kwargs, "regex cannot be altered"


expectation = ExpectColumnValuesToNotContainSpacingSmell()
expectation.register_data_smell()
del expectation
