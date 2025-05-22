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


@pytest.mark.skip
def test_find_function_validator_good():
    scv = ServiceConfigurationValidator()

    test_keys_and_expected_validator_names = {
        "bulk-copier": "Bulk Copier",
        "bulk_copier": "Bulk Copier",
        "bulk copier": "Bulk Copier",
        "bulkcopier": "Bulk Copier",
    }

    for test_key, expected_validator_names in test_keys_and_expected_validator_names.items():
        result = scv._find_function_validator(test_key)
        assert result.name == expected_validator_names

@pytest.mark.skip
def test_find_function_validator_bad():
    scv = ServiceConfigurationValidator()

    test_keys_and_expected_error_messages = {
        "bulkasfkdjcopier": 
            "The function_name 'bulkasfkdjcopier', cannot be matched to a function available in wmul_file_manager. "
            "The valid function names are: 'bulk-copier'.",
        "foobar": "The function_name 'foobar', cannot be matched to a function available in wmul_file_manager. "
            "The valid function names are: 'bulk-copier'."
    }

    for test_key, expected_error_message in test_keys_and_expected_error_messages.items():
        with pytest.raises(ValueError, match=expected_error_message):
            result = scv._find_function_validator(test_key)


