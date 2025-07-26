"""
metadata_utils.py

Handles metadata extraction from video clip structure and notes.json,
and manages persistent storage of finalized metadata records.

Author: Llama Chile Shop
"""

import json
import re
from pathlib import Path
from modules.config import NAS_MOUNT_ROOT

# Define where to persist finalized metadata records after upload
HISTORY_DIR = Path("Z:/LCS/Logs/processed")


def derive_session_metadata(session_dir: Path) -> dict:
    """
    Derives session-level metadata from a session directory.
    Includes shared attributes, notes.json contents, and clip metadata for all videos found.

    Args:
        session_dir (Path): Path to the session folder (e.g., 2025.07.24 or 2025.07.24.2)

    Returns:
        dict: A dictionary representing session metadata, including notes and per-clip info.
    """
    session_dir = Path(session_dir)
    session_name = session_dir.name

    # Validate session folder format: YYYY.MM.DD or YYYY.MM.DD.N
    match = re.match(r"(\d{4})\.(\d{2})\.(\d{2})(?:\.(\d+))?", session_name)
    if not match:
        raise ValueError(f"Invalid session folder format: {session_name}")

    year, month, day, session_index = match.groups()
    session_date = f"{year}-{month}-{day}"
    session_number = int(session_index) if session_index else 1

    # Attempt to load notes.json from the session root
    notes_path = session_dir / "notes.json"
    notes_data = {}
    if notes_path.exists():
        try:
            with open(notes_path, "r", encoding="utf-8") as f:
                notes_data = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to parse notes.json: {e}")

    # Extract shared fields (with fallback defaults)
    session_meta = {
        "session_date": session_date,
        "session_number": session_number,
        "highlight": notes_data.get("highlight", "Fortnite highlight moment"),
        "tags": notes_data.get("tags", []),
        "gag_name": notes_data.get("gag_name", None),
        "notes": notes_data,
        "clips": []
    }

    # Scan for all .mp4 clips within expected subdirectories
    for subfolder in ["hits", "misses", "montages", "outtakes"]:
        clip_dir = session_dir / subfolder
        if not clip_dir.exists():
            continue

        for clip_path in clip_dir.glob("*.mp4"):
            stem = clip_path.stem.lower()
            is_vertical = stem.endswith("-vert") or stem.endswith("-vertical")
            format = "vertical" if is_vertical else "wide"

            clip_meta = {
                "path": str(clip_path),
                "filename": clip_path.name,
                "stem": clip_path.stem,
                "format": format,
                "clip_type": subfolder,
                "youtube_urls": [],
                "peertube_urls": []
            }

            session_meta["clips"].append(clip_meta)

    return session_meta


def save_metadata_record(metadata: dict) -> None:
    """
    Saves a finalized metadata record to disk for future lookup or audit.

    This includes all session-level and clip-level data, plus any added URLs
    after upload to YouTube or PeerTube.

    Args:
        metadata (dict): Fully populated metadata record, typically post-upload.

    Raises:
        RuntimeError: If required fields are missing or write fails.
    """
    try:
        session_date = metadata.get("session_date")
        filename = metadata.get("filename") or metadata.get("stem")

        if not session_date or not filename:
            raise ValueError("Metadata missing required fields: session_date or filename/stem")

        # Use YYYY.MM.DD folder for archival
        dest_dir = HISTORY_DIR / session_date.replace("-", ".")
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Save as <stem>.json
        dest_file = dest_dir / f"{Path(filename).stem}.json"
        with open(dest_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        print(f"📁 Saved metadata record to: {dest_file}")

    except Exception as e:
        raise RuntimeError(f"Failed to save metadata record: {e}")
