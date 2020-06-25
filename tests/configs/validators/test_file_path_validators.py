"""Tests for DVDFilePathValidator, HDDFilePathValidator and
OptionalHDDFilePathValidator from configs.validators

Valid file paths in Python format are of the form C:\\...
Valid file paths in config file format are of the form \\Device\\...
Valid optional file paths may be None in Python format or 0 in config file
format
"""
from itertools import chain
import pytest

from lib.configs import ConfigFieldValueError
from lib.configs.validators.file_path_validators import (
    DVDFilePathValidator,
    HDDFilePathValidator,
    OptionalHDDFilePathValidator,
)


# Config path format
## HDD
_VALID_HDD_CONFIG_FILE_PATHS = (
    "\\Device\\Harddisk0\\Partition2\\flubber.x",
    "\\Device\\Harddisk0\\Partition1\\somedir\\flubber.x",
    "\\Device\\Harddisk0\\Partition6\\a\\b\\c\\logo.bmp",
)

_INVALID_HDD_CONFIG_FILE_PATHS = (
    "\\Device\\Harddisk0\\Partition7\\file",  # No extension
    "\\Device\\Harddisk1\\Partition2\\flubber.x",
    "\\Device\\Harddisk\\Partition1\\somedir\\flubber.x",
    "\\device\\Harddisk0\\Partition6\\a\\b\\c\\logo.bmp",
    "\\Device\\harddisk0\\Partition7\\file",
    "\\Device\\Harddisk0\\Partition\\file",
    "\\Device\\Harddisk0\\file",
    "\\Device\\Harddisk0\\Partition0\\file",
    "\\Device\\Harddisk0\\Partition3\\file",
    "\\Device\\Harddisk0\\Partition4\\file",
    "\\Device\\Harddisk0\\Partition5\\file",
    "Device\\Harddisk0\\Partition7\\file",
    "/Device/Harddisk0/Partition7/file",
    "File.xbe",
)

## DVD
_VALID_DVD_CONFIG_FILE_PATHS = (
    "\\Device\\CdRom0\\flubber.x",
    "\\Device\\CdRom0\\somedir\\flubber.x",
    "\\Device\\CdRom0\\a\\b\\c\\logo.bmp",
)

_INVALID_DVD_CONFIG_FILE_PATHS = (
    "\\Device\\CdRom0\\file",  # No extension
    "\\Device\\CdRom1\\flubber.x",
    "\\Device\\CdRom2\\somedir\\flubber.x",
    "\\Device\\CdRom\\a\\b\\c\\logo.bmp",
    "\\Device\\cdrom0\\file",
    "\\device\\CdRom\\a\\b\\c\\logo.bmp",
    "\\CdRom0\\file",
    "Device\\CdRom0\\file",
    "/Device/CdRom0/file",
)

# Python path format
## HDD
_VALID_HDD_PYTHON_FILE_PATHS = (
    "C:\\xboxdash.xbe",
    "E:\\xboxdash.xbe",
    "F:\\xboxdash.xbe",
    "G:\\xboxdash.xbe",
    "C:\\directtory\\xboxdash.bmp",
)

_INVALID_HDD_PYTHON_FILE_PATHS = (
    "A:\\xboxdash.xbe",
    "B:\\xboxdash.xbe",
    "X:\\xboxdash.xbe",
    "Y:\\xboxdash.xbe",
    "Z:\\xboxdash.xbe",
    "C:xboxdash.xbe",
    "C\\xboxdash.xbe",
    "xboxdash.xbe",
    "c:\\xboxdash.xbe",
    "C:/xboxdash.xbe",
)

## DVD
_VALID_DVD_PYTHON_FILE_PATHS = (
    "D:\\default.xbe",
    "D:\\test\\other.xbe",
)

_INVALID_DVD_PYTHON_FILE_PATHS = (
    "D:\\file",  # No extension
    "D:default.xbe",
    "D:/test/other.xbe",
    "D:/file",
    "file.xbe",
)


def _get_file_extension(path):
    return path.split(".")[-1] if "." in path else None


def _get_all_file_extensions(paths):
    """Returns a set of all the file extensions for all the file paths in 
    paths
    """
    return {_get_file_extension(path) for path in paths}


def _pair_by_file_extension(paths):
    """return a tuple whose elements are tuples where the first element is a
    path from paths and the second is the file extension
    """
    return ((_get_file_extension(path), path) for path in paths)


def _get_params(validator_classes, paths):
    """Returns a tuple containing tuples that of the form
    (validator_class, file_path, file extension) for every combination of
    values in validator_classes and paths
    """
    return (
        (validator_class, file_path, extension)
        for validator_class in validator_classes
        for file_path, extension in _pair_by_file_extension(paths)
    )


@pytest.mark.parametrize(
    "validator_class, extension, path",
    chain(
        _get_params(
            (HDDFilePathValidator, OptionalHDDFilePathValidator),
            _VALID_HDD_CONFIG_FILE_PATHS,
        ),
        _get_params((DVDFilePathValidator,), _VALID_DVD_CONFIG_FILE_PATHS),
        (
            (OptionalHDDFilePathValidator, "txt", "0"),
        ),  # Extension does not matter here...
    ),
)
def test_validate_in_config_file_format_valid(validator_class, extension, path):
    """Ensures that no errors are thrown when validating valid file paths in
    config file format

    Valid file paths in config file format are of the form \\Device\\...
    Valid optional file paths may be 0
    """
    validator = validator_class(extension)
    validator.validate_in_config_file_format(path)


@pytest.mark.parametrize(
    "validator_class, extension, path",
    chain(
        _get_params(
            (HDDFilePathValidator, OptionalHDDFilePathValidator),
            _INVALID_HDD_CONFIG_FILE_PATHS
            + _VALID_DVD_CONFIG_FILE_PATHS
            + _INVALID_DVD_CONFIG_FILE_PATHS
            + _VALID_HDD_PYTHON_FILE_PATHS
            + _INVALID_HDD_PYTHON_FILE_PATHS
            + _VALID_DVD_PYTHON_FILE_PATHS
            + _INVALID_DVD_PYTHON_FILE_PATHS,
        ),
        _get_params(
            (DVDFilePathValidator,),
            _VALID_HDD_CONFIG_FILE_PATHS
            + _INVALID_HDD_CONFIG_FILE_PATHS
            + _INVALID_DVD_CONFIG_FILE_PATHS
            + _VALID_HDD_PYTHON_FILE_PATHS
            + _INVALID_HDD_PYTHON_FILE_PATHS
            + _VALID_DVD_PYTHON_FILE_PATHS
            + _INVALID_DVD_PYTHON_FILE_PATHS,
        ),
        (  # Extension does not matter here...
            (HDDFilePathValidator, "txt", "0"),
            (DVDFilePathValidator, "txt", "0"),
            (OptionalHDDFilePathValidator, "txt", "1"),
            (OptionalHDDFilePathValidator, "txt", "False"),
            (HDDFilePathValidator, "txt", None),
            (DVDFilePathValidator, "txt", None),
            (OptionalHDDFilePathValidator, "txt", None),
        ),
    ),
)
def test_validate_in_config_file_format_invalid(validator_class, extension, path):
    """Ensures that a ConfigFieldValueError is thrown when parsing an invalid
    path in config file format
    """
    extension = extension if extension is not None else ""
    validator = validator_class(extension)
    with pytest.raises(ConfigFieldValueError) as excinfo:
        validator.validate_in_config_file_format(path)
    assert str(path) in str(excinfo.value)
    assert str(extension) in str(excinfo.value)


@pytest.mark.parametrize(
    "validator_class, extension, path",
    chain(
        _get_params(
            (HDDFilePathValidator, OptionalHDDFilePathValidator),
            _VALID_HDD_PYTHON_FILE_PATHS,
        ),
        _get_params((DVDFilePathValidator,), _VALID_DVD_PYTHON_FILE_PATHS),
        (  # Extension does not matter here...
            (OptionalHDDFilePathValidator, "txt", None),
        ),
    ),
)
def test_validate_in_python_format_valid(validator_class, extension, path):
    """Ensures that no errors are thrown when validating valid file paths in
    Python format


    Valid file paths in Python format are of the form C:\\...
    Valid optional file paths may be None
    """
    validator = validator_class(extension)
    validator.validate_in_python_format(path)


@pytest.mark.parametrize(
    "validator_class, extension, path",
    chain(
        _get_params(
            (HDDFilePathValidator, OptionalHDDFilePathValidator),
            _VALID_HDD_CONFIG_FILE_PATHS
            + _INVALID_HDD_CONFIG_FILE_PATHS
            + _VALID_DVD_CONFIG_FILE_PATHS
            + _INVALID_DVD_CONFIG_FILE_PATHS
            + _INVALID_HDD_PYTHON_FILE_PATHS
            + _VALID_DVD_PYTHON_FILE_PATHS
            + _INVALID_DVD_PYTHON_FILE_PATHS,
        ),
        _get_params(
            (DVDFilePathValidator,),
            _VALID_HDD_CONFIG_FILE_PATHS
            + _INVALID_HDD_CONFIG_FILE_PATHS
            + _VALID_DVD_CONFIG_FILE_PATHS
            + _INVALID_DVD_CONFIG_FILE_PATHS
            + _VALID_HDD_PYTHON_FILE_PATHS
            + _INVALID_HDD_PYTHON_FILE_PATHS
            + _INVALID_DVD_PYTHON_FILE_PATHS,
        ),
        (  # Extension does not matter here...
            (HDDFilePathValidator, "txt", "0"),
            (DVDFilePathValidator, "txt", "0"),
            (HDDFilePathValidator, "txt", None),
            (DVDFilePathValidator, "txt", None),
            (OptionalHDDFilePathValidator, "txt", "0"),
            (OptionalHDDFilePathValidator, "txt", "1"),
            (OptionalHDDFilePathValidator, "txt", "None"),
            (OptionalHDDFilePathValidator, "txt", False),
        ),
    ),
)
def test_validate_in_python_format_invalid(validator_class, extension, path):
    """Ensures that a ConfigFieldValueError is thrown when parsing an invalid
    path in Python format
    """
    extension = extension if extension is not None else ""
    validator = validator_class(extension)
    with pytest.raises(ConfigFieldValueError) as excinfo:
        validator.validate_in_python_format(path)
    assert str(path) in str(excinfo.value)
    assert str(extension) in str(excinfo.value)
