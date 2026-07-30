"""Prometheus metrics registry stub."""

from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram

# Create a custom registry
registry = CollectorRegistry()

# Counters
INGESTION_COUNT = Counter(
    "document_ingestion_total",
    "Total number of document ingestions",
    ["format", "status"],
    registry=registry,
)

DELTA_COMPUTATION_COUNT = Counter(
    "delta_computation_total",
    "Total number of delta computations",
    ["status"],
    registry=registry,
)

CHAT_REQUEST_COUNT = Counter(
    "chat_requests_total",
    "Total number of chat requests",
    ["status"],
    registry=registry,
)

LLM_TOKEN_COUNT = Counter(
    "llm_tokens_total",
    "Total number of LLM tokens used",
    ["type"],  # prompt or completion
    registry=registry,
)

# Gauges
ACTIVE_CONNECTIONS = Gauge(
    "active_connections",
    "Number of active connections",
    registry=registry,
)

DOCUMENT_PAGES_GAUGE = Gauge(
    "document_pages",
    "Number of pages in document",
    ["pid"],
    registry=registry,
)

# Histograms
INGESTION_DURATION = Histogram(
    "ingestion_duration_seconds",
    "Time spent on document ingestion",
    buckets=[0.1, 0.5, 1.0, 5.0, 10.0, 30.0],
    registry=registry,
)

DELTA_DURATION = Histogram(
    "delta_duration_seconds",
    "Time spent on delta computation",
    buckets=[0.1, 0.5, 1.0, 5.0, 10.0, 30.0],
    registry=registry,
)

CHAT_RESPONSE_DURATION = Histogram(
    "chat_response_duration_seconds",
    "Time spent generating chat responses",
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
    registry=registry,
)

LLM_LATENCY = Histogram(
    "llm_latency_seconds",
    "LLM request latency",
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0],
    registry=registry,
)
