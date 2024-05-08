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
from wmul_file_manager.ConvertFolderToMP4 import _archive_folder
from wmul_test_utils import generate_true_false_matrix_from_list_of_strings, make_namedtuple

archive_folder_params, archive_folder_ids = generate_true_false_matrix_from_list_of_strings(
    "archive_folder_options",
    ["delete_files"]
)

@pytest.fixture(scope="function", params=archive_folder_params, ids=archive_folder_ids)
def setup_archive_folder(mocker, request):
    params = request.param
    mock_source_path = "mock_source_path"
    mock_converted_files_final_folder = "mock_converted_files_final_folder"

    mock_desired_suffix = "mock_desired_suffix"
    mock_arguments = mocker.Mock(
        desired_suffix=mock_desired_suffix,
        delete_files_flag = params.delete_files
    )

    mock_call_ffmpeg = "mock_call_ffmpeg"

    mock_factory = "mock_factory"
    mock_get_factory = mocker.Mock(return_value=mock_factory)
    mocker.patch("wmul_file_manager.ConvertFolderToMP4._ConversionFileInformation.get_factory", mock_get_factory)

    mock_list_of_files_for_conversion = "mock_list_of_files_for_conversion"
    mock_populate_list_of_files_for_conversion = mocker.Mock(return_value=mock_list_of_files_for_conversion)
    mocker.patch(
        "wmul_file_manager.ConvertFolderToMP4._populate_list_of_files_for_conversion", 
        mock_populate_list_of_files_for_conversion
    )

    mock_list_of_files_for_deletion = "mock_list_of_files_for_deletion"
    mock_convert_list_of_files = mocker.Mock(return_value = mock_list_of_files_for_deletion)
    mocker.patch("wmul_file_manager.ConvertFolderToMP4._convert_list_of_files", mock_convert_list_of_files)

    mock_delete_files = mocker.Mock()
    mocker.patch("wmul_file_manager.ConvertFolderToMP4._delete_files", mock_delete_files)

    result = _archive_folder(
        source_path=mock_source_path,
        converted_files_final_folder=mock_converted_files_final_folder,
        arguments=mock_arguments,
        call_ffmpeg=mock_call_ffmpeg
    )

    return make_namedtuple(
        "setup_archive_folder",
        params=params,
        mock_source_path=mock_source_path,
        mock_converted_files_final_folder=mock_converted_files_final_folder,
        mock_desired_suffix=mock_desired_suffix,
        mock_arguments=mock_arguments,
        mock_call_ffmpeg=mock_call_ffmpeg,
        mock_factory=mock_factory,
        mock_get_factory=mock_get_factory,
        mock_list_of_files_for_conversion=mock_list_of_files_for_conversion,
        mock_populate_list_of_files_for_conversion=mock_populate_list_of_files_for_conversion,
        mock_list_of_files_for_deletion=mock_list_of_files_for_deletion,
        mock_convert_list_of_files=mock_convert_list_of_files,
        mock_delete_files=mock_delete_files,
        result=result
    )

def test_result_is_none(setup_archive_folder):
    result = setup_archive_folder.result
    assert result is None

def test_get_factory_called_correctly(setup_archive_folder):
    mock_get_factory = setup_archive_folder.mock_get_factory
    mock_source_path = setup_archive_folder.mock_source_path
    mock_converted_files_final_folder = setup_archive_folder.mock_converted_files_final_folder

    mock_get_factory.assert_called_once_with(
        mock_source_path,
        mock_converted_files_final_folder
    )

def test_populate_list_of_files_for_conversion_called_correctly(setup_archive_folder):
    mock_populate_list_of_files_for_conversion = setup_archive_folder.mock_populate_list_of_files_for_conversion
    mock_source_path = setup_archive_folder.mock_source_path
    mock_factory = setup_archive_folder.mock_factory
    mock_desired_suffix = setup_archive_folder.mock_desired_suffix

    mock_populate_list_of_files_for_conversion.assert_called_once_with(
        mock_source_path,
        mock_factory,
        mock_desired_suffix
    )

def test_convert_list_of_files_called_correctly(setup_archive_folder):
    mock_convert_list_of_files = setup_archive_folder.mock_convert_list_of_files
    mock_call_ffmpeg = setup_archive_folder.mock_call_ffmpeg
    mock_list_of_files_for_conversion = setup_archive_folder.mock_list_of_files_for_conversion
    
    mock_convert_list_of_files.assert_called_once_with(
        mock_call_ffmpeg,
        mock_list_of_files_for_conversion
    )

def test_delete_files_called_correctly(setup_archive_folder):
    params = setup_archive_folder.params
    mock_delete_files = setup_archive_folder.mock_delete_files
    mock_list_of_files_for_deletion = setup_archive_folder.mock_list_of_files_for_deletion
    
    if params.delete_files:
        mock_delete_files.assert_called_once_with(
            mock_list_of_files_for_deletion
        )
    else:
        mock_delete_files.assert_not_called()
