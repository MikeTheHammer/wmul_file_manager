"""
@Author = 'Mike Stanley'

Interface to call ffmpeg from within Python. Note that the executable called need not actually be ffmpeg, it just
needs to obey the same command-line options.

============ Change Log ============
2024-May-08 = Added convert_video method for compressing video files.

2018-May-01 = Imported from Titanium_Monticello to this project.

              Change bitrate comparisons from equality to greater-than / less-than.

              E.G.
              if bitrate == 320:
                    bitrate = "320000"

              became

              if bitrate > 192:
                    bitrate = "320000"

2017-Aug-11 = Modify to use python 3.5's .run method and to capture stderr and stdout instead of dumping to
                    console.

2015-Feb-25 = Created.

============ License ============
The MIT License (MIT)

Copyright (c) 2015, 2017-2018, 2024 Michael Stanley

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
import subprocess
import wmul_logger

logger = wmul_logger.get_logger()

def call(input_file_path, output_file_path, codec, bitrate, executable_path):
    bitrate = int(bitrate)

    if codec == "mp3":
        codec = "libmp3lame"

    if bitrate > 192:
        bitrate = "320000"
    elif bitrate > 160:
        bitrate = "192000"
    elif bitrate > 96:
        bitrate = "160000"
    elif bitrate <= 96:
        bitrate = "96000"

    return subprocess.run(
        [executable_path, "-i", input_file_path, "-codec:a", codec,  "-b:a", bitrate, output_file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

def convert_video(input_file_path, output_file_path, video_codec, video_bitrate, audio_codec, audio_bitrate, threads, executable_path):
    audio_bitrate = int(audio_bitrate)
    video_bitrate = int(video_bitrate)

    if audio_codec == "mp3":
        audio_codec = "libmp3lame"

    if audio_bitrate > 192:
        audio_bitrate = "320k"
    elif audio_bitrate > 160:
        audio_bitrate = "192k"
    elif audio_bitrate > 96:
        audio_bitrate = "160k"
    elif audio_bitrate <= 96:
        audio_bitrate = "96k"

    if video_bitrate > 19:
        video_bitrate = "20000k"
    elif video_bitrate > 14: 
        video_bitrate = "15000k"
    elif video_bitrate > 9:
        video_bitrate = "10000k"
    elif video_bitrate > 4:
        video_bitrate = "5000k"
    else:
        video_bitrate = "1000k"

    subprocess_args = [
        executable_path, 
        "-i", input_file_path, 
        "-c:a", audio_codec,  
        "-b:a", audio_bitrate, 
        "-c:v", video_codec, 
        "-b:v", video_bitrate, 
        "-threads", str(threads), 
        output_file_path
    ]

    logger.info(f"subprocess_args: {subprocess_args}")

    subprocess_result = subprocess.run(
        subprocess_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    return subprocess_result.returncode