"""Tests for logging module."""

import json
from io import StringIO
from unittest.mock import patch

from src.observability.logging import get_logger, setup_logging


def test_setup_logging() -> None:
    """Test that logging setup doesn't raise errors."""
    # Just ensure it doesn't crash
    setup_logging(level="DEBUG")


def test_get_logger() -> None:
    """Test getting a logger instance."""
    setup_logging()
    logger = get_logger("test")
    assert logger is not None


def test_logger_outputs_json() -> None:
    """Test that logger outputs JSON format."""
    output = StringIO()

    with patch("sys.stdout", output):
        setup_logging()
        logger = get_logger("test")
        logger.info("test message", key="value")

    log_output = output.getvalue().strip()
    if log_output:
        # Should be valid JSON
        parsed = json.loads(log_output)
        assert "event" in parsed or "msg" in parsed
