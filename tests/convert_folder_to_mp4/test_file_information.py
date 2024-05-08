"""
@Author = 'Mike Stanley'

============ Change Log ============
2024-May-03 = Created.

============ License ============
The MIT License (MIT)

Copyright (c) 2024 Michael Stanley

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
from pathlib import Path
from wmul_file_manager.ConvertFolderToMP4 import _ConversionFileInformation, _ConversionFileInformationType
from wmul_test_utils import make_namedtuple

@pytest.fixture(scope="function")
def setup_conversion_file_information(fs):
    mock_file_info_type = "mock_file_info_type"
    source_file_path = Path("/foo/bar/baz.mov")
    source_root_path = Path("/foo/")
    converted_files_final_folder = Path("/converted/")

    expected_source_path = source_file_path
    expected_destination_path = Path("/converted/bar/baz.mp4")
    expected_str = "_ConversionFileInformation:\nmock_file_info_type\n\\foo\\bar\\baz.mov"

    file_info_under_test = _ConversionFileInformation(
        file_info_type=mock_file_info_type,
        source_file_path=source_file_path,
        source_root_path=source_root_path,
        converted_files_final_folder=converted_files_final_folder
    )

    return make_namedtuple(
        "setup_conversion_file_information",
        mock_file_info_type=mock_file_info_type,
        source_file_path=source_file_path,
        source_root_path=source_root_path,
        converted_files_final_folder=converted_files_final_folder,
        expected_source_path=expected_source_path,
        expected_destination_path=expected_destination_path,
        expected_str=expected_str,
        file_info_under_test=file_info_under_test
    )

def test_file_info_type_set_correctly(setup_conversion_file_information):
    file_info_under_test = setup_conversion_file_information.file_info_under_test
    mock_file_info_type = setup_conversion_file_information.mock_file_info_type

    assert file_info_under_test.file_info_type == mock_file_info_type

def test_original_file_name_set_correctly(setup_conversion_file_information):
    file_info_under_test = setup_conversion_file_information.file_info_under_test
    source_file_path = setup_conversion_file_information.source_file_path

    assert file_info_under_test.original_file_name == source_file_path

def test_source_path_set_correctly(setup_conversion_file_information):
    file_info_under_test = setup_conversion_file_information.file_info_under_test
    expected_source_path = setup_conversion_file_information.expected_source_path

    assert file_info_under_test.source_path == expected_source_path

def test_destination_path_generated_correctly(setup_conversion_file_information):
    file_info_under_test = setup_conversion_file_information.file_info_under_test
    expected_destination_path = setup_conversion_file_information.expected_destination_path

    assert file_info_under_test.destination_path == expected_destination_path

def test_parents_created(setup_conversion_file_information):
    expected_destination_path = setup_conversion_file_information.expected_destination_path
    destination_parent = expected_destination_path.parent
    assert destination_parent.exists()
    
def test_str(setup_conversion_file_information):
    file_info_under_test = setup_conversion_file_information.file_info_under_test
    expected_str = setup_conversion_file_information.expected_str

    assert str(file_info_under_test) == expected_str

def test_converted_works(setup_conversion_file_information):
    file_info_under_test = setup_conversion_file_information.file_info_under_test
    mock_file_info_type = setup_conversion_file_information.mock_file_info_type
    assert file_info_under_test.file_info_type == mock_file_info_type
    file_info_under_test.converted()
    assert file_info_under_test.file_info_type == _ConversionFileInformationType.Converted_File
