"""Canonical document model definitions."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CanonicalDocument:
    """Canonical representation of a document."""

    pid: str
    format: str
    revision: str
    page_count: int
    pages: list[Any] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    ingestion_trace_id: str = ""
