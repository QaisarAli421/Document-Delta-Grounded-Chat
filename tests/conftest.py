"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path


@pytest.fixture
def sample_data_dir() -> Path:
    """Return path to sample data directory."""
    return Path(__file__).parent.parent / "data" / "samples"


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Return a temporary directory."""
    return tmp_path
