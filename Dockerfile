# syntax=docker/dockerfile:1.4

# Stage 1: Builder
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        gfortran \
        libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy dependency files
WORKDIR /build
COPY requirements.txt pyproject.toml ./
COPY src/ src/

# Install dependencies and build wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir build && \
    python -m build --wheel

# Stage 2: Runtime
FROM python:3.11-slim

# OCI labels
LABEL org.opencontainers.image.title="SparseTagging"
LABEL org.opencontainers.image.version="2.4.0"
LABEL org.opencontainers.image.description="High-performance sparse array library"
LABEL org.opencontainers.image.source="https://github.com/cgbraun/SparseTagging"

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libopenblas0 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash sparsetag

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application
WORKDIR /app
COPY --from=builder /build/dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm /tmp/*.whl

# Copy example scripts (optional)
COPY examples/ examples/ 2>/dev/null || true

# Switch to non-root user
USER sparsetag

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sparsetagging; print('OK')"

# Default command (can be overridden)
CMD ["python", "-c", "import sparsetagging; print('SparseTagging v2.4.0 loaded successfully')"]
