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
from wmul_file_manager.ConvertFolderToMP4 import _check_and_archive_folder
from wmul_test_utils import generate_true_false_matrix_from_list_of_strings, make_namedtuple


check_and_archive_folder_params, check_and_archive_folder_ids = generate_true_false_matrix_from_list_of_strings(
    "check_and_archive_folder_options",
    [
        "separate_folder",
        "folder_exists"
    ]
)

@pytest.fixture(scope="function", params=check_and_archive_folder_params, ids=check_and_archive_folder_ids)
def setup_check_and_archive_folder(fs, mocker, request, caplog):
    params = request.param

    mock_arguments = mocker.Mock(separate_folder_flag=params.separate_folder)

    source_path = Path("/temp/folder_1")

    if params.folder_exists:
        fs.create_dir(source_path)

    mock_archive_folder = mocker.Mock()
    mocker.patch("wmul_file_manager.ConvertFolderToMP4._archive_folder", mock_archive_folder)

    mock_call_ffmpeg = "mock_call_ffmpeg"

    if params.separate_folder:
        expected_converted_files_folder = Path("/temp/folder_1_mp4")
    else:
        expected_converted_files_folder = source_path

    result = _check_and_archive_folder(arguments=mock_arguments, call_ffmpeg=mock_call_ffmpeg, source_path=source_path)

    return make_namedtuple(
        "setup_check_and_archive_folder",
        params=params,
        mock_arguments=mock_arguments,
        source_path=source_path,
        mock_archive_folder=mock_archive_folder,
        mock_call_ffmpeg=mock_call_ffmpeg,
        expected_converted_files_folder=expected_converted_files_folder,
        result=result,
        logging_output=caplog.text
    )

def test_archive_folder_called_correctly(setup_check_and_archive_folder):
    params = setup_check_and_archive_folder.params
    mock_archive_folder = setup_check_and_archive_folder.mock_archive_folder
    if params.folder_exists:
        mock_archive_folder.assert_called_once_with(
            setup_check_and_archive_folder.source_path,
            setup_check_and_archive_folder.expected_converted_files_folder,
            setup_check_and_archive_folder.mock_arguments,
            setup_check_and_archive_folder.mock_call_ffmpeg
        )
    else:
        mock_archive_folder.assert_not_called()

def test_logging_correct(setup_check_and_archive_folder):
    params = setup_check_and_archive_folder.params
    logging_output = setup_check_and_archive_folder.logging_output

    assert "Working on: \\temp\\folder_1" in logging_output

    if params.folder_exists:
        assert "Folder does not exist. \\temp\\folder_1" not in logging_output
    else:
        assert "Folder does not exist. \\temp\\folder_1" in logging_output

def test_result_is_none(setup_check_and_archive_folder):
    result = setup_check_and_archive_folder.result
    assert result is None
