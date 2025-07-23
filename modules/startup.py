# startup.py
#
# Description:
# This module verifies the presence and accessibility of all critical assets needed for the video processing pipeline.
# If any required file is missing or unreadable, the script exits with an error message.
#
# Usage:
# Called at the beginning of main.py to ensure a clean, verified startup state.

from pathlib import Path
import sys

# These are expected to be already set correctly in config.py
from config import (
    INTRO_WIDE_PATH,
    INTRO_VERTICAL_PATH,
    OUTRO_WIDE_PATH,
    OUTRO_VERTICAL_PATH,
    FONT_PATH,
    THEME_MUSIC_PATH
)

REQUIRED_PATHS = [
    ("INTRO_WIDE_PATH", INTRO_WIDE_PATH),
    ("INTRO_VERTICAL_PATH", INTRO_VERTICAL_PATH),
    ("OUTRO_WIDE_PATH", OUTRO_WIDE_PATH),
    ("OUTRO_VERTICAL_PATH", OUTRO_VERTICAL_PATH),
    ("FONT_PATH", FONT_PATH),
    ("THEME_MUSIC_PATH", THEME_MUSIC_PATH),
]

def resolve_path(label: str, path_str: str):
    try:
        path = Path(path_str)
        if not path.is_file():
            raise FileNotFoundError(f"{label} not found at {path}")
        return path
    except Exception as e:
        print(f"❌ {label} → {e}")
        sys.exit(1)

def verify_assets():
    print("🔍 Verifying external file dependencies...")
    for label, path_str in REQUIRED_PATHS:
        resolved = resolve_path(label, path_str)
        print(f"✅ {label} → {resolved}")
