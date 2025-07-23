from datetime import datetime
from pathlib import Path

def parse_stream_date(path: Path) -> datetime:
    """
    Extracts a datetime object from a stream session folder name.

    Assumes the structure: Z:/YYYY.MM.DD[.N]/category/clip.mp4
    Always returns the date from the stream folder (two levels up).
    """
    session_folder = path.parent.parent  # clip.mp4 → montages → 2025.06.20
    folder_name = session_folder.name.strip()
    date_parts = folder_name.split('.')[:3]

    if len(date_parts) != 3:
        raise ValueError(f"Invalid folder name format: {folder_name}")

    date_str = '.'.join(date_parts)
    try:
        return datetime.strptime(date_str, '%Y.%m.%d')
    except Exception as e:
        raise ValueError(f"Failed to parse '{date_str}' from '{folder_name}': {e}")
