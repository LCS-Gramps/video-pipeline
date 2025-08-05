# tests/test_metadata_utils.py
"""
Unit tests for metadata parsing and archiving functions.
"""

from modules.metadata_utils import derive_session_metadata, save_metadata_record
from pathlib import Path
import json


def test_derive_session_metadata_structure(test_session_path):
    """
    Validates that metadata is parsed correctly and includes expected keys.
    """
    metadata = derive_session_metadata(test_session_path)

    assert "session_date" in metadata
    assert "clips" in metadata
    assert isinstance(metadata["clips"], list)
    assert len(metadata["clips"]) > 0, "Expected at least one clip in metadata"

    for clip in metadata["clips"]:
        assert "stem" in clip
        assert "highlight" in clip or "notes" in clip
        assert clip["format"] in ("wide", "vertical")


def test_save_metadata_record_creates_file(tmp_path):
    """
    Ensures metadata is saved to a properly named JSON file.
    """
    fake_record = {
        "session_date": "2025-07-25",
        "stem": "test-clip",
        "youtube_urls": ["https://youtu.be/test123"],
        "peertube_urls": [],
    }

    # Override history dir to a temp path
    from modules import metadata_utils
    metadata_utils.HISTORY_DIR = tmp_path

    save_metadata_record(fake_record)

    expected_dir = tmp_path / "2025.07.25"
    expected_file = expected_dir / "test-clip.json"

    assert expected_file.exists(), f"Expected {expected_file} to be created"

    with expected_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["youtube_urls"][0] == "https://youtu.be/test123"
