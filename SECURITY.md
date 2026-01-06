# Security Policy

## Supported Versions

We actively support the latest minor version of SparseTagging with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 2.4.x   | :white_check_mark: |
| < 2.4   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in SparseTagging, please report it responsibly:

1. **Do NOT** create a public GitHub issue for security vulnerabilities
2. Email security concerns to: noreply@sparsetag.org
3. Include detailed information:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

We will acknowledge receipt within 48 hours and aim to provide a fix within 7 days for critical issues.

## Current Security Status

**Last Updated:** 2026-01-06
**Latest Secure Version:** v2.4.1

### Vulnerability Summary

- **CRITICAL:** 0
- **HIGH:** 0
- **MEDIUM:** 2 (in base image only)
- **Application Dependencies:** Clean ✓

### Known Vulnerabilities

#### Base Image (python:3.11-slim on Debian)

**CVE-2025-14104 - util-linux Heap Buffer Overread**
- **Severity:** MEDIUM (CVSS 5.5)
- **Status:** No fix available from Debian (as of 2026-01-06)
- **Affected Packages:** util-linux, bsdutils, login, mount (10 packages)
- **Impact:** Heap buffer overread in setpwnam() when processing 256-byte usernames
- **Risk to SparseTag:** **LOW**
  - Affects SUID login utilities writing to password database
  - SparseTag is a data processing library with no login/authentication functionality
  - Containerized applications don't use login utilities
  - Requires local access and crafted input
- **Mitigation:** Not required - vulnerability is not exploitable in SparseTag's use case
- **Monitoring:** Awaiting Debian security update; will rebuild image when available

**CVE-2025-7709 - libsqlite3-0 Integer Overflow**
- **Severity:** MEDIUM (CVSS 5.5)
- **Status:** No fix available from Debian (as of 2026-01-06)
- **Affected Package:** libsqlite3-0 3.46.1-7
- **Impact:** Integer overflow in FTS5 full-text search extension
- **Risk to SparseTag:** **VERY LOW**
  - Only affects SQLite FTS5 extension (full-text search)
  - SparseTag does not use SQLite
  - Python 3.11 includes SQLite but SparseTag's dependencies (numpy, scipy, psutil) don't use it
  - Application code has zero SQLite calls
- **Mitigation:** Not required - SQLite is not used by SparseTag
- **Monitoring:** Will update when Debian patches become available during routine base image updates

### Application Dependencies

**Python Dependencies: CLEAN ✓**

All direct dependencies are free of known vulnerabilities:

- **numpy** ≥1.20.0: No CVEs
- **scipy** ≥1.8.0: No CVEs
- **psutil** ≥5.8.0: No CVEs

**Dependency Monitoring:**
- GitHub Dependabot configured for automated CVE alerts
- Automatic PRs created for security updates
- See `.github/dependabot.yml` for configuration

## Security Scanning

### Automated Scans

**Trivy (Container Security)**
- Runs on every push and pull request
- Scans Docker images for CVEs, secrets, and misconfigurations
- Results available in GitHub Actions artifacts under "ScanResults/"
- SARIF reports uploaded to GitHub Security tab

**SonarCloud (Code Quality & Security)**
- Continuous code analysis on every PR
- Zero security vulnerabilities maintained (Security Rating: A)
- Dashboard: https://sonarcloud.io/project/overview?id=vonbraun_SparseTagging

**Dependabot (Dependency CVEs)**
- Monitors numpy, scipy, psutil for known CVEs
- Automatic security update PRs
- Configured to check weekly

### Manual Security Review

To run security scans locally:

```bash
# Scan Python dependencies for CVEs
pip install pip-audit
pip-audit -r requirements.txt

# Scan Docker image with Trivy
docker build -t sparsetagging:local .
trivy image sparsetagging:local --severity CRITICAL,HIGH,MEDIUM

# Run SonarCloud analysis (requires SonarCloud token)
# See .github/workflows/sonar-scan.yml for configuration
```

## Security Best Practices

### Docker Image Security

The SparseTagging Docker image follows security best practices:

1. **Minimal Base Image:** Uses python:3.11-slim (reduced attack surface)
2. **Non-Root User:** Runs as user `sparsetag` (UID 1000), not root
3. **Multi-Stage Build:** Separates build dependencies from runtime
4. **No Secrets:** No credentials or API keys in image
5. **Pinned Dependencies:** All Python packages use version constraints
6. **Updated pip:** Version 25.3 (fixes CVE-2025-8869)

### Production Deployment

For production use, we recommend:

1. **Scan Images:** Always scan with Trivy before deployment
2. **Read-Only Filesystem:** Mount application as read-only when possible
3. **Drop Capabilities:** Remove unnecessary Linux capabilities
4. **Network Isolation:** Run containers in isolated networks
5. **Resource Limits:** Set CPU/memory limits to prevent DoS
6. **Update Regularly:** Rebuild images monthly for security patches

## Recent Security Updates

### v2.4.1 (2026-01-06)

**Fixed:**
- CVE-2025-8869 (pip): Upgraded pip to 25.3 in Dockerfile
  - Fixes symbolic link vulnerability in tar extraction
  - Affects both builder and runtime stages
  - Python 3.11 already includes PEP 706 protections, but upgrade provides defense-in-depth

**Added:**
- SECURITY.md: This security policy document
- Risk assessment for unpatched base image CVEs

### v2.4.0 (2025-12-23)

**Security Improvements:**
- 100% type hint coverage with mypy strict mode (prevents type-related bugs)
- Custom exception hierarchy for better error handling
- No security vulnerabilities in release

## Security Contact

For security-related questions or concerns:
- Email: noreply@sparsetag.org
- GitHub Security Advisories: https://github.com/cgbraun/SparseTagging/security/advisories

**Please do not use public issues for security vulnerabilities.**

## Acknowledgments

We appreciate responsible disclosure of security vulnerabilities. Security researchers who report valid vulnerabilities will be acknowledged in release notes (unless anonymity is requested).
