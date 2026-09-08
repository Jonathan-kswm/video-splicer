# This is where the src for the video io class will live
from moviepy import VideoFileClip
import os
from pathlib import Path
from PIL import Image
# What we want to do is split multiple files into frames, combine the frames
# Then layer over the audio

# Anchor all paths to the project root (the parent of src/) so they work
# no matter which directory the code is run from.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_DIR = PROJECT_ROOT / "Inputs"
OUTPUT_DIR = PROJECT_ROOT / "Outputs"
TEMP_DIR = PROJECT_ROOT / "temp"

VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".mpg", ".mpeg", ".wmv", ".flv"}

class VideoIO:

    def __init__(self):
        self.input_dir = INPUT_DIR
        self.output_dir = OUTPUT_DIR
        self.temp_dir = TEMP_DIR
        self.paths = []

    def find_video_files(self, refresh=False):
        """Scan the input directory for video files, cache the result on
        self.paths, and return it.

        The directory is only scanned once; later calls return the cached
        list. Pass refresh=True to force a re-scan.
        """
        if self.paths and not refresh:
            return self.paths

        paths = []
        for path in sorted(self.input_dir.iterdir()):
            if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS:
                paths.append(str(path))

        self.paths = paths
        return self.paths



    def get_video_frames(self): ...


class AudioIO: ...

