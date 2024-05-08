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
from wmul_file_manager.ConvertFolderToMP4 import _delete_files, _ConversionFileInformation, \
    _ConversionFileInformationType
from wmul_test_utils import make_namedtuple, assert_lists_contain_same_items, assert_has_only_these_calls


def test_delete_files(fs):
    root_folder = Path("/temp/root")
    folder_1 = root_folder / "folder_1"
    file_1 = folder_1 / "file_1.wav"
    file_3 = folder_1 / "file_3.wav"
    folder_1_subfolder_1 = folder_1 / "subfolder_1"
    file_4 = folder_1_subfolder_1 / "file_4.wav"
    folder_2 = root_folder / "folder_2"
    file_6 = folder_2 / "file_6.wav"

    final_folder = Path("/temp/final")

    fs.create_dir(root_folder)
    fs.create_dir(folder_1)
    fs.create_file(file_1)
    fs.create_file(file_3)
    fs.create_dir(folder_1_subfolder_1)
    fs.create_file(file_4)
    fs.create_dir(folder_2)
    fs.create_file(file_6)
    fs.create_dir(final_folder)

    file_1_information = _ConversionFileInformation(
        _ConversionFileInformationType.Converted_File, 
        file_1, 
        root_folder, 
        final_folder
        )
    
    file_3_information = _ConversionFileInformation(
        _ConversionFileInformationType.Raw_File, 
        file_3, 
        root_folder, 
        final_folder
    )

    file_4_information = _ConversionFileInformation(
        _ConversionFileInformationType.Converted_File, 
        file_4, 
        root_folder, 
        final_folder
    )

    file_6_information = _ConversionFileInformation(
        _ConversionFileInformationType.Converted_File, 
        file_6, 
        root_folder, 
        final_folder
    )

    list_of_files_for_deletion = [
        file_1_information, 
        file_3_information,
        file_4_information,
        file_6_information
    ]

    assert file_1.exists()
    assert file_3.exists()
    assert file_4.exists()
    assert file_6.exists()

    _delete_files(list_of_files_for_deletion=list_of_files_for_deletion)

    assert not file_1.exists()
    assert file_3.exists()
    assert not file_4.exists()
    assert not file_6.exists()
