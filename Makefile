.PHONY: install test lint run chat eval markup clean

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

lint:
	ruff check src/ tests/

run:
	python -m scripts.run_ingest

chat:
	python -m src.chat.ui

eval:
	python -m eval.run_eval

markup:
	python -m scripts.markup_documents

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name *.egg-info -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf data/traces/* data/logs/*
