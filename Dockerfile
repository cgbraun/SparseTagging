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
RUN pip install --no-cache-dir --upgrade pip==25.3 "setuptools>=76.0.0" wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir build && \
    python -m build --wheel

# Stage 2: Runtime
FROM python:3.11-slim

# SECURITY NOTE: Base image contains CVE-2026-0861 (glibc memalign integer overflow, CVSS 8.0)
# Status: Accepted risk pending Debian patch release
# Details: See SECURITY.md (line 42-64) for full risk assessment and justification
# Tracking: GitHub Issue #18, automated monthly checks via .github/workflows/cve-tracker.yml
# Last Reviewed: 2026-01-18
# Fix Available: No (monitoring https://security-tracker.debian.org/tracker/CVE-2026-0861)

# Build argument for version
ARG APP_VERSION=unknown

# Convert ARG to ENV for runtime availability
ENV APP_VERSION=${APP_VERSION}

# OCI labels
LABEL org.opencontainers.image.title="SparseTagging"
LABEL org.opencontainers.image.version="${APP_VERSION}"
LABEL org.opencontainers.image.description="High-performance sparse array library"
LABEL org.opencontainers.image.source="https://github.com/cgbraun/SparseTagging"

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libopenblas0 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to fix CVE-2025-8869
RUN pip install --no-cache-dir --upgrade pip==25.3

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash sparsetag

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application
WORKDIR /app
COPY --from=builder /build/dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm /tmp/*.whl

# Switch to non-root user
USER sparsetag

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sparsetagging; print('OK')"

# Default command (can be overridden)
CMD python -c "import sparsetagging; import os; print(f'SparseTagging v{os.environ.get(\"APP_VERSION\", \"unknown\")} loaded successfully')"
