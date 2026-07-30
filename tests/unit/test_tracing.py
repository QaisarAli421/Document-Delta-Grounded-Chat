"""Tests for tracing module."""

from src.observability.tracing import (
    Span,
    Tracer,
    generate_id,
    get_current_span,
    trace,
)


def test_span_creation() -> None:
    """Test span creation and attributes."""
    span = Span(trace_id="test-trace", span_id="test-span", name="test-operation")
    assert span.trace_id == "test-trace"
    assert span.span_id == "test-span"
    assert span.name == "test-operation"
    assert span.end_time is None


def test_span_finish() -> None:
    """Test finishing a span."""
    span = Span(trace_id="test-trace", span_id="test-span", name="test-operation")
    span.finish()
    assert span.end_time is not None


def test_span_set_attribute() -> None:
    """Test setting attributes on a span."""
    span = Span(trace_id="test-trace", span_id="test-span", name="test-operation")
    span.set_attribute("key", "value")
    assert span.attributes["key"] == "value"


def test_span_record_error() -> None:
    """Test recording an error on a span."""
    span = Span(trace_id="test-trace", span_id="test-span", name="test-operation")
    error = ValueError("test error")
    span.record_error(error)
    assert span.error is error


def test_generate_id() -> None:
    """Test ID generation produces unique IDs."""
    id1 = generate_id()
    id2 = generate_id()
    assert id1 != id2
    assert len(id1) > 0


def test_tracer_start_span() -> None:
    """Test tracer can start spans."""
    tracer = Tracer()
    span = tracer.start_span("test-operation")
    assert span.name == "test-operation"
    assert span in tracer.spans


def test_tracer_parent_child() -> None:
    """Test tracer creates parent-child relationships."""
    tracer = Tracer()
    parent = tracer.start_span("parent")
    child = tracer.start_span("child", parent=parent)
    assert child in parent.children
    assert child.trace_id == parent.trace_id


def test_trace_context_manager() -> None:
    """Test trace context manager."""
    with trace("test-operation") as span:
        assert span.name == "test-operation"
        assert get_current_span() is span
    assert span.end_time is not None
    assert get_current_span() is None


def test_trace_context_manager_with_error() -> None:
    """Test trace context manager records errors."""
    try:
        with trace("test-operation") as span:
            raise ValueError("test error")
    except ValueError:
        pass
    assert span.error is not None
    assert span.end_time is not None


def test_get_current_span_outside_context() -> None:
    """Test get_current_span returns None outside trace context."""
    assert get_current_span() is None
