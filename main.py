import sys
import subprocess
from pathlib import Path
from datetime import datetime

from modules.config import (
    INTRO_WIDE_PATH,
    INTRO_VERTICAL_PATH,
    OUTRO_WIDE_PATH,
    OUTRO_VERTICAL_PATH,
    THEME_MUSIC_PATH,
    FONT_PATH,
    NAS_MOUNT_ROOT
)
from modules.date_utils import parse_stream_date
from modules.title_utils import (
    generate_title_overlay,
    format_overlay_text,
    generate_montage_title,
    generate_output_filename,
    extract_session_metadata
)
from modules.render_engine import render_montage_clip

def scan_for_montage_clips(nas_root: Path) -> list[Path]:
    """Scan the NAS for montage clips to process."""
    montage_clips = []
    for session_dir in nas_root.iterdir():
        if not session_dir.is_dir():
            continue
        montage_dir = session_dir / "montages"
        if not montage_dir.exists():
            continue
        for file in montage_dir.glob("*.mp4"):
            if file.name.lower() != "title_card.mp4":
                montage_clips.append(file)
    return montage_clips

def process_clip(clip_path: Path):
    is_vertical = clip_path.stem.endswith(("-vert", "-vertical"))
    stream_date = parse_stream_date(clip_path)

    # ⏺️ Compose overlay text for title overlay
    overlay_text = format_overlay_text(
        title="Fortnite Highlights",
        subtitle="with Gramps",
        date_str=stream_date.strftime("%B %d, %Y"),
    )

    # 🪪 Create session metadata
    session_name = extract_session_metadata(clip_path)

    # 🖼️ Generate title overlay baked into intro (2s fade before end)
    output_name = generate_output_filename(clip_path)
    output_path = clip_path.parents[1] / "rendered" / output_name
    temp_intro_path = output_path.parent / "intro_with_title.mp4"

    stock_intro = INTRO_VERTICAL_PATH if is_vertical else INTRO_WIDE_PATH
    print(f"[DEBUG] Generating intro with title overlay at: {temp_intro_path}")
    generate_title_overlay(
        intro_path=stock_intro,
        overlay_text=overlay_text,
        output_path=temp_intro_path,
        font_path=FONT_PATH,
        is_vertical=is_vertical
    )

    # 🎞️ Final outro (unchanged)
    outro_path = OUTRO_VERTICAL_PATH if is_vertical else OUTRO_WIDE_PATH

    # 🎬 Render final video
    render_montage_clip(
        title_card_path=temp_intro_path,
        montage_path=clip_path,
        output_path=output_path,
        intro_path=temp_intro_path,  # semantic placeholder
        outro_path=outro_path,
        music_path=THEME_MUSIC_PATH,
        is_vertical=is_vertical
    )

    # 🧹 Cleanup
    if temp_intro_path.exists():
        try:
            temp_intro_path.unlink()
        except Exception as e:
            print(f"[WARN] Couldn't delete temp intro file: {e}")

def main():
    print(f"🐛 DEBUG: main.py loaded from: {__file__}")
    print(f"⏱️ LAUNCH TIMESTAMP: {datetime.now().isoformat()}")
    print(f"🔧 modules_path = {Path(__file__).parent / 'modules'}")
    print(f"🔍 Scanning NAS for montage clips under: {NAS_MOUNT_ROOT}")

    montage_clips = scan_for_montage_clips(NAS_MOUNT_ROOT)
    if not montage_clips:
        print("📭 No montage clips found.")
        return

    for clip_path in montage_clips:
        print(f"📦 Sending clip to processor: {clip_path} (type: {type(clip_path)})")
        try:
            process_clip(clip_path)
        except Exception as e:
            print(f"❌ Error processing {clip_path} (is_vertical={clip_path.stem.endswith(('-vert', '-vertical'))}) → {e}")

if __name__ == "__main__":
    main()
