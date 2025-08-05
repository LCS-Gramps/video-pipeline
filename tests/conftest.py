# tests/conftest.py
"""
Shared pytest fixtures and constants for testing the LCS video pipeline.
"""

import pytest
from pathlib import Path

@pytest.fixture(scope="session")
def test_session_path() -> Path:
    """
    Fixture providing the fixed test session directory.

    NOTE: This directory must exist and be preserved. It contains test clips
    and notes.json used by multiple tests.

    Returns:
        Path: Absolute path to test session folder.
    """
    return Path("Z:/LCS/Videos/eklipse/2025.07.25.9")
