# This is where the src for the video io class will live
from moviepy import VideoFileClip
import os
from PIL import Image
# What we want to do is split multiple files into frames, combine the frames
# Then layer over the audio

INPUT_DIR = "../Inputs/"
OUTPUT_DIR = "../Outputs/"
TEMP_DIR = "../temp/"

VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".mpg", ".mpeg", ".wmv", ".flv"}

class VideoIO:

    def __init__(self):
        self.input_dir = INPUT_DIR
        self.output_dir = OUTPUT_DIR
        self.temp_dir = TEMP_DIR

    def find_video_files(self):
        """Return the paths of the video files in the input directory."""
        paths = []
        for name in sorted(os.listdir(self.input_dir)):
            path = os.path.join(self.input_dir, name)
            if os.path.isfile(path) and os.path.splitext(name)[1].lower() in VIDEO_EXTENSIONS:
                paths.append(path)
        return paths


    def get_video_frames(self): ...


class AudioIO: ...

