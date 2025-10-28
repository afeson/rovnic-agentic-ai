# Stage 1: Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs models

# Expose port
EXPOSE 8080

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=8080 \
    HOST=0.0.0.0 \
    LOG_LEVEL=INFO \
    ENVIRONMENT=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Default command: run API server
CMD ["python", "-m", "uvicorn", "src.api_server:app", "--host", "0.0.0.0", "--port", "8080"]

# Alternative command for scheduler (override with: docker run -e COMMAND=scheduler)
# CMD ["python", "src/main.py"]
