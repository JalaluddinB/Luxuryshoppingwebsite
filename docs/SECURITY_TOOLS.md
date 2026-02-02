# Security Tools Documentation

This document provides detailed information about the security scanning tools integrated into the Luxury Shopping Website project.

## Overview

The project uses four free, open-source security tools to provide comprehensive security coverage:

1. **OWASP ZAP** - Dynamic Application Security Testing (DAST)
2. **Checkov** - Infrastructure as Code (IaC) Security
3. **OWASP Dependency-Check** - Dependency Vulnerability Scanning
4. **Open Policy Agent (OPA)** - Policy Enforcement

## 1. OWASP ZAP (Zed Attack Proxy)

### Purpose
OWASP ZAP is a dynamic application security testing tool that scans running web applications for vulnerabilities.

### What It Does
- Performs automated security scans on the deployed web application
- Detects common web vulnerabilities (XSS, SQL injection, etc.)
- Tests authentication and session management
- Identifies security misconfigurations

### Configuration
- **Workflow**: `.github/workflows/owasp-zap-scan.yml`
- **Target**: Production website (`https://luxuryshoppingwebsite.azurewebsites.net`)
- **Rules**: `.zap/rules.tsv` - Custom rules for ignoring false positives

### Schedule
- On push to `main` branch
- On pull requests
- Weekly on Mondays at 00:00 UTC
- Manual trigger available

### Output
- Creates GitHub issues with scan results
- Generates detailed HTML reports (available as artifacts)
- Non-blocking (won't fail builds)

### Customization
To ignore specific findings, add entries to `.zap/rules.tsv`:
```
scanRuleId    IGNORE    URL
10011         IGNORE    https://luxuryshoppingwebsite.azurewebsites.net/some/path/
```

## 2. Checkov

### Purpose
Checkov is a static code analysis tool for Infrastructure as Code (IaC) that prevents security misconfigurations.

### What It Does
- Scans Terraform configurations for security issues
- Validates Dockerfile best practices
- Checks GitHub Actions workflows for security problems
- Detects over 1000+ policy violations

### Configuration
- **Workflow**: `.github/workflows/checkov-scan.yml`
- **Scope**: 
  - `infrastructure/terraform/` - Terraform files
  - `Dockerfile` - Container configuration
  - `.github/workflows/` - CI/CD workflows

### Schedule
- On push to `main` when infrastructure files change
- On pull requests affecting infrastructure
- Manual trigger available

### Output
- CLI output in workflow logs
- SARIF file uploaded to GitHub Security tab
- Soft-fail mode (warns but doesn't block)

### Key Checks
- Azure resource security configurations
- Network security group rules
- Encryption settings
- Access control policies
- Container security best practices

## 3. OWASP Dependency-Check

### Purpose
Identifies known vulnerabilities in project dependencies by checking against the National Vulnerability Database (NVD).

### What It Does
- Scans Python dependencies (`requirements.txt`)
- Checks for known CVEs in dependencies
- Identifies outdated packages with security issues
- Provides remediation recommendations

### Configuration
- **Workflow**: `.github/workflows/dependency-check.yml`
- **Scope**: 
  - `requirements.txt` - Python dependencies
  - Any `package*.json` files (if present)

### Schedule
- On push to `main` when dependencies change
- On pull requests affecting dependencies
- Weekly on Mondays at 02:00 UTC
- Manual trigger available

### Output
- HTML report (human-readable)
- JSON report (machine-readable)
- SARIF file (GitHub Security integration)
- All reports available as artifacts

### Interpreting Results
Reports show:
- CVE identifiers
- Severity levels (Critical, High, Medium, Low)
- Affected dependency versions
- Fixed versions (if available)
- References to vulnerability details

## 4. Open Policy Agent (OPA)

### Purpose
OPA is a policy engine that enforces custom security and compliance policies across infrastructure and code.

### What It Does
- Validates infrastructure configurations against security policies
- Enforces compliance requirements
- Provides policy-as-code framework
- Enables automated policy testing

### Configuration
- **Workflow**: `.github/workflows/opa-policy-check.yml`
- **Policies**: `policies/` directory
  - `policies/security/` - Security policies
  - `policies/compliance/` - Compliance policies

### Available Policies

#### Dockerfile Security (`policies/security/dockerfile.rego`)
- Enforces version tags on base images
- Requires non-root USER specification
- Validates cleanup after apt-get operations
- Recommends HEALTHCHECK instructions

#### Terraform Security (`policies/security/terraform.rego`)
- HTTPS-only enforcement for App Services
- Database encryption requirements
- Storage account security
- Network security group validation
- Key Vault soft delete enforcement

#### Compliance (`policies/compliance/general.rego`)
- Resource tagging requirements
- Environment tag enforcement
- Owner/team accountability tags

### Schedule
- On push to `main` when policies or infrastructure change
- On pull requests
- Manual trigger available

### Output
- Policy validation results in workflow logs
- Policy report (markdown format)
- Uploaded as artifact for review

### Adding New Policies
See [`policies/README.md`](../policies/README.md) for detailed instructions on writing and testing new policies.

## GitHub Security Integration

All tools integrate with GitHub Security features:

### Code Scanning Alerts
- Navigate to **Security** → **Code scanning alerts**
- View Checkov and Dependency-Check findings
- See severity, status, and remediation info

### Workflow Status
- Check **Actions** tab for workflow runs
- View detailed logs for each scan
- Download artifacts for detailed reports

### Pull Request Integration
- ZAP creates issues with findings
- Checkov comments on PRs (when configured)
- Dependency-Check results visible in checks

## Running Scans Locally

### Checkov
```bash
# Install
pip install checkov

# Run scan
checkov -d . --framework terraform,dockerfile,github_actions
```

### OWASP Dependency-Check
```bash
# Download latest version from GitHub releases
# Visit: https://github.com/jeremylong/DependencyCheck/releases
wget https://github.com/jeremylong/DependencyCheck/releases/latest/download/dependency-check-*-release.zip || \
  curl -LO https://github.com/jeremylong/DependencyCheck/releases/latest/download/dependency-check-*-release.zip
unzip dependency-check-*-release.zip

# Run scan
./dependency-check/bin/dependency-check.sh --project "Luxury Shopping" --scan .
```

### OPA
```bash
# Install
curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64
chmod +x opa
sudo mv opa /usr/local/bin/

# Test policies
opa check policies/
opa test policies/ -v
```

### ZAP
```bash
# Using Docker
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://luxuryshoppingwebsite.azurewebsites.net
```

## Best Practices

### 1. Review Scan Results Regularly
- Check GitHub Security tab weekly
- Prioritize Critical and High severity findings
- Address findings before merging PRs

### 2. Keep Dependencies Updated
- Review Dependency-Check reports
- Update vulnerable packages promptly
- Test updates before deploying

### 3. Maintain Policies
- Review and update OPA policies quarterly
- Add new policies as requirements evolve
- Document policy decisions

### 4. False Positive Management
- Document false positives in ZAP rules
- Use Checkov skip annotations when justified
- Add comments explaining exceptions

### 5. Security Champions
- Designate team members as security champions
- Provide training on security tools
- Conduct regular security reviews

## Troubleshooting

### Workflow Failures

#### Checkov Soft Fail
Checkov is configured with `soft_fail: true`, so it won't block builds. Review findings and address critical issues.

#### ZAP Baseline Issues
ZAP runs `fail_action: false` to prevent build blocking. Check created issues for findings.

#### Dependency-Check Timeouts
If dependency scanning times out, increase the workflow timeout or run on schedule only.

### Permission Issues

If workflows can't create issues or upload SARIF:
1. Check workflow permissions in `.github/workflows/`
2. Ensure GitHub Actions has required permissions
3. Verify repository security settings

### Policy Failures

If OPA policies fail:
1. Check policy syntax with `opa check policies/`
2. Review input data format
3. Test policies locally before pushing

## Resources

### Documentation
- [OWASP ZAP](https://www.zaproxy.org/docs/)
- [Checkov](https://www.checkov.io/documentation.html)
- [OWASP Dependency-Check](https://jeremylong.github.io/DependencyCheck/)
- [Open Policy Agent](https://www.openpolicyagent.org/docs/latest/)

### Learning Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Azure Security Best Practices](https://docs.microsoft.com/en-us/azure/security/)
- [Rego Language Guide](https://www.openpolicyagent.org/docs/latest/policy-language/)

### Community
- [OWASP ZAP Google Group](https://groups.google.com/g/zaproxy-users)
- [Checkov Slack](https://slack.bridgecrew.io/)
- [OPA Slack](https://slack.openpolicyagent.org/)

## Support

For issues or questions about security tools:
1. Check workflow logs in GitHub Actions
2. Review this documentation
3. Consult tool-specific documentation
4. Create an issue in the repository
