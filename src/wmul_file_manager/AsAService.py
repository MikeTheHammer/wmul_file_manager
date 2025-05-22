"""
@Author = 'Mike Stanley'

Allows wmul_file_manager to be run as a service. 


============ Change Log ============
2025-May-22 = Created.

============ License ============
The MIT License (MIT)

Copyright (c) 2025 Michael Stanley

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from collections.abc import Callable
from dataclasses import dataclass
import re
import yaml


@dataclass
class _FunctionValidator:
    name: str
    regex: re.Pattern
    validate: Callable[[dict], bool]


def _dictionary_validator(item_under_test: dict) -> bool:
    if not isinstance(item_under_test, dict):
        raise ValueError(
            f"The configuration requires a dictionary type. Instead, it received '{type(function_arguments_dict)}'."
        )
    return True


def _list_validator(item_under_test: list) -> bool:
    if not isinstance(item_under_test, list):
        raise ValueError(
            f"This argument requires a list type. Instead, it received '{type(function_arguments_dict)}'."
        )
    return True


def _required_arguments_validator(arguments_dict: dict, required_arguments: list[str]) -> bool:
    for ra in required_arguments:
        if not ra in arguments_dict:
            raise ValueError(f"The function configuration is missing required argument '{ra}' .")
    return True


def _bulk_copier_validator(function_arguments_dict) -> bool:
    try:
        _dictionary_validator(item_under_test=function_arguments_dict)
        _required_arguments_validator(
            arguments_dict=function_arguments_dict,
            required_arguments=["source_directories", "destination_directory"]
        )
        source_directories = function_arguments_dict["source_directories"]
        _list_validator(source_directories)
    except ValueError as ve:
        raise ValueError("Bulk Copier configuration is invalid.") from ve
    return True

_function_validators: list[_FunctionValidator] = [
    _FunctionValidator(name="Bulk Copier", regex=re.compile("bulk[-|_| ]?copier"), validate=_bulk_copier_validator)
]




class ServiceConfigurationValidator:

    def validate_service_configuration(self, configuration):
        for inventory_name, function_dict in configuration.items():
            try:
                self._validate_function_dict(function_dict=function_dict)
                for function_name, function_arguments_dict in function_dict.items():
                    function_validator = self._find_function_validator(function_name)
                    function_validator.validate(function_arguments_dict)
            except ValueError as ve:
                raise ValueError(f"The inventory entry, '{inventory_name}' has an invalid configuration.") from ve
            

    def _validate_function_dict(self, function_dict) -> bool:
        _dictionary_validator(item_under_test=function_dict)

        if (count_of_function_names := len(function_dict)) != 1:
            raise ValueError(
                f"The inventory entry does not have the correct number of function names. There must be exactly one "
                f"function name per inventory entry. This entry has {count_of_function_names}: "
                f"{list(function_dict.keys())} ."
            )

        return True

    def _find_function_validator(self, function_name):
        for fv in _function_validators:
            if fv.regex.fullmatch(function_name):
                return fv
        raise ValueError(
            f"The function_name '{function_name}', cannot be matched to a function available in wmul_file_manager. The "
            "valid function names are: 'bulk-copier'.")
     


@dataclass
class WMULFileManagerService:
    config_filename: str

    def _load_config_from_file(self):
        with open(self.config_filename) as config_file:
            return yaml.safe_load(config_file.read())
        
    def validate_configuration(self, configuration):
        
        ...

    def service_loop(self):
        configuration = self._load_config_from_file()

    
