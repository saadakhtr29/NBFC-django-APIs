# Use Python 3.9 slim image for compatibility
FROM python:3.9-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user for security
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set work directory and change ownership
WORKDIR /app
RUN chown -R appuser:appuser /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies globally (no virtual environment needed in Docker)
RUN pip install --no-cache-dir -r requirements.txt

# Switch to non-root user
USER appuser

# Copy project files
COPY --chown=appuser:appuser . .

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/media

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python manage.py check || exit 1

# Default command - will be overridden by docker-compose
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
