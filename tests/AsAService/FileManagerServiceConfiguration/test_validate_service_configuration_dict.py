"""
@Author = 'Mike Stanley'

============ Change Log ============
2025-May-23 = Created.

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
import pytest
import re
from wmul_file_manager.AsAService import FileManagerServiceConfiguration


def test_all_good():
    service_configuration_dict = {
        "Function_1": True
    }

    assert FileManagerServiceConfiguration._validate_service_configuration_dict(
        service_configuration_dict=service_configuration_dict
    )


@pytest.mark.parametrize("service_configuration_dict_type", ["Bool", "List", "Int"])
def test_not_a_dict(service_configuration_dict_type):
    match service_configuration_dict_type:
        case "Bool":
            service_configuration_dict = True
        case "List":
            service_configuration_dict = []
        case "Int":
            service_configuration_dict = 12
        case _:
            service_configuration_dict = object()

    expected_error_message = re.escape(
        f"The configuration for the service requires a dictionary type. Instead, it received Type: "
        f"'{type(service_configuration_dict)}', {service_configuration_dict} ."
    )

    with pytest.raises(ValueError, match=expected_error_message):
        FileManagerServiceConfiguration._validate_service_configuration_dict(
            service_configuration_dict=service_configuration_dict
        )
    

def test_empty_dict():
    service_configuration_dict = {}

    expected_error_message = re.escape(
        f"The configuration for the service does not have the correct number of function names. There must be exactly "
        f"one function name per service. This entry has 0: [] ."
    )

    with pytest.raises(ValueError, match=expected_error_message):
        FileManagerServiceConfiguration._validate_service_configuration_dict(
            service_configuration_dict=service_configuration_dict
        )


def test_three_item_dict():
    service_configuration_dict = {
        "Function_1": True,
        "Function_2": True,
        "Function_3": True

    }

    expected_error_message = re.escape(
        f"The configuration for the service does not have the correct number of function names. There must be exactly "
        f"one function name per service. This entry has 3: ['Function_1', 'Function_2', 'Function_3'] ."
    )

    with pytest.raises(ValueError, match=expected_error_message):
        FileManagerServiceConfiguration._validate_service_configuration_dict(
            service_configuration_dict=service_configuration_dict
        )
