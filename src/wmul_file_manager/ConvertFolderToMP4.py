"""
@Author = 'Mike Stanley'

Script to archive a directory or set of directories into mp4 format. It uses ffmpeg to do the actual work.

============ Change Log ============
2024-May-03 = Created. This is a single-threaded re-work of ConvertFolderToMP3.

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
from collections import namedtuple
from enum import Enum
from functools import partial
import time

from wmul_file_manager.utilities import ffmpeg
from wmul_file_manager.utilities.FileNamePrinter import object_cleaner

import wmul_logger

logger = wmul_logger.get_logger()


class _ConversionFileInformationType(Enum):
    Raw_File = 0
    Converted_File = 1

class _ConversionFileInformation:

    def __init__(self, file_info_type, source_file_path, source_root_path, converted_files_final_folder):
        self.file_info_type = file_info_type
        self.original_file_name = source_file_path
        self.source_path = source_file_path

        relative_to_root = source_file_path.relative_to(source_root_path).parent
        final_filename = source_file_path.stem + ".mp4"
        self.destination_path = converted_files_final_folder / relative_to_root / final_filename

        self._create_all_needed_parents()

    def __str__(self):
        return f"_ConversionFileInformation:\n{str(self.file_info_type)}\n{str(self.original_file_name)}"

    def _create_all_needed_parents(self):
        _ConversionFileInformation._create_parents(self.destination_path)

    def converted(self):
        self.file_info_type = _ConversionFileInformationType.Converted_File

    @staticmethod
    def _create_parents(file_path):
        file_parent = file_path.parent
        file_parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_factory(cls, root_path, converted_files_final_folder):
        def inner(file_info_type, source_file_path):
            return cls(file_info_type, source_file_path, root_path, converted_files_final_folder)
        return inner


def archive_list_of_folders(arguments, call_ffmpeg):
    logger.debug(f"With {locals()}")
    for source_path in arguments.source_paths:
        _check_and_archive_folder(arguments, call_ffmpeg, source_path)

def _check_and_archive_folder(arguments, call_ffmpeg, source_path):
    logger.info(f"Working on: {object_cleaner(source_path)}")
    if source_path.exists():
        if arguments.separate_folder_flag:
            converted_files_folder = source_path.parent / (source_path.name + "_mp4")
        else:
            converted_files_folder = source_path
        _archive_folder(source_path, converted_files_folder, arguments, call_ffmpeg)
    else:
        logger.warning(f"Folder does not exist. {object_cleaner(source_path)}")

def _archive_folder(source_path, converted_files_final_folder, arguments, call_ffmpeg):
    logger.debug(f"With {locals()}")
    file_info_factory = _ConversionFileInformation.get_factory(
        source_path,
        converted_files_final_folder
    )

    list_of_files_for_conversion = _populate_list_of_files_for_conversion(
        source_path, 
        file_info_factory, 
        arguments.desired_suffix
    )

    list_of_files_for_deletion = _convert_list_of_files(call_ffmpeg, list_of_files_for_conversion)

    if arguments.delete_files_flag:
        logger.info("Delete files true.")
        _delete_files(list_of_files_for_deletion)

def _populate_list_of_files_for_conversion(source_path, file_info_factory, desired_suffix):
    list_of_files_for_conversion = []
    logger.debug(f"With {locals()}")
    for file_item in source_path.iterdir():
        logger.debug(f"Working on {object_cleaner(file_item)}")
        if file_item.is_file():
            logger.debug("Is File.")
            if not file_item.suffix.casefold() == desired_suffix.casefold():
                logger.debug(f"Not the desired suffix. {file_item.suffix}\t{desired_suffix}")
            else:
                this_file = file_info_factory(_ConversionFileInformationType.Raw_File, file_item)
                logger.debug("Adding file to copy queue.")
                list_of_files_for_conversion.append(this_file)
        else:
            logger.debug("Is dir.")
            sublist_of_files_for_conversion = _populate_list_of_files_for_conversion(
                file_item,
                file_info_factory,
                desired_suffix
            )
            list_of_files_for_conversion.extend(sublist_of_files_for_conversion)
    return list_of_files_for_conversion

def _convert_list_of_files(call_ffmpeg, list_of_files_for_conversion):
    list_of_files_for_deletion = []
    for file_to_be_converted in list_of_files_for_conversion:
        return_code = call_ffmpeg(
            input_file_path=str(file_to_be_converted.source_path),
            output_file_path=str(file_to_be_converted.destination_path)
        )
        if return_code == 0:
            logger.debug("Return code good.")
            file_to_be_converted.converted()
            list_of_files_for_deletion.append(file_to_be_converted)
        else:
            logger.warning(f"Return code bad: {return_code} \t {object_cleaner(file_to_be_converted)}")
    return list_of_files_for_deletion

def _delete_files(list_of_files_for_deletion):
    for file_to_be_deleted in list_of_files_for_deletion:
        if file_to_be_deleted.file_info_type == _ConversionFileInformationType.Converted_File:
            logger.debug(f"Deleting {object_cleaner(file_to_be_deleted)}")
            original_file_name = file_to_be_deleted.original_file_name
            try:
                original_file_name.unlink()
            except PermissionError as pe:
                # Wait 5 seconds, retry once
                time.sleep(5)
                try:
                    original_file_name.unlink()
                except PermissionError as pe:
                    logger.error(f"Permission error on {original_file_name}")
        else:
            logger.warning(f"File in deletion queue, but not converted. {object_cleaner(file_to_be_deleted)}")

ConvertFolderToMP4Arguments = namedtuple(
    "ConvertFolderToMP4Arguments",
    [
        "source_paths",
        "desired_suffix",
        "audio_codec",
        "audio_bitrate",
        "video_codec",
        "video_bitrate",
        "threads",
        "ffmpeg_executable",
        "separate_folder_flag",
        "delete_files_flag",
    ]
)

def run_script(arguments):
    logger.debug(f"Starting with {arguments}")
    #arguments.desired_suffix = arguments.desired_suffix.casefold()
    call_ffmpeg = partial(
        ffmpeg.convert_video,
        video_codec=arguments.video_codec,
        video_bitrate=arguments.video_bitrate,
        audio_codec=arguments.audio_codec, 
        audio_bitrate=arguments.audio_bitrate,
        threads=arguments.threads,
        executable_path=arguments.ffmpeg_executable
    )
    archive_list_of_folders(arguments, call_ffmpeg)
