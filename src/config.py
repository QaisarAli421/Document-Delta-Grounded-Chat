"""Configuration management using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # LLM Configuration
    groq_api_key: str = ""
    model_name: str = "llama-3.1-70b"
    llm_temperature: float = 0.1
    llm_timeout: int = 30

    # Alignment thresholds
    match_threshold: float = 0.5
    geo_weight: float = 0.4
    txt_weight: float = 0.3
    kind_weight: float = 0.2
    attr_weight: float = 0.1

    # Vector store configuration
    chroma_persist_dir: str = "data/chroma"
    embedding_model: str = "all-MiniLM-L6-v2"

    # Chat configuration
    system_prompt: str = "You are a helpful assistant for document analysis."
    max_tokens: int = 1024
    refusal_phrases: list[str] = [
        "I don't know",
        "I cannot answer",
        "Not enough information",
    ]

    # Security
    token_budget_per_request: int = 4096
    allowed_pid_directories: list[str] = ["data/samples"]

    # Evaluation
    eval_threshold: float = 0.7


settings = Settings()
