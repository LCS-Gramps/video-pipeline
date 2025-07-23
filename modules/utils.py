# modules/utils.py
#
# General-purpose utility functions used throughout the rendering pipeline.

import re
from pathlib import Path
from datetime import datetime
from modules.config import NAS_MOUNT_ROOT, resolve_path # type: ignore

# Regex pattern to match date formats like '2025.06.20', '2025.06.20.2', etc.
DATE_PATTERN = re.compile(r"^(\d{4})\.(\d{2})\.(\d{2})(?:\.(\d{1,2}))?$")


def scan_for_new_clips(base_path: Path, subfolder: str) -> list[Path]:
    """
    Recursively scan base_path for any files under a named subfolder
    (e.g. 'montages', 'hits', etc).
    Returns a list of all video files found.
    """
    matching_clips = []

    for session_dir in base_path.iterdir():
        if session_dir.is_dir() and session_dir.name.count(".") >= 2:
            target_dir = session_dir / subfolder
            if target_dir.exists():
                for f in target_dir.glob("*.mp4"):
                    matching_clips.append(f)

    return matching_clips

def run_ffmpeg(cmd: list[str]) -> None:
    """
    Execute an ffmpeg command, logging output and raising if the command fails.
    """
    import subprocess
    from textwrap import indent

    print(f"\n🛠️  Running ffmpeg:\n{indent(' '.join(cmd), '    ')}\n")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg failed with error: {e}")
        raise
