FROM python:3.11-slim

# Install system dependencies including tesseract-ocr
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml .

RUN pip install --no-cache-dir -e .

COPY . .

EXPOSE 8000 8501

CMD ["uvicorn", "src.chat.api:app", "--host", "0.0.0.0", "--port", "8000"]
