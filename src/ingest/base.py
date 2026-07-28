"""Base module for document ingestion adapters."""

from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Protocol


class CanonicalDocument(Protocol):
    """Protocol for canonical document structure."""

    pid: str
    format: str
    revision: str
    page_count: int
    pages: list[Any]
    metadata: dict[str, Any]
    ingestion_trace_id: str


class FormatAdapter(Protocol):
    """Protocol for format-specific adapters."""

    def ingest(self, path: Path) -> CanonicalDocument:
        """Ingest a document and return canonical representation."""
        ...

    @property
    def supported_formats(self) -> list[str]:
        """Return list of supported file extensions."""
        ...


class AdapterRegistry:
    """Registry for format adapters."""

    def __init__(self) -> None:
        self._adapters: dict[str, FormatAdapter] = {}

    def register(self, adapter: FormatAdapter) -> None:
        """Register an adapter for its supported formats."""
        for fmt in adapter.supported_formats:
            self._adapters[fmt] = adapter

    def get_adapter(self, format_hint: str) -> FormatAdapter | None:
        """Get adapter for a given format."""
        return self._adapters.get(format_hint.lower())

    def detect_format(self, path: Path) -> str | None:
        """Detect format from file extension."""
        suffix = path.suffix.lower()
        if suffix:
            return suffix[1:]  # Remove leading dot
        return None

    def ingest(self, path: Path) -> CanonicalDocument:
        """Ingest a document using the appropriate adapter."""
        format_hint = self.detect_format(path)
        if not format_hint:
            raise ValueError(f"Cannot detect format for {path}")

        adapter = self.get_adapter(format_hint)
        if not adapter:
            raise ValueError(f"No adapter registered for format: {format_hint}")

        return adapter.ingest(path)


class FormatDetector:
    """Utility for detecting document formats."""

    @staticmethod
    def by_extension(path: Path) -> str | None:
        """Detect format by file extension."""
        suffix = path.suffix.lower()
        if suffix:
            return suffix[1:]
        return None

    @staticmethod
    def by_magic_bytes(path: Path) -> str | None:
        """Detect format by reading magic bytes."""
        try:
            with open(path, "rb") as f:
                header = f.read(16)

            # PDF magic bytes
            if header.startswith(b"%PDF"):
                return "pdf"

            # DWG magic bytes (simplified)
            if header[:4] in [b"AC10", b"MC0."]:
                return "dwg"

            return None
        except Exception:
            return None

    @staticmethod
    def generate_pid(path: Path) -> str:
        """Generate a unique document ID from path."""
        content_hash = hashlib.sha256(str(path.resolve()).encode()).hexdigest()[:16]
        return f"doc_{content_hash}"
