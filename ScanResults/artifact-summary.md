# SparseTagging Docker Build Artifacts

**Build Date:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Commit SHA:** 0a56a127ebfcfa09dc764b72634ee2a9d2bfbb32
**Branch:** main

## Available Artifacts

### 1. Docker Image (`docker-image`)
- **File:** `sparsetagging-0a56a127ebfcfa09dc764b72634ee2a9d2bfbb32.tar.gz`
- **Size:** ~300MB (compressed)
- **Usage:**
  ```bash
  # Download and load the image
  gunzip sparsetagging-0a56a127ebfcfa09dc764b72634ee2a9d2bfbb32.tar.gz
  docker load -i sparsetagging-0a56a127ebfcfa09dc764b72634ee2a9d2bfbb32.tar

  # Run the image
  docker run --rm sparsetagging:0a56a127ebfcfa09dc764b72634ee2a9d2bfbb32

  # Interactive shell
  docker run --rm -it sparsetagging:0a56a127ebfcfa09dc764b72634ee2a9d2bfbb32 /bin/bash
  ```

### 2. Trivy Vulnerability Report (`trivy-vulnerability-report`)
- **File:** `trivy-report.txt`
- **Format:** Human-readable table
- **Severities:** CRITICAL, HIGH, MEDIUM
- **Scans:** Vulnerabilities, Secrets, Misconfigurations
- **Usage:** Open in text editor to review findings

### 3. Trivy SARIF Report (`trivy-sarif-report`)
- **File:** `trivy-results.sarif`
- **Format:** SARIF (machine-readable)
- **Usage:** Import into security tools, IDEs, or GitHub Security

### 4. SBOM - Software Bill of Materials (`sbom`)
- **File:** `sbom.spdx.json`
- **Format:** SPDX JSON
- **Usage:** Compliance, license tracking, supply chain security
  ```bash
  # View with Trivy
  trivy sbom sbom.spdx.json

  # Validate SPDX
  java -jar spdx-tools.jar Verify sbom.spdx.json
  ```

## Image Details

- **Base Image:** python:3.11-slim
- **Architecture:** linux/amd64
- **User:** sparsetag (UID 1000, non-root)
- **Working Directory:** /app
- **Python Version:** 3.11
- **SparseTagging Version:** 2.4.0

## Testing the Image

```bash
# Load the image
docker load -i sparsetagging-0a56a127ebfcfa09dc764b72634ee2a9d2bfbb32.tar

# Verify it works
docker run --rm sparsetagging:0a56a127ebfcfa09dc764b72634ee2a9d2bfbb32 python -c "import sparsetagging; print('OK')"

# Run benchmarks (if available)
docker run --rm sparsetagging:0a56a127ebfcfa09dc764b72634ee2a9d2bfbb32 python -m pytest --version
```

## Security Review

1. **Review vulnerabilities:** Check `trivy-report.txt`
2. **Check SARIF:** Import `trivy-results.sarif` to IDE
3. **Verify SBOM:** Review `sbom.spdx.json` for dependencies
4. **Test image:** Load and run security scans locally

## GitHub Container Registry

On main branch, this image is also published to:
```
ghcr.io/cgbraun/sparsetagging:latest
ghcr.io/cgbraun/sparsetagging:2.4.0
```

Pull and use:
```bash
docker pull ghcr.io/cgbraun/sparsetagging:latest
docker run --rm ghcr.io/cgbraun/sparsetagging:latest
```
