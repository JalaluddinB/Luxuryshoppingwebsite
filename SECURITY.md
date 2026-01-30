# Security

## Overview

This project implements a comprehensive security strategy using multiple free, open-source security tools for continuous security monitoring and vulnerability detection.

## Security Tools

We use four industry-standard security tools:

### 1. 🛡️ OWASP ZAP
**Dynamic Application Security Testing (DAST)**
- Scans the running web application for vulnerabilities
- Detects: XSS, SQL Injection, CSRF, security misconfigurations
- Runs: Weekly + on every deployment
- [Workflow](.github/workflows/owasp-zap-scan.yml)

### 2. 🔍 Checkov
**Infrastructure as Code Security**
- Scans Terraform, Dockerfile, and GitHub Actions
- Detects: Security misconfigurations, compliance violations
- Runs: On infrastructure code changes
- [Workflow](.github/workflows/checkov-scan.yml)

### 3. 📦 OWASP Dependency-Check
**Software Composition Analysis**
- Scans project dependencies for known vulnerabilities
- Detects: CVEs in Python packages
- Runs: Weekly + on dependency changes
- [Workflow](.github/workflows/dependency-check.yml)

### 4. 📋 Open Policy Agent (OPA)
**Policy Enforcement**
- Enforces custom security and compliance policies
- Validates: Dockerfile, Terraform, resource configurations
- Runs: On policy or infrastructure changes
- [Workflow](.github/workflows/opa-policy-check.yml)
- [Policies](policies/)

## Security Coverage

| Layer | Tool | Coverage |
|-------|------|----------|
| Application | OWASP ZAP | Runtime vulnerabilities |
| Infrastructure | Checkov | IaC misconfigurations |
| Dependencies | Dependency-Check | Known CVEs |
| Policies | OPA | Custom security rules |

## Viewing Security Reports

### GitHub Security Tab
1. Navigate to **Security** → **Code scanning alerts**
2. Filter by tool, severity, or status
3. Review findings and recommended fixes

### Workflow Artifacts
1. Go to **Actions** → Select workflow run
2. Download reports from **Artifacts** section
3. Review detailed HTML/JSON reports

### Pull Requests
- Security findings appear as status checks
- Review comments on PRs for violations
- Links to detailed reports available

## Responding to Security Findings

### Critical & High Severity
1. **Review immediately**
2. Create issue to track fix
3. Assign to appropriate team member
4. Fix and test
5. Re-run security scan to verify

### Medium & Low Severity
1. Review in next sprint planning
2. Prioritize based on risk
3. Schedule for upcoming releases

### False Positives
1. Verify it's truly a false positive
2. Document reasoning
3. Configure tool to suppress
4. Add comment in code if needed

## Security Policies (OPA)

Custom policies enforce security standards:

### Dockerfile Security
- ✅ Version-tagged base images
- ✅ Non-root user specification
- ✅ Cleanup after package installations
- ✅ HEALTHCHECK instructions

### Terraform Security
- ✅ HTTPS enforcement on web apps
- ✅ Database encryption enabled
- ✅ Storage account security
- ✅ Network security group validation
- ✅ Key Vault soft delete

### Compliance
- ✅ Resource tagging requirements
- ✅ Environment tag specification
- ✅ Owner/team accountability

[Learn more about policies →](policies/README.md)

## Running Scans Locally

### Quick Start
```bash
# Checkov (IaC scanning)
pip install checkov
checkov -d .

# OPA (Policy testing)
curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64
chmod +x opa && sudo mv opa /usr/local/bin/
opa check policies/
```

[Detailed instructions →](docs/SECURITY_TOOLS.md)

## Security Best Practices

### For Developers
- ✅ Review security findings before merging PRs
- ✅ Keep dependencies updated
- ✅ Follow secure coding guidelines
- ✅ Add security tests for new features
- ✅ Never commit secrets or credentials

### For Operations
- ✅ Monitor GitHub Security tab regularly
- ✅ Subscribe to security advisories
- ✅ Keep infrastructure definitions updated
- ✅ Review and update policies quarterly
- ✅ Maintain documentation of security decisions

### For Security Champions
- ✅ Triage security findings weekly
- ✅ Provide guidance on remediation
- ✅ Update security policies as needed
- ✅ Conduct security training
- ✅ Review security tool configurations

## Compliance & Standards

Our security tools help achieve compliance with:

- **OWASP Top 10** - Coverage of all major categories
- **CIS Benchmarks** - Azure and Docker benchmarks
- **NIST Framework** - Identify, Protect, Detect, Respond, Recover

[See detailed coverage →](docs/SECURITY_CHECKS.md)

## Documentation

- 📖 [Security Tools Guide](docs/SECURITY_TOOLS.md) - Comprehensive tool documentation
- 📋 [Security Checks Reference](docs/SECURITY_CHECKS.md) - All security checks performed
- 📝 [OPA Policies Guide](policies/README.md) - Policy documentation
- ⚙️ [Workflows README](.github/workflows/README.md) - CI/CD workflow documentation

## Reporting Security Issues

If you discover a security vulnerability:

1. **Do NOT** create a public GitHub issue
2. Email the security team directly
3. Provide detailed information:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Resources

### Official Documentation
- [OWASP ZAP](https://www.zaproxy.org/docs/)
- [Checkov](https://www.checkov.io/documentation.html)
- [OWASP Dependency-Check](https://jeremylong.github.io/DependencyCheck/)
- [Open Policy Agent](https://www.openpolicyagent.org/docs/latest/)

### Learning
- [OWASP Security Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Azure Security](https://docs.microsoft.com/en-us/azure/security/)
- [Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

## Support

For questions or issues:
- 📧 Contact the security team
- 💬 Create an issue (non-security related)
- 📚 Review documentation linked above

---

**Last Updated**: January 2026  
**Security Tools Version**: Latest stable releases
