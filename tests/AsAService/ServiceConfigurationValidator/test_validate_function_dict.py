"""
@Author = 'Mike Stanley'

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
from wmul_file_manager.AsAService import ServiceConfigurationValidator
import pytest
import re


@pytest.mark.skip
def test_all_good():
    scv = ServiceConfigurationValidator()

    configuration_under_test = {
        "Thing 1": { "bar": False },
        "Thing 2": { "foo": "bar" },
        "Thing 3": { "baz": 12}
    }
    
    for _, function_dict in configuration_under_test.items():
        assert scv._validate_function_dict(function_dict=function_dict)

@pytest.mark.skip    
def test_not_a_dict():
    scv = ServiceConfigurationValidator()

    with pytest.raises(ValueError, match=f"The configuration requires a dictionary type. Instead, it received '<class 'bool'>'."):
        scv._validate_function_dict(False)

@pytest.mark.skip
def test_empty_dict():
    scv = ServiceConfigurationValidator()

    with pytest.raises(
        ValueError, 
        match=f"The inventory entry does not have the correct number of function names. There must be exactly one "
              f"function name per inventory entry. This entry has 0: ."
    ):
        scv._validate_function_dict({})

@pytest.mark.skip
def test_dict_with_two_keys():
    scv = ServiceConfigurationValidator()

    expected_exception_string = re.escape(
        "The inventory entry does not have the correct number of function names. There must be exactly one function "
        "name per inventory entry. This entry has 2: ['bar', 'foo'] ."
    )

    with pytest.raises(
        ValueError, 
        match=expected_exception_string
    ):
        scv._validate_function_dict({ "bar": False, "foo": "bar" })


# def test_validate_service_configuration_function_length():
#     scv = ServiceConfigurationValidator()

