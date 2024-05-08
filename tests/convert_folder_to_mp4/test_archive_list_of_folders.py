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
from pathlib import Path
from wmul_file_manager.ConvertFolderToMP4 import archive_list_of_folders
from wmul_test_utils import assert_has_only_these_calls

def test_archive_list_of_folders__single_folder(fs, mocker):
    folder_1 = Path("/temp/folder1")
    mock_source_paths = [folder_1]
    mock_arguments = mocker.Mock(source_paths=mock_source_paths)
    mock_call_ffmpeg = "mock_call_ffmpeg"

    mock_check_and_archive_folder = mocker.Mock()
    mocker.patch("wmul_file_manager.ConvertFolderToMP4._check_and_archive_folder", mock_check_and_archive_folder)

    result = archive_list_of_folders(
        arguments=mock_arguments,
        call_ffmpeg=mock_call_ffmpeg
    )

    assert result is None
    mock_check_and_archive_folder.assert_called_once_with(mock_arguments, mock_call_ffmpeg, folder_1)


def test_archive_list_of_folders__two_folders(fs, mocker):
    folder_1 = Path("/temp/folder1")
    folder_2 = Path("/temp/folder2")
    mock_source_paths = [folder_1, folder_2]
    mock_arguments = mocker.Mock(source_paths=mock_source_paths)
    mock_call_ffmpeg = "mock_call_ffmpeg"

    mock_check_and_archive_folder = mocker.Mock()
    mocker.patch("wmul_file_manager.ConvertFolderToMP4._check_and_archive_folder", mock_check_and_archive_folder)

    result = archive_list_of_folders(
        arguments=mock_arguments,
        call_ffmpeg=mock_call_ffmpeg
    )

    expected_calls = [
        mocker.call(mock_arguments, mock_call_ffmpeg, folder_1),
        mocker.call(mock_arguments, mock_call_ffmpeg, folder_2),
    ]

    assert result is None
    assert_has_only_these_calls(mock_check_and_archive_folder, expected_calls)
