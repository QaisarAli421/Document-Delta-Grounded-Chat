"""Tests for configuration."""

import os
from unittest.mock import patch

from src.config import Settings


def test_settings_default_values() -> None:
    """Test that settings have correct default values."""
    with patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        assert settings.model_name == "llama-3.1-70b"
        assert settings.match_threshold == 0.5
        assert settings.geo_weight == 0.4
        assert settings.txt_weight == 0.3
        assert settings.kind_weight == 0.2
        assert settings.attr_weight == 0.1


def test_settings_from_env() -> None:
    """Test that settings can be loaded from environment."""
    with patch.dict(
        os.environ,
        {
            "GROQ_API_KEY": "test-key",
            "MODEL_NAME": "custom-model",
            "MATCH_THRESHOLD": "0.8",
        },
    ):
        settings = Settings()
        assert settings.groq_api_key == "test-key"
        assert settings.model_name == "custom-model"
        assert settings.match_threshold == 0.8
