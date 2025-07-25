"""
upload_montage_youtube.py

Standalone entry point to upload a rendered Fortnite montage video to YouTube.
Assumes that the input video is a montage and therefore does NOT rely on a notes.* file.

Handles:
- Validating input parameters (video path)
- Deriving vertical format from filename
- Generating dynamic description via OpenAI
- Uploading to YouTube with appropriate metadata
- Flagging video as private if DEBUG is enabled

Author: Llama Chile Shop
Created: 2025-07-22
"""

import os
import sys
from pathlib import Path

from modules.config import DEBUG
from modules.yt_poster import upload_video
from modules.description_utils import generate_montage_description
from authorize_youtube import get_authenticated_service


def main():
    """
    Entry point to handle YouTube upload of montage video.
    Usage:
        python upload_montage_youtube.py <video_path>
    """

    if len(sys.argv) != 2:
        print("Usage: python upload_montage_youtube.py <path_to_rendered_video>")
        sys.exit(1)

    # Extract stream date from parent directory (Z:\2025.06.20)
    video_path = Path(sys.argv[1])
    stream_date = video_path.parents[1].name  # '2025.06.20'

    if not os.path.isfile(video_path):
        print(f"[ERROR] File not found: {video_path}")
        sys.exit(1)

    video_name = os.path.basename(video_path)
    is_vertical = "-vert" in video_path.stem or "-vertical" in video_path.stem

    # Generate a dynamic, humorous montage description
    description = generate_montage_description()

    # Upload the video to YouTube
    upload_video(
        file_path=video_path,
        is_vertical=is_vertical,
        stream_date=stream_date,
        description=description,
        private=DEBUG
    )

if __name__ == "__main__":
    main()
