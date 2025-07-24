import os
import logging
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# debugging flag
DEBUG = os.getenv("DEBUG_MODE", "false").lower() == "true"


# 🔧 Project Root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
NAS_MOUNT_ROOT = Path("Z:/")

# 📁 Assets
ASSETS_DIR = PROJECT_ROOT / "assets"

# 🎵 Theme Music
THEME_MUSIC_PATH = ASSETS_DIR / "The_Llama_Song.mp3"

# Font
FONT_PATH = ASSETS_DIR / "BurbankBigCondensed-Black.otf"

# Brand colors
FONT_COLOR = "#f7338f"
SHADING_COLOR = "#10abba"
SHADOW_COLOR = "#1c0c38"
BRANDING_COLORS = {
    "font": FONT_COLOR,
    "shade": SHADING_COLOR,
    "shadow": SHADOW_COLOR
}

# Rendering quality settings (used by render_engine.py)
RENDER_PRESET = "slow"  # or "medium" for faster encode
RENDER_CRF = 18         # lower = better quality, 18–23 is typical

TITLE_TEMPLATE = {
    "main": "Fortnite Highlights",
    "sub": "from livestream",
}

# 🎬 Static Intros and Outros prevetted to 1080p60
INTRO_WIDE_PATH = NAS_MOUNT_ROOT / "assets" / "intro-wide-60fps.mp4"
OUTRO_WIDE_PATH = NAS_MOUNT_ROOT / "assets" / "outro-wide-60fps.mp4"
INTRO_VERTICAL_PATH = NAS_MOUNT_ROOT / "assets" / "intro-vertical-60fps.mp4"
OUTRO_VERTICAL_PATH = NAS_MOUNT_ROOT / "assets" / "outro-vertical-60fps.mp4"

# 🔨 Optional: FFmpeg executable path
FFMPEG_PATH = Path("C:/ffmpeg/bin/ffmpeg.exe")

# 🧠 OpenAI API Key
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# 📂 Path resolver (Z: → UNC fallback), now exception wrapped
def resolve_path(path_obj: Path) -> str:
    """
    Safely resolves a path for use in subprocess calls.
    Falls back from Z:/ to UNC if necessary and logs issues.
    """
    try:
        if path_obj.exists():
            return str(path_obj)
        # Try UNC fallback
        fallback = Path(str(path_obj).replace("Z:/", "//chong/LCS/Videos/eklipse/"))
        if fallback.exists():
            return str(fallback)
        raise FileNotFoundError(f"❌ Path not found: {path_obj} or fallback {fallback}")
    except Exception as e:
        logging.error(f"[resolve_path] Failed to resolve: {path_obj} → {e}")
        raise
