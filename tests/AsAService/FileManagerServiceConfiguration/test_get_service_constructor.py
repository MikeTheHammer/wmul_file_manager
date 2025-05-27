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
from wmul_file_manager.AsAService import _get_service_constructor
from wmul_test_utils import multiple_random_case_strings


def test_bad_service_type():
    service_type = "mock_service_type"

    expected_error_message = re.escape(
        f"The service wants service type '{service_type}', but there is no service available with that type. The "
        f"available services are: ['bulkcopier']"
    )

    with pytest.raises(ValueError, match=expected_error_message):
        _get_service_constructor(
            service_type=service_type
        )


def test_bulk_copier_service():
    from wmul_file_manager.BulkCopier import BulkCopierArguments
    bulk_copier_service_type = "bulkcopier"

    service_types_under_test = multiple_random_case_strings(
        input_string=bulk_copier_service_type
    )

    service_types_under_test.append(bulk_copier_service_type) # Always check the default casing.

    for st in service_types_under_test:
        result = _get_service_constructor(service_type=st)
        assert result == BulkCopierArguments
