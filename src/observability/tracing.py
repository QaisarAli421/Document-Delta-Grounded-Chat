"""Observability tracing module using contextvars."""

import contextvars
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Span:
    """Represents a trace span."""

    trace_id: str
    span_id: str
    name: str
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: datetime | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    error: Exception | None = None
    children: list["Span"] = field(default_factory=list)

    def finish(self) -> None:
        """Mark the span as finished."""
        self.end_time = datetime.utcnow()

    def set_attribute(self, key: str, value: Any) -> None:
        """Set an attribute on the span."""
        self.attributes[key] = value

    def record_error(self, error: Exception) -> None:
        """Record an error on the span."""
        self.error = error


# Context variable for current span
_current_span: contextvars.ContextVar[Span | None] = contextvars.ContextVar(
    "current_span", default=None
)


def get_current_span() -> Span | None:
    """Get the current span from context."""
    return _current_span.get()


def generate_id() -> str:
    """Generate a unique ID for traces/spans."""
    return str(uuid.uuid4())


class Tracer:
    """Context manager-based tracer."""

    def __init__(self, service_name: str = "document-delta"):
        self.service_name = service_name
        self.spans: list[Span] = []

    def start_span(self, name: str, parent: Span | None = None) -> Span:
        """Start a new span."""
        trace_id = parent.trace_id if parent else generate_id()
        span = Span(
            trace_id=trace_id,
            span_id=generate_id(),
            name=name,
        )
        if parent:
            parent.children.append(span)
        self.spans.append(span)
        return span

    def __enter__(self) -> "Tracer":
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager."""
        pass


class trace:
    """Decorator and context manager for tracing."""

    def __init__(self, name: str):
        self.name = name
        self.span: Span | None = None
        self.token: contextvars.Token | None = None

    def __enter__(self) -> Span:
        """Enter the trace context."""
        parent = get_current_span()
        tracer = Tracer()
        self.span = tracer.start_span(self.name, parent)
        self.token = _current_span.set(self.span)
        return self.span

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the trace context."""
        if self.span:
            if exc_val:
                self.span.record_error(exc_val)
            self.span.finish()
        if self.token:
            _current_span.reset(self.token)

    async def __aenter__(self) -> Span:
        """Async enter."""
        return self.__enter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async exit."""
        self.__exit__(exc_type, exc_val, exc_tb)
