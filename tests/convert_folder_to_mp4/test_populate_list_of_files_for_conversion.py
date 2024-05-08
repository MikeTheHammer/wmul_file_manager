"""
@Author = 'Mike Stanley'

============ Change Log ============
2024-May-07 = Created.

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
from wmul_file_manager.ConvertFolderToMP4 import _populate_list_of_files_for_conversion, _ConversionFileInformation
from wmul_test_utils import make_namedtuple, assert_lists_contain_same_items


@pytest.fixture(scope="function")
def setup_populate_list_of_files_for_conversion(fs):
    root_folder = Path("/temp/root")
    folder_1 = root_folder / "folder_1"
    folder_1_file_1 = folder_1 / "file_1.wav"
    folder_1_file_2 = folder_1 / "file_2.jpg"
    folder_1_file_3 = folder_1 / "file_3.wAv"
    folder_1_subfolder_1 = folder_1 / "subfolder_1"
    folder_1_subfolder_1_file_4 = folder_1_subfolder_1 / "file_4.wav"
    folder_2 = root_folder / "folder_2"
    folder_2_file_5 = folder_2 / "file_5.mp3"
    folder_2_file_6 = folder_2 / "file_6.wav"
    folder_2_subfolder_2 = folder_2 / "subfolder_2"

    final_folder = Path("/temp/final")

    fs.create_dir(root_folder)
    fs.create_dir(folder_1)
    fs.create_file(folder_1_file_1)
    fs.create_file(folder_1_file_2)
    fs.create_file(folder_1_file_3)
    fs.create_dir(folder_1_subfolder_1)
    fs.create_file(folder_1_subfolder_1_file_4)
    fs.create_dir(folder_2)
    fs.create_file(folder_2_file_5)
    fs.create_file(folder_2_file_6)
    fs.create_dir(folder_2_subfolder_2)
    fs.create_dir(final_folder)

    file_info_factory = _ConversionFileInformation.get_factory(
        root_path=root_folder,
        converted_files_final_folder=final_folder
    )

    expected_files = [
        folder_1_file_1,
        folder_1_file_3,
        folder_1_subfolder_1_file_4,
        folder_2_file_6
    ]

    results = _populate_list_of_files_for_conversion(
        root_folder, 
        file_info_factory,
        ".wav"
    )

    return make_namedtuple(
        "setup_populate_list_of_files_for_conversion",
        expected_files=expected_files,
        results=results,
    )

def test_correct_types_returned(setup_populate_list_of_files_for_conversion):
    results = setup_populate_list_of_files_for_conversion.results
    assert isinstance(results, list)
    for result in results:
        assert isinstance(result, _ConversionFileInformation)

def test_correct_items_returned(setup_populate_list_of_files_for_conversion):
    results = setup_populate_list_of_files_for_conversion.results
    expected_files = setup_populate_list_of_files_for_conversion.expected_files

    result_filenames = [result.original_file_name for result in results]
    assert_lists_contain_same_items(expected_files, result_filenames)
