# Docker Usage Guide

Complete guide for building, scanning, and deploying the SparseTagging Docker image.

## Quick Start

### Prerequisites

1. **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
   - Download: https://www.docker.com/products/docker-desktop
   - Verify installation: `docker --version`

2. **Trivy** (for local vulnerability scanning)
   - Windows (Chocolatey): `choco install trivy`
   - Windows (Manual): Download from https://github.com/aquasecurity/trivy/releases
   - Linux: `sudo apt-get install trivy` or use installer script
   - Verify: `trivy --version`

### Build Image Locally

```bash
# Option 1: Using the build script (recommended)
bash scripts/build-docker.sh

# Option 2: Manual build
docker build -t sparsetagging:2.4.0 .
```

### Run the Image

```bash
# Run default command (prints library version)
docker run --rm sparsetagging:2.4.0

# Interactive Python shell
docker run --rm -it sparsetagging:2.4.0 python

# Interactive bash shell
docker run --rm -it sparsetagging:2.4.0 /bin/bash

# Run a specific Python script
docker run --rm -v $(pwd)/examples:/app/examples sparsetagging:2.4.0 python examples/demo.py
```

## Security Scanning

### Local Trivy Scan

```bash
# Scan for HIGH and CRITICAL vulnerabilities
trivy image --severity HIGH,CRITICAL sparsetagging:2.4.0

# Full scan with all severities
trivy image sparsetagging:2.4.0

# Generate SBOM (Software Bill of Materials)
trivy image --format spdx-json --output sbom.json sparsetagging:2.4.0

# Scan for misconfigurations
trivy config .
```

### CI/CD Scanning

The GitHub Actions workflow automatically:
- Scans every build with Trivy
- Uploads results to GitHub Security tab
- Generates SBOM artifacts
- Fails build if CRITICAL/HIGH vulnerabilities found

View results:
1. Go to repository → **Security** → **Code scanning**
2. Filter by **Tool: Trivy**
3. Review vulnerability details

## Image Details

### Multi-Stage Build

**Stage 1 (Builder):**
- Installs build dependencies (gcc, gfortran, etc.)
- Creates isolated virtual environment
- Builds Python wheel package

**Stage 2 (Runtime):**
- Minimal base image (python:3.11-slim)
- Only runtime dependencies (libopenblas0)
- Non-root user (UID 1000)
- Optimized for size and security

### Image Specifications

- **Base**: python:3.11-slim (~150MB)
- **Final Size**: ~300MB (estimated)
- **Architecture**: AMD64 (Intel/AMD x86_64)
- **User**: sparsetag (UID 1000, non-root)
- **Working Directory**: /app
- **Health Check**: Every 30s, checks Python import

### OCI Labels

```dockerfile
org.opencontainers.image.title="SparseTagging"
org.opencontainers.image.version="2.4.0"
org.opencontainers.image.description="High-performance sparse array library"
org.opencontainers.image.source="https://github.com/cgbraun/SparseTagging"
```

## Pushing to GitHub Container Registry

### Setup GHCR

1. **Generate Personal Access Token (PAT)**
   - Go to GitHub → Settings → Developer settings → Personal access tokens
   - Create token with `write:packages` scope

2. **Login to GHCR**
   ```bash
   echo $GHCR_TOKEN | docker login ghcr.io -u YOUR_USERNAME --password-stdin
   ```

### Manual Push

```bash
# Tag for GHCR
docker tag sparsetagging:2.4.0 ghcr.io/cgbraun/sparsetagging:2.4.0
docker tag sparsetagging:2.4.0 ghcr.io/cgbraun/sparsetagging:latest

# Push to registry
docker push ghcr.io/cgbraun/sparsetagging:2.4.0
docker push ghcr.io/cgbraun/sparsetagging:latest
```

### Automatic CI Push

When you push to `main` branch:
1. GitHub Actions builds image
2. Scans with Trivy
3. Automatically pushes to `ghcr.io/cgbraun/sparsetagging`
4. Tags with `:latest` and `:2.4.0`

## Using the Published Image

### Pull from GHCR

```bash
# Pull latest version
docker pull ghcr.io/cgbraun/sparsetagging:latest

# Pull specific version
docker pull ghcr.io/cgbraun/sparsetagging:2.4.0

# Run pulled image
docker run --rm ghcr.io/cgbraun/sparsetagging:latest
```

### In Python Applications

**Dockerfile example:**
```dockerfile
FROM ghcr.io/cgbraun/sparsetagging:2.4.0

# Copy your application
COPY app.py /app/

# Run your application
CMD ["python", "app.py"]
```

**Docker Compose example:**
```yaml
version: '3.8'
services:
  app:
    image: ghcr.io/cgbraun/sparsetagging:2.4.0
    volumes:
      - ./data:/app/data
    command: python /app/process_data.py
```

## Testing Inside Container

### Run Unit Tests

```bash
# Copy tests into container and run
docker run --rm \
  -v $(pwd)/tests:/app/tests \
  sparsetagging:2.4.0 \
  python -m pytest /app/tests/ -v
```

### Interactive Development

```bash
# Mount source code for development
docker run --rm -it \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/tests:/app/tests \
  sparsetagging:2.4.0 \
  /bin/bash
```

## Advanced Usage

### Custom Entrypoint

```bash
# Run with custom Python command
docker run --rm sparsetagging:2.4.0 \
  python -c "from sparsetagging import SparseTag; print(SparseTag.__version__)"
```

### Environment Variables

```bash
# Set Python environment variables
docker run --rm \
  -e PYTHONUNBUFFERED=1 \
  -e LOG_LEVEL=DEBUG \
  sparsetagging:2.4.0 \
  python your_script.py
```

### Resource Limits

```bash
# Limit CPU and memory
docker run --rm \
  --cpus="2.0" \
  --memory="2g" \
  sparsetagging:2.4.0
```

## Troubleshooting

### Build Issues

**Problem:** Build fails with "No space left on device"
```bash
# Clean up Docker resources
docker system prune -a
```

**Problem:** Build hangs at dependency installation
```bash
# Increase Docker memory limit in Docker Desktop settings
# Recommended: 4GB+ for building scipy/numpy
```

**Problem:** Permission denied errors
```bash
# Ensure Docker daemon is running
# Windows: Check Docker Desktop is started
# Linux: sudo systemctl start docker
```

### Scan Issues

**Problem:** Trivy not found
```bash
# Windows: Install via Chocolatey
choco install trivy

# Or download binary from GitHub releases
# https://github.com/aquasecurity/trivy/releases
```

**Problem:** Trivy database errors
```bash
# Clear Trivy cache
trivy clean --all

# Re-download vulnerability database
trivy image --download-db-only
```

### Runtime Issues

**Problem:** "sparsetagging module not found"
```bash
# Verify image built correctly
docker run --rm sparsetagging:2.4.0 python -c "import sparsetagging; print('OK')"
```

**Problem:** Health check failing
```bash
# Check container logs
docker ps -a  # Get container ID
docker logs CONTAINER_ID

# Run health check manually
docker exec CONTAINER_ID python -c "import sparsetagging; print('OK')"
```

## Best Practices

1. **Always scan before deployment**
   ```bash
   trivy image --severity HIGH,CRITICAL your-image:tag
   ```

2. **Use specific version tags**
   ```yaml
   # Good
   image: ghcr.io/cgbraun/sparsetagging:2.4.0

   # Avoid in production
   image: ghcr.io/cgbraun/sparsetagging:latest
   ```

3. **Keep base images updated**
   - Rebuild weekly to get security patches
   - Monitor Dependabot alerts

4. **Review SBOM regularly**
   ```bash
   trivy sbom sbom.spdx.json
   ```

5. **Use minimal permissions**
   - Image runs as non-root (UID 1000)
   - No sudo/root access needed

## Additional Resources

- **Docker Documentation**: https://docs.docker.com/
- **Trivy Documentation**: https://aquasecurity.github.io/trivy/
- **GHCR Documentation**: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
- **OCI Image Spec**: https://github.com/opencontainers/image-spec

## Support

For issues with:
- **SparseTagging library**: Open issue on GitHub repository
- **Docker build**: Check Dockerfile and .dockerignore configuration
- **CI/CD**: Review GitHub Actions logs in repository
- **Security concerns**: Email security@sparsetag.org (or your contact)
