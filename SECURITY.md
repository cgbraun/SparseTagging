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

**Last Updated:** 2026-01-18
**Latest Secure Version:** v2.4.1

### Vulnerability Summary

- **CRITICAL:** 0
- **HIGH:** 2 (accepted risk - base image + build dependency)
- **MEDIUM:** 2 (in base image only)
- **Application Dependencies:** Clean ✓

### Known Vulnerabilities

#### Base Image (python:3.11-slim on Debian)

**CVE-2026-0861 - glibc memalign Integer Overflow** ⚠️ **ACCEPTED RISK**
- **Severity:** HIGH (CVSS 8.0)
- **Status:** ⏳ Awaiting fix from Debian (no patch available as of 2026-01-18)
- **Affected Packages:** libc6@2.41-12+deb13u1, libc-bin@2.41-12+deb13u1
- **Impact:** Integer overflow in memalign suite of functions (memalign, posix_memalign, aligned_alloc) may result in heap corruption when processing extremely large alignment values
- **Risk to SparseTag:** **VERY LOW**
  - Exploitation requires attacker control over BOTH size and alignment arguments
  - Alignment must be in range [1<<62+1, 1<<63] with size near PTRDIFF_MAX (extremely uncommon)
  - SparseTag does not directly call memalign functions
  - NumPy/SciPy may use these internally but only with safe, controlled alignments (page size, block size, etc.)
  - Typical alignment values are small constants, not attacker-controlled
- **Accepted Risk Rationale:**
  - No fix available from Debian (monitoring https://security-tracker.debian.org/tracker/CVE-2026-0861)
  - Extremely low practical exploitability in SparseTag's use case
  - Switching base images (e.g., Alpine) would break NumPy/SciPy binary wheel compatibility
  - Compatibility testing burden outweighs negligible security benefit
- **Mitigation Plan:**
  - Monitor Debian security tracker for patch availability
  - Rebuild Docker image immediately when patched glibc becomes available
  - Manual review: First Monday of each month
  - Automated tracking: Monthly CI workflow (`.github/workflows/cve-tracker.yml`)
- **Tracking:** GitHub Issue [#18](https://github.com/cgbraun/SparseTagging/issues/18)
- **Documentation:** See Dockerfile (line 33-38) for inline reference
- **Next Review:** 2026-02-03 (first Monday of next month)

**GHSA-58pv-8j8x-9vj2 - jaraco.context Path Traversal** ⚠️ **ACCEPTED RISK**
- **Severity:** HIGH (CVSS 8.6)
- **Status:** ⏳ Awaiting setuptools to update vendored dependency (no fix available as of 2026-01-18)
- **Affected Package:** jaraco.context@5.3.0 (vendored within setuptools)
- **Impact:** Zip Slip path traversal vulnerability in `jaraco.context.tarball()` function allows arbitrary file writes when extracting malicious tar archives
- **Risk to SparseTag:** **VERY LOW**
  - jaraco.context is only present in Docker **builder stage**, not runtime
  - setuptools vendors (bundles) jaraco.context 5.3.0 internally in `_vendor/` directory
  - SparseTag does not extract tar archives at runtime
  - Vulnerability only exploitable if application processes untrusted tar files using setuptools' vendored code
  - Runtime Docker image does not include setuptools or its vendored dependencies
- **Accepted Risk Rationale:**
  - No practical fix available - setuptools maintainers must update vendored copy
  - Build-time only dependency, not accessible at runtime
  - Installing jaraco.context 6.1.0+ separately doesn't affect setuptools' internal vendored copy
  - Extremely low practical exploitability in SparseTag's use case
  - Standard practice to wait for upstream (setuptools) to update vendored dependencies
- **Mitigation Plan:**
  - Monitor setuptools GitHub releases for vendored jaraco.context updates
  - Rebuild Docker image immediately when setuptools updates to jaraco.context >=6.1.0
  - Manual review: First Monday of each month
  - Automated tracking: Monthly CI workflow (`.github/workflows/cve-tracker.yml`)
- **Tracking:** GitHub Issue [#19](https://github.com/cgbraun/SparseTagging/issues/19)
- **Documentation:** See Dockerfile builder stage for inline reference
- **Next Review:** 2026-02-03 (first Monday of next month)

#### Base Image - Other Vulnerabilities

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

### 2026-01-18 Security Patch

**Fixed:**
- GHSA-58pv-8j8x-9vj2 (jaraco.context): Upgraded setuptools to >=75.7.0 in Dockerfile
  - Fixes path traversal vulnerability in jaraco.context.tarball() (Zip Slip attack)
  - Severity: HIGH (CVSS 8.6)
  - Impact: Prevents arbitrary file writes when extracting malicious tar archives
  - Risk to SparseTag: LOW (library doesn't extract tar files, but fix applied for defense-in-depth)

**Documented:**
- CVE-2026-0861 (glibc memalign): Accepted risk with detailed justification
  - Added to SECURITY.md with full risk assessment
  - Added inline comment in Dockerfile for visibility
  - Created GitHub Issue [#18](https://github.com/cgbraun/SparseTagging/issues/18) for tracking
  - Established monthly review schedule (first Monday of each month)
  - Added automated CVE tracker workflow (`.github/workflows/cve-tracker.yml`)
    - Checks Debian security tracker monthly
    - Auto-comments on issue #18 when fix detected

- GHSA-58pv-8j8x-9vj2 (jaraco.context): Accepted risk - setuptools vendored dependency
  - Added to SECURITY.md with full risk assessment
  - Created GitHub Issue [#19](https://github.com/cgbraun/SparseTagging/issues/19) for tracking
  - Updated CVE tracker workflow to monitor setuptools releases
  - Build-time only dependency, not exploitable at runtime
  - No fix available - awaiting setuptools to update vendored copy

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
