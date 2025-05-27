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
import pytest
import yaml
from pathlib import Path
from wmul_file_manager.AsAService import FileManagerService
from wmul_file_manager.BulkCopier import BulkCopier


def test_load_config_from_file_valid(fs):
    configuration_string = r"""
Thing_1:
    bulk-copier:
        source_directories:
            - "C:\\Temp_1"
            - "C:\\Temp_2"
            - "C:\\Temp_3"
        destination_directory: "C:\\Destination"
        exclude_suffixes: 
            - ".sfk"
            - ".pk"
        ignore_directories:
            - "C:\\Temp_1\\Bad Files"
        force_copy: True
        delete_old_files: True
"""

    config_filename = "C:\\fileman\\config.yaml"

    fs.create_file(config_filename, contents=configuration_string)

    expected_dictionary = {
        "Thing_1": {
            "bulk-copier": {
                "source_directories": [
                    "C:\\Temp_1",
                    "C:\\Temp_2",
                    "C:\\Temp_3"
                ],
                "destination_directory": "C:\\Destination",
                "exclude_suffixes": [
                    ".sfk",
                    ".pk"
                ],
                "ignore_directories": [
                    "C:\\Temp_1\\Bad Files"
                ],
                "force_copy": True,
                "delete_old_files": True
            }
        }
    }

    fms = FileManagerService(config_filename=config_filename)

    result = fms._load_config_from_file()

    assert result == expected_dictionary



def test_load_config_from_file_not_valid(fs):
    configuration_string = r"""
Thing_1
    bulk-copier:
        source_directories:
            - "C:\\Temp_1"
            - "C:\\Temp_2"
            - "C:\\Temp_3"
        destination_directory: "C:\\Destination"
        exclude_suffixes: 
            - ".sfk"
            - ".pk"
        ignore_directories:
            - "C:\\Temp_1\\Bad Files"
        force_copy: True
        delete_old_files: True
"""

    config_filename = "C:\\fileman\\config.yaml"

    fs.create_file(config_filename, contents=configuration_string)

    fms = FileManagerService(config_filename=config_filename)

    with pytest.raises(yaml.YAMLError):
        fms._load_config_from_file()

