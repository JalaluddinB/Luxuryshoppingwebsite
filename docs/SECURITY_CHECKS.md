# Security Checks Overview

This document provides a quick reference of all security checks performed by the integrated security tools.

## Quick Reference Matrix

| Tool | Type | Target | Frequency | Blocking |
|------|------|--------|-----------|----------|
| OWASP ZAP | DAST | Running App | Weekly + PR | No |
| Checkov | SAST | IaC/Docker | On Change | No |
| Dependency-Check | SCA | Dependencies | Weekly + PR | No |
| OPA | Policy | IaC/Config | On Change | No |

## Security Checks by Category

### 1. Application Security (OWASP ZAP)

#### Injection Attacks
- ✓ SQL Injection detection
- ✓ Command Injection detection
- ✓ LDAP Injection detection
- ✓ XML Injection detection

#### Authentication & Session
- ✓ Session fixation
- ✓ Weak authentication
- ✓ Session ID in URL
- ✓ Cookie security flags

#### Cross-Site Attacks
- ✓ Cross-Site Scripting (XSS)
- ✓ Cross-Site Request Forgery (CSRF)
- ✓ Clickjacking

#### Security Misconfigurations
- ✓ Directory listing
- ✓ Server information disclosure
- ✓ Insecure HTTP methods
- ✓ Missing security headers

#### Sensitive Data
- ✓ Sensitive data in URL
- ✓ Password in clear text
- ✓ Credit card exposure

### 2. Infrastructure Security (Checkov)

#### Azure Resources
- ✓ Storage account encryption
- ✓ Storage account public access
- ✓ Network security groups
- ✓ Virtual network configurations
- ✓ Resource tagging

#### App Services
- ✓ HTTPS enforcement
- ✓ TLS version requirements
- ✓ Client certificate authentication
- ✓ Authentication settings

#### Container Registry
- ✓ Admin account usage
- ✓ Vulnerability scanning
- ✓ Network access rules
- ✓ Encryption settings

#### SQL Database
- ✓ Transparent data encryption
- ✓ Firewall rules
- ✓ Threat detection
- ✓ Auditing enabled

#### Key Vault
- ✓ Soft delete enabled
- ✓ Purge protection
- ✓ Network ACLs
- ✓ Access policies

### 3. Container Security (Checkov on Dockerfile)

#### Base Image
- ✓ Image tag specification
- ✓ Official image usage
- ✓ Image vulnerability scanning

#### Best Practices
- ✓ Non-root user
- ✓ HEALTHCHECK instruction
- ✓ Layer optimization
- ✓ Secrets in environment

#### Package Management
- ✓ Package cache cleanup
- ✓ Minimal dependencies
- ✓ Version pinning

### 4. Dependency Security (OWASP Dependency-Check)

#### Python Packages
- ✓ Known CVE detection
- ✓ Outdated package identification
- ✓ Vulnerability severity assessment
- ✓ Remediation recommendations

#### Vulnerability Database
- ✓ NVD (National Vulnerability Database)
- ✓ GitHub Security Advisories
- ✓ npm Security Advisories
- ✓ PyPI advisories

#### Severity Levels
- ✓ Critical (CVSS 9.0-10.0)
- ✓ High (CVSS 7.0-8.9)
- ✓ Medium (CVSS 4.0-6.9)
- ✓ Low (CVSS 0.1-3.9)

### 5. Policy Compliance (OPA)

#### Dockerfile Security Policies
- ✓ Base image version tags required
- ✓ No 'latest' tag usage
- ✓ Non-root USER specified
- ✓ apt-get cleanup verification
- ✓ HEALTHCHECK recommendation

#### Terraform Security Policies
- ✓ Storage account public access disabled
- ✓ SQL database encryption enabled
- ✓ App Service HTTPS enforcement
- ✓ Minimum TLS version set
- ✓ Container Registry admin disabled
- ✓ Network security rules validation
- ✓ Key Vault soft delete enabled

#### Compliance Policies
- ✓ Resource tagging requirements
- ✓ Environment tag presence
- ✓ Owner/team accountability tags

### 6. GitHub Actions Security (Checkov)

#### Workflow Security
- ✓ Third-party action versions
- ✓ Secret handling
- ✓ Permission scoping
- ✓ Branch protection

## Severity Levels

### Critical 🔴
- Immediate attention required
- Can lead to system compromise
- Examples: SQL injection, RCE, exposed secrets

### High 🟠
- Should be addressed soon
- Significant security risk
- Examples: XSS, insecure authentication, missing encryption

### Medium 🟡
- Should be addressed in due course
- Moderate security risk
- Examples: Information disclosure, weak configurations

### Low 🟢
- Nice to fix
- Minor security concern
- Examples: Missing best practices, informational findings

### Informational ℹ️
- Good to know
- No immediate action needed
- Examples: Recommendations, security tips

## Remediation Priority

1. **Critical & High** in Production → Fix immediately
2. **Critical & High** in Development → Fix before production
3. **Medium** → Address in next sprint
4. **Low** → Address during refactoring
5. **Informational** → Consider for improvements

## Automated vs. Manual Checks

### Automated (These Tools)
- ✅ Common vulnerabilities
- ✅ Known CVEs
- ✅ Security misconfigurations
- ✅ Policy violations
- ✅ Best practice violations

### Manual Review Needed
- ⚠️ Business logic flaws
- ⚠️ Complex authentication flows
- ⚠️ Authorization issues
- ⚠️ Custom security controls
- ⚠️ Social engineering vectors

## Continuous Monitoring

### On Every Commit
- Checkov (if infrastructure files changed)
- OPA policies (if policies/infrastructure changed)

### On Pull Requests
- All applicable tools based on changed files
- Results visible in PR checks

### Weekly Scans
- OWASP ZAP (Monday 00:00 UTC)
- Dependency-Check (Monday 02:00 UTC)

### On Demand
- All workflows support manual triggering
- Use GitHub Actions UI to run

## False Positives

### How to Handle
1. **Verify**: Confirm it's actually a false positive
2. **Document**: Add comment explaining why
3. **Configure**: Update tool configuration
   - ZAP: Add to `.zap/rules.tsv`
   - Checkov: Add skip annotation
   - Dependency-Check: Suppress in config
   - OPA: Adjust policy rules

### Example Suppressions

#### ZAP
```
# .zap/rules.tsv
10011    IGNORE    https://example.com/api/endpoint
```

#### Checkov
```hcl
# In Terraform file
# Note: Verify check ID from scan output or Checkov documentation before suppressing
# List of checks: https://www.checkov.io/5.Policy%20Index/terraform.html
resource "azurerm_storage_account" "example" {
  #checkov:skip=CKV_AZURE_35:Public access required for CDN
  public_network_access_enabled = true
}
```

## Integration Points

### GitHub Security Tab
- View all findings in one place
- Filter by severity, status, tool
- Assign to team members

### Pull Requests
- Automated comments on findings
- Status checks for blocking issues
- Links to detailed reports

### Artifacts
- Download detailed reports
- Share with team
- Archive for compliance

### Notifications
- Email on workflow failure
- Slack integration (if configured)
- GitHub notifications

## Compliance Mapping

### OWASP Top 10 Coverage
- A01:2021 – Broken Access Control ✓
- A02:2021 – Cryptographic Failures ✓
- A03:2021 – Injection ✓
- A04:2021 – Insecure Design ✓
- A05:2021 – Security Misconfiguration ✓
- A06:2021 – Vulnerable and Outdated Components ✓
- A07:2021 – Identification and Authentication Failures ✓
- A08:2021 – Software and Data Integrity Failures ✓
- A09:2021 – Security Logging and Monitoring Failures ✓
- A10:2021 – Server-Side Request Forgery (SSRF) ✓

### CIS Benchmarks
- Azure CIS Benchmark (partial coverage via Checkov)
- Docker CIS Benchmark (partial coverage via Checkov)

### NIST Framework
- Identify: Asset discovery and vulnerability identification ✓
- Protect: Policy enforcement and security controls ✓
- Detect: Continuous monitoring and scanning ✓
- Respond: Alert and reporting mechanisms ✓
- Recover: Vulnerability remediation guidance ✓

## Next Steps

1. **Review Initial Scans**: Check GitHub Security tab for findings
2. **Prioritize Fixes**: Address Critical and High severity first
3. **Update Policies**: Customize OPA policies for your needs
4. **Schedule Reviews**: Set up regular security review meetings
5. **Train Team**: Ensure team understands security tools
6. **Document Decisions**: Keep track of security decisions and suppressions

## Resources

- [Security Tools Documentation](SECURITY_TOOLS.md)
- [OPA Policies README](../policies/README.md)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
