"""Tests for adapter registry."""

from pathlib import Path
from typing import Any

import pytest

from src.ingest.base import AdapterRegistry, FormatDetector


class MockAdapter:
    """Mock adapter for testing."""

    def __init__(self, formats: list[str]) -> None:
        self._formats = formats

    @property
    def supported_formats(self) -> list[str]:
        return self._formats

    def ingest(self, path: Path) -> Any:
        return {"pid": "mock", "format": self._formats[0]}


def test_adapter_registry_register() -> None:
    """Test registering an adapter."""
    registry = AdapterRegistry()
    adapter = MockAdapter(["pdf"])
    registry.register(adapter)
    assert registry.get_adapter("pdf") is adapter


def test_adapter_registry_get_unknown() -> None:
    """Test getting unknown adapter returns None."""
    registry = AdapterRegistry()
    assert registry.get_adapter("unknown") is None


def test_adapter_registry_detect_format() -> None:
    """Test format detection from path."""
    registry = AdapterRegistry()
    path = Path("test.pdf")
    assert registry.detect_format(path) == "pdf"


def test_adapter_registry_ingest() -> None:
    """Test ingesting with registry."""
    registry = AdapterRegistry()
    adapter = MockAdapter(["pdf"])
    registry.register(adapter)

    # Create a temp file
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        path = Path(f.name)

    result = registry.ingest(path)
    assert result["pid"] == "mock"

    # Cleanup
    path.unlink()


def test_adapter_registry_ingest_no_adapter() -> None:
    """Test ingesting without registered adapter raises error."""
    registry = AdapterRegistry()

    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as f:
        path = Path(f.name)

    with pytest.raises(ValueError):
        registry.ingest(path)

    path.unlink()


def test_format_detector_by_extension() -> None:
    """Test format detection by extension."""
    assert FormatDetector.by_extension(Path("test.pdf")) == "pdf"
    assert FormatDetector.by_extension(Path("test.dwg")) == "dwg"
    assert FormatDetector.by_extension(Path("test")) is None


def test_format_detector_generate_pid() -> None:
    """Test PID generation."""
    path = Path("/some/path/document.pdf")
    pid = FormatDetector.generate_pid(path)
    assert pid.startswith("doc_")
    assert len(pid) == 20  # doc_ + 16 hex chars
