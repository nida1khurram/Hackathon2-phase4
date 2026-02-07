# Backend Dockerfile with security and efficiency optimizations
# Created with Docker AI (Gordon) best practices for optimal containerization

FROM python:3.13-slim

# Install system dependencies in a single layer with cleanup for smaller image
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/doc/* \
    && rm -rf /usr/share/man/*

# Create dedicated non-root user with specific UID for security
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m -s /bin/bash appuser

# Set working directory
WORKDIR /app

# Copy project file for dependency installation (optimized for layer caching)
COPY pyproject.toml ./

# Install Python package manager and create virtual environment with security considerations
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uv && \
    uv venv && \
    rm -rf /root/.cache

# Install application dependencies with security and efficiency optimizations
RUN . .venv/bin/activate && \
    uv pip install --only-binary=all --compile-bytecode --no-cache-dir -e . && \
    rm -rf /root/.cache

# Copy application code with proper ownership
COPY --chown=appuser:appgroup . .

# Switch to non-root user for security
USER appuser

# Expose application port
EXPOSE 8000

# Health check to monitor application status
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Set environment variables with secure defaults
ENV DATABASE_URL=${DATABASE_URL:-sqlite:///./todo_app_local.db}
ENV OPENROUTER_API_KEY=${OPENROUTER_API_KEY:-""}

# Activate virtual environment and start the application
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "run_server.py"]