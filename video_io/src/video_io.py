# This is where the src for the video io class will live
from moviepy import VideoFileClip
import os
import shutil
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
        self.frames = []

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
        """Split every input video into frames and write them, flat, into the
        temp directory.

        Videos are processed in the order find_video_files() returns them
        (alphabetical by filename), and every frame from every video shares
        one continuous sequence:

            temp/frame_000000.png   <- first frame of the first video
            temp/frame_000001.png
            ...
            temp/frame_000160.png   <- last frame of the first video
            temp/frame_000161.png   <- first frame of the second video
            ...

        The temp directory is wiped first so the sequence is always clean.
        Returns (and caches on self.frames) the ordered list of frame paths.
        """
        video_paths = self.find_video_files()

        # Start from a clean temp directory so stale frames can't corrupt
        # the sequence or leak into the splice.
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        frame_paths = []
        index = 0
        for video_path in video_paths:
            capture = cv2.VideoCapture(str(video_path))
            if not capture.isOpened():
                capture.release()
                raise IOError(f"Could not open video: {video_path}")

            while True:
                ok, frame = capture.read()
                if not ok:
                    break
                frame_path = self.temp_dir / f"frame_{index:06d}.{image_format}"
                cv2.imwrite(str(frame_path), frame)
                frame_paths.append(str(frame_path))
                index += 1

            capture.release()

        self.frames = frame_paths
        return self.frames



    def load_video(self):... # this will run the above


    def create_video(self):... # This will add the frames together

class AudioIO: ...

