# modules/render_montages.py
#
# Entrypoint for rendering Fortnite montage clips.
# This module handles parsing the clip metadata and orchestrating the render pipeline.

from pathlib import Path
from datetime import datetime
from render_engine import render_montage_clip
from title_utils import format_overlay_text


def process_montage_clip(
    clip_path: Path,
    stream_date: datetime,
    out_path: Path,
    is_vertical: bool
):
    """
    Handles full processing of a montage clip:
    - Builds overlay title from stream date
    - Renders intro with overlay
    - Stitches intro + clip + outro
    - Saves final result to out_path
    """
    # Format multiline overlay text using stream date
    title_text = format_overlay_text(stream_date)

    # Run full montage render pipeline
    try:
        print(f"\n[TRACE] about to render:")
        print(f"  montage_path: {montage_path} → {montage_path.exists()}")
        print(f"  title_card_path: {title_card_path} → {title_card_path.exists()}")
        print(f"  output_path: {output_path}")
        render_montage_clip(
            montage_path=montage_path,
            title_card_path=title_card_path,
            output_path=output_path,
            is_vertical=is_vertical
        )
    except Exception as e:
        print(f"🔥 Exception BEFORE render_montage_clip: {type(e).__name__} → {e}")
        import traceback
        traceback.print_exc()
