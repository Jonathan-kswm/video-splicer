# This is where the src for the video io class will live
from moviepy import VideoFileClip
import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image
import cv2

# Prefer the ffmpeg binary that ships with imageio-ffmpeg (a moviepy
# dependency) so frame extraction does not depend on a system install.
try:
    import imageio_ffmpeg
    FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_EXE = "ffmpeg"
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

        Frames are extracted by shelling out to ffmpeg rather than reading
        with OpenCV: OpenCV's frame-by-frame decode can stop early on some
        builds/codecs (returning fewer frames than the video contains),
        whereas ffmpeg decodes every frame deterministically.
        """
        video_paths = self.find_video_files()

        # Start from a clean temp directory so stale frames can't corrupt
        # the sequence or leak into the splice.
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        frame_paths = []
        for video_path in video_paths:
            # -start_number continues the shared sequence; -fps_mode passthrough
            # keeps every source frame (no dup/drop to hit a target rate).
            command = [
                FFMPEG_EXE, "-nostdin", "-loglevel", "error",
                "-i", str(video_path),
                "-start_number", str(len(frame_paths)),
                "-fps_mode", "passthrough",
                str(self.temp_dir / f"frame_%06d.{image_format}"),
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                raise IOError(
                    f"ffmpeg failed on {video_path}:\n{result.stderr.strip()}"
                )

            # Newly written frames are everything not already accounted for.
            written = sorted(self.temp_dir.glob(f"frame_*.{image_format}"))
            frame_paths.extend(str(p) for p in written[len(frame_paths):])

        self.frames = frame_paths
        return self.frames



    def load_video(self):... # this will run the above


    def create_video(self):... # This will add the frames together

class AudioIO: ...

