from collections import namedtuple
from itertools import product
import pytest

from resources.lib.configs import ConfigFieldValueError
from resources.lib.configs.validators import RegexPatternMatchValidator

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
        (RegexValidInvalid(None, None, None), ),
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
        (RegexValidInvalid(None, None, None), ),
        _ERROR_MESSAGES,
        lambda regex_valid_invalid: regex_valid_invalid.invalid_values,
    )
)


def swap_pattern_order(test_params):
    return tuple(
        (pattern2, pattern1, error_message, value)
        for (pattern1, pattern2, error_message, value) in test_params
    )


@pytest.mark.parametrize(
    "config_regex_pattern, python_regex_pattern, error_message, value",
    _VALID_TEST_PARAMS_BOTH_REGEX_SUPPLIED
    + swap_pattern_order(_VALID_TEST_PARAMS_ONLY_PYTHON_REGEX_SUPPLIED),
)
def test_validate_in_config_format_valid(
    config_regex_pattern, python_regex_pattern, error_message, value
):
    validator = RegexPatternMatchValidator(
        python_regex_pattern, config_regex_pattern, error_message
    )
    validator.validate_in_config_format(value)


@pytest.mark.parametrize(
    "config_regex_pattern, python_regex_pattern, error_message, value",
    _INVALID_TEST_PARAMS_BOTH_REGEX_SUPPLIED
    + swap_pattern_order(_INVALID_TEST_PARAMS_ONLY_PYTHON_REGEX_SUPPLIED),
)
def test_validate_in_config_format_invalid(
    config_regex_pattern, python_regex_pattern, error_message, value
):
    validator = RegexPatternMatchValidator(
        python_regex_pattern, config_regex_pattern, error_message
    )
    with pytest.raises(ConfigFieldValueError) as excinfo:
        validator.validate_in_config_format(value)
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
