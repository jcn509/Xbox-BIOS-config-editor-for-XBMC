"""Tests for configs.validators.RegexPatternMatchValidator

Tests values in scenarios where both the Python format regex and config file
format regex are supplied as well as scenarios where only the Python format
regex is supplied
"""
from collections import namedtuple
from itertools import product
import pytest

from lib.configs import ConfigFieldValueError
from lib.configs.validators import RegexPatternMatchValidator

RegexValidInvalid = namedtuple(
    "RegexValidInvalid", ["pattern", "valid_values", "invalid_values"]
)

_REGEX_VALID_INVALID = (
    RegexValidInvalid(".*", ("a", "", "asdasdasdasd"), ()),
    RegexValidInvalid("^$", (""), ("a", "$", "^", "^$")),
)
_ERROR_MESSAGES = ("asdadasdasdadasdad", "error message", None)


def _get_all_combos(
    regex_valid_invalid_list_1, regex_valid_invalid_list_2, error_messages, get_values
):
    """:returns: a generator for tuples with:\
            - the pattern property from a regex from\
            regex_valid_invalid_list_1 as the first element\
            - the pattern from a regex in regex_valid_invalid_list_2 as the\
            second element\
            - an error message from error_messages as the third element\
            - a value obtained from\
            get_values(the regex from regex_valid_invalid_list_1) as the\
            final element\
            for all possible combinations of these values
    """
    return (
        (regex1.pattern, regex2.pattern, error_message, value)
        for regex1, regex2, error_message in product(
            regex_valid_invalid_list_1, regex_valid_invalid_list_2, error_messages
        )
        for value in get_values(regex1)
    )


# Re-used so don't want a generator
_VALID_TEST_PARAMS_BOTH_REGEX_SUPPLIED = tuple(
    _get_all_combos(
        _REGEX_VALID_INVALID,
        _REGEX_VALID_INVALID,
        _ERROR_MESSAGES,
        lambda regex_valid_invalid: regex_valid_invalid.valid_values,
    )
)
_VALID_TEST_PARAMS_ONLY_PYTHON_REGEX_SUPPLIED = tuple(
    _get_all_combos(
        _REGEX_VALID_INVALID,
        (RegexValidInvalid(None, None, None),),
        _ERROR_MESSAGES,
        lambda regex_valid_invalid: regex_valid_invalid.valid_values,
    )
)
_INVALID_TEST_PARAMS_BOTH_REGEX_SUPPLIED = tuple(
    _get_all_combos(
        _REGEX_VALID_INVALID,
        _REGEX_VALID_INVALID,
        _ERROR_MESSAGES,
        lambda regex_valid_invalid: regex_valid_invalid.invalid_values,
    )
)
_INVALID_TEST_PARAMS_ONLY_PYTHON_REGEX_SUPPLIED = tuple(
    _get_all_combos(
        _REGEX_VALID_INVALID,
        (RegexValidInvalid(None, None, None),),
        _ERROR_MESSAGES,
        lambda regex_valid_invalid: regex_valid_invalid.invalid_values,
    )
)


def _swap_pattern_order(test_params):
    """Takes a tuple from :_get_all_combos: and swaps the first two elements
    """
    return tuple(
        (pattern2, pattern1, error_message, value)
        for (pattern1, pattern2, error_message, value) in test_params
    )


@pytest.mark.parametrize(
    "config_regex_pattern, python_regex_pattern, error_message, value",
    _VALID_TEST_PARAMS_BOTH_REGEX_SUPPLIED
    + _swap_pattern_order(_VALID_TEST_PARAMS_ONLY_PYTHON_REGEX_SUPPLIED),
)
def test_validate_in_config_file_format_valid(
    config_regex_pattern, python_regex_pattern, error_message, value
):
    """Ensures that no error is thrown when validating a valid value in
    config file format
    """
    validator = RegexPatternMatchValidator(
        python_regex_pattern, config_regex_pattern, error_message
    )
    validator.validate_in_config_file_format(value)


@pytest.mark.parametrize(
    "config_regex_pattern, python_regex_pattern, error_message, value",
    _INVALID_TEST_PARAMS_BOTH_REGEX_SUPPLIED
    + _swap_pattern_order(_INVALID_TEST_PARAMS_ONLY_PYTHON_REGEX_SUPPLIED),
)
def test_validate_in_config_file_format_invalid(
    config_regex_pattern, python_regex_pattern, error_message, value
):
    """Ensures that a ConfigFieldValueError is raised and that the error
    message contains error_message if its not None and if it is None then
    either config_regex_pattern if it was supplied or python_regex_pattern if
    it was not
    """
    validator = RegexPatternMatchValidator(
        python_regex_pattern, config_regex_pattern, error_message
    )
    with pytest.raises(ConfigFieldValueError) as excinfo:
        validator.validate_in_config_file_format(value)
    if error_message is None:
        if config_regex_pattern is None:
            assert python_regex_pattern in str(excinfo.value)
        else:
            assert config_regex_pattern in str(excinfo.value)
    else:
        assert str(error_message) in str(excinfo.value)
    assert value in str(excinfo.value)


# Note: the parameters are the other way around to the config format test
@pytest.mark.parametrize(
    "python_regex_pattern, config_regex_pattern, error_message, value",
    _VALID_TEST_PARAMS_BOTH_REGEX_SUPPLIED,
)
def test_validate_in_python_format_valid(
    python_regex_pattern, config_regex_pattern, error_message, value
):
    """Ensures that no exception is thrown when validating a valid value in
    Python format
    """
    validator = RegexPatternMatchValidator(
        python_regex_pattern, config_regex_pattern, error_message
    )
    validator.validate_in_python_format(value)


@pytest.mark.parametrize(
    "python_regex_pattern, config_regex_pattern, error_message, value",
    _INVALID_TEST_PARAMS_BOTH_REGEX_SUPPLIED,
)
def test_validate_in_python_format_invalid(
    python_regex_pattern, config_regex_pattern, error_message, value
):
    """Ensures that a ConfigFieldValueError is raised and that the error
    message contains error_message if its not None and if it is None then
    python_regex_pattern
    """
    validator = RegexPatternMatchValidator(
        python_regex_pattern, config_regex_pattern, error_message
    )
    with pytest.raises(ConfigFieldValueError) as excinfo:
        validator.validate_in_python_format(value)
    if error_message is None:
        assert python_regex_pattern in str(excinfo.value)
    else:
        assert str(error_message) in str(excinfo.value)
    assert value in str(excinfo.value)
