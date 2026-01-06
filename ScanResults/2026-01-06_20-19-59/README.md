# Security Scan Results

**Scan Date:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Commit SHA:** b022e61c2036552fb683453f0c0e91cc24af653d
**Branch:** main
**Workflow Run:** https://github.com/cgbraun/SparseTagging/actions/runs/20760846208

---

## Vulnerability Summary (Trivy)

| Severity | Count |
|----------|-------|
| CRITICAL | ${CRITICAL_COUNT} |
| HIGH     | ${HIGH_COUNT} |
| MEDIUM   | ${MEDIUM_COUNT} |
| LOW      | ${LOW_COUNT} |

> **Note:** Counts are approximate based on keyword matching. See `trivy-report.txt` for full details.

---

## Available Files

### 1. `trivy-results.sarif`
- **Format:** SARIF (Static Analysis Results Interchange Format)
- **Purpose:** Machine-readable security findings
- **Usage:**
  - Import into VS Code, PyCharm, or other IDEs with SARIF support
  - Upload to GitHub Security tab (Code Scanning)
  - Process with automated security tools
- **Contains:** Vulnerabilities, secrets, misconfigurations
- **Severity Filter:** CRITICAL, HIGH only

### 2. `trivy-report.txt`
- **Format:** Human-readable table
- **Purpose:** Quick visual review of all vulnerabilities
- **Usage:** Open in text editor to review findings
- **Contains:** Vulnerabilities, secrets, misconfigurations
- **Severity Filter:** CRITICAL, HIGH, MEDIUM

### 3. `sbom.spdx.json`
- **Format:** SPDX 2.3 JSON
- **Purpose:** Software Bill of Materials for compliance and supply chain security
- **Usage:**
  ```bash
  # View with Trivy
  trivy sbom sbom.spdx.json

  # Validate SPDX format
  # (requires spdx-tools: https://github.com/spdx/tools)
  java -jar spdx-tools.jar Verify sbom.spdx.json
  ```
- **Contains:** All packages, versions, licenses, dependencies

### 4. `sonarcloud-links.md`
- **Format:** Markdown with links
- **Purpose:** Quick access to SonarCloud analysis results
- **Contains:** Links to dashboards, coverage, security hotspots

---

## How to Use These Results

### Quick Security Review

1. **Start with `trivy-report.txt`:** Open and scan for CRITICAL/HIGH severities
2. **Check SBOM:** Review `sbom.spdx.json` to understand all dependencies
3. **Review SonarCloud:** Click links in `sonarcloud-links.md` for code quality issues

### Detailed Analysis

1. **Import SARIF to IDE:**
   - VS Code: Install "SARIF Viewer" extension
   - PyCharm: Settings → Tools → SARIF → Import `trivy-results.sarif`

2. **GitHub Security Tab:**
   - Go to repository Security tab → Code Scanning
   - Results from SARIF upload appear here

3. **Compare with Previous Scans:**
   - Check `ScanResults/` directory for historical scans
   - Compare vulnerability counts over time

---

## Docker Image Details

- **Base Image:** python:3.11-slim (Debian)
- **Application:** SparseTagging v2.4.1
- **Python Version:** 3.11
- **User:** sparsetag (non-root, UID 1000)
- **Architecture:** linux/amd64

---

## Next Steps

If vulnerabilities are found:

1. **Assess Impact:** Check if the CVE affects SparseTagging's use case
2. **Check for Fixes:** See if updated base images or packages are available
3. **Risk Assessment:** Document in SECURITY.md if no fix is available
4. **Patch:** Update Dockerfile or requirements.txt as needed
5. **Retest:** Push changes to trigger new security scan

For questions about these results, see `SECURITY.md` in the repository root.
