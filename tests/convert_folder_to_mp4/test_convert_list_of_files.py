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
from wmul_file_manager.ConvertFolderToMP4 import _convert_list_of_files, _ConversionFileInformation, \
    _ConversionFileInformationType
from wmul_test_utils import make_namedtuple, assert_lists_contain_same_items, assert_has_only_these_calls


@pytest.fixture(scope="function")
def setup_convert_list_of_files(fs, mocker):
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

    def get_return_code(input_file_path, output_file_path):
        if input_file_path == str(file_3): # Simulate a random failure
            return -1
        else:
            return 0

    mock_call_ffmpeg = mocker.Mock(side_effect=get_return_code)

    file_1_information = _ConversionFileInformation(
        _ConversionFileInformationType.Raw_File, 
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
        _ConversionFileInformationType.Raw_File, 
        file_4, 
        root_folder, 
        final_folder
    )

    file_6_information = _ConversionFileInformation(
        _ConversionFileInformationType.Raw_File, 
        file_6, 
        root_folder, 
        final_folder
    )

    list_of_files_for_conversion = [
        file_1_information,
        file_3_information,
        file_4_information,
        file_6_information
    ]

    expected_calls = [
        mocker.call(
            input_file_path=str(file_1_information.source_path), 
            output_file_path=str(file_1_information.destination_path)
        ),
        mocker.call(
            input_file_path=str(file_3_information.source_path), 
            output_file_path=str(file_3_information.destination_path)
        ),
        mocker.call(
            input_file_path=str(file_4_information.source_path), 
            output_file_path=str(file_4_information.destination_path)
        ),
        mocker.call(
            input_file_path=str(file_6_information.source_path), 
            output_file_path=str(file_6_information.destination_path)
        ),
    ]

    expected_files_for_deletion = [
        file_1, 
        file_4,
        file_6
    ]

    results = _convert_list_of_files(
        call_ffmpeg=mock_call_ffmpeg,
        list_of_files_for_conversion=list_of_files_for_conversion
    )

    return make_namedtuple(
        "setup_convert_list_of_files",
        mock_call_ffmpeg=mock_call_ffmpeg,
        expected_calls=expected_calls,
        file_1_information=file_1_information,
        file_3_information=file_3_information,
        file_4_information=file_4_information,
        file_6_information=file_6_information,
        expected_files_for_deletion=expected_files_for_deletion,
        results=results
    )

def test_call_ffmpeg_called_correctly(setup_convert_list_of_files):
    mock_call_ffmpeg = setup_convert_list_of_files.mock_call_ffmpeg
    expected_calls = setup_convert_list_of_files.expected_calls

    assert_has_only_these_calls(mock=mock_call_ffmpeg, calls=expected_calls)

def test_files_marked_as_converted_correctly(setup_convert_list_of_files):
    file_1_information = setup_convert_list_of_files.file_1_information
    file_3_information = setup_convert_list_of_files.file_3_information
    file_4_information = setup_convert_list_of_files.file_4_information
    file_6_information = setup_convert_list_of_files.file_6_information

    assert file_1_information.file_info_type == _ConversionFileInformationType.Converted_File
    assert file_3_information.file_info_type == _ConversionFileInformationType.Raw_File
    assert file_4_information.file_info_type == _ConversionFileInformationType.Converted_File
    assert file_6_information.file_info_type == _ConversionFileInformationType.Converted_File

def test_correct_list_of_files_for_deletion(setup_convert_list_of_files):
    results = setup_convert_list_of_files.results
    expected_files_for_deletion = setup_convert_list_of_files.expected_files_for_deletion

    results_filenames = [result.original_file_name for result in results]

    assert_lists_contain_same_items(expected_files_for_deletion, results_filenames)
