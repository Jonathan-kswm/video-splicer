# This is where the src for the video io class will live
from moviepy import VideoFileClip
import os
from pathlib import Path
from PIL import Image
import cv2
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
        self.frames = {}

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

    def get_video_frames(self, image_format="png"):
        """Split every input video into frames and write them to the temp
        directory.

        Each video gets its own sub-folder under temp/, e.g.

            temp/<video name>/frame_00000.png
            temp/<video name>/frame_00001.png
            ...

        Returns (and caches on self.frames) a dict mapping each video's
        name to the ordered list of frame file paths written for it.
        """
        video_paths = self.find_video_files()

        self.temp_dir.mkdir(parents=True, exist_ok=True)

        frames = {}
        for video_path in video_paths:
            video_path = Path(video_path)
            frame_dir = self.temp_dir / video_path.stem
            frame_dir.mkdir(parents=True, exist_ok=True)

            capture = cv2.VideoCapture(str(video_path))
            if not capture.isOpened():
                capture.release()
                raise IOError(f"Could not open video: {video_path}")

            frame_paths = []
            index = 0
            while True:
                ok, frame = capture.read()
                if not ok:
                    break
                frame_path = frame_dir / f"frame_{index:05d}.{image_format}"
                cv2.imwrite(str(frame_path), frame)
                frame_paths.append(str(frame_path))
                index += 1

            capture.release()
            frames[video_path.stem] = frame_paths

        self.frames = frames
        return self.frames



    def load_video(self):... # this will run the above


    def create_video(self):... # This will add the frames together

class AudioIO: ...

