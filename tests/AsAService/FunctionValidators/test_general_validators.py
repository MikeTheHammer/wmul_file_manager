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
from wmul_file_manager.AsAService import _dictionary_validator, _required_arguments_validator
import pytest

@pytest.mark.skip
def test_dictionary_validator__not_a_dict():
    with pytest.raises(ValueError, match=f"The configuration requires a dictionary type. Instead, it received '<class 'bool'>'."):
        _dictionary_validator(False) # type: ignore

@pytest.mark.skip
def test_dictionary_validator__is_a_dict():
    assert _dictionary_validator({})

@pytest.mark.skip
def test_dictionary_validator__is_a_dict_not_empty():
    assert _dictionary_validator({"foo": True})

@pytest.mark.skip
def test_required_arguments_validator__no_arguments_required_none_supplied():
    arguments_dict = {}
    required_arguments = []
    assert _required_arguments_validator(function_arguments_dict=arguments_dict, required_arguments=required_arguments)

@pytest.mark.skip
def test_required_arguments_validator__no_arguments_required_some_supplied():
    arguments_dict = {"Foo": True, "Bar": 12, "Baz": []}
    required_arguments = []
    assert _required_arguments_validator(function_arguments_dict=arguments_dict, required_arguments=required_arguments)

@pytest.mark.skip
def test_required_arguments_validator__arguments_required_none_supplied():
    arguments_dict = {}
    required_arguments = ["Foo", "Bar"]
    with pytest.raises(
        ValueError,
        match="The function configuration is missing required argument '(Foo|Bar)' ."
    ):
        _required_arguments_validator(function_arguments_dict=arguments_dict, required_arguments=required_arguments)

@pytest.mark.skip
def test_required_arguments_validator__arguments_required_some_supplied():
    arguments_dict = {"Foo": True}
    required_arguments = ["Foo", "Bar"]
    with pytest.raises(
        ValueError,
        match="The function configuration is missing required argument 'Bar' ."
    ):
        _required_arguments_validator(function_arguments_dict=arguments_dict, required_arguments=required_arguments)

@pytest.mark.skip
def test_required_arguments_validator__arguments_required_all_supplied():
    arguments_dict = {"Foo": True, "Bar": 12}
    required_arguments = ["Foo", "Bar"]
    assert _required_arguments_validator(function_arguments_dict=arguments_dict, required_arguments=required_arguments)

@pytest.mark.skip
def test_required_arguments_validator__arguments_required_all_and_more_supplied():
    arguments_dict = {"Foo": True, "Bar": 12, "Baz": []}
    required_arguments = ["Foo", "Bar"]
    assert _required_arguments_validator(function_arguments_dict=arguments_dict, required_arguments=required_arguments)
