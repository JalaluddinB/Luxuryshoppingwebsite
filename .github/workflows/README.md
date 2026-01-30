# GitHub Actions Workflows

This directory contains CI/CD and security scanning workflows for the Luxury Shopping Website.

## Available Workflows

### Deployment
- **deploy-to-azure.yml** - Builds Docker image and deploys to Azure App Service
- **generate_uml.yml** - Generates UML diagrams for architecture documentation

### Security Scanning
- **owasp-zap-scan.yml** - OWASP ZAP dynamic application security testing
- **checkov-scan.yml** - Infrastructure as Code security scanning
- **dependency-check.yml** - Dependency vulnerability scanning
- **opa-policy-check.yml** - Open Policy Agent policy validation

## Workflow Triggers

### Deployment Workflows
- Trigger on push to `main` branch
- Manual trigger available via workflow_dispatch

### Security Workflows

#### OWASP ZAP
- On push to `main`
- On pull requests
- Weekly schedule (Mondays 00:00 UTC)
- Manual trigger

#### Checkov
- On push to `main` (when infrastructure files change)
- On pull requests (when infrastructure files change)
- Manual trigger

#### Dependency-Check
- On push to `main` (when dependency files change)
- On pull requests (when dependency files change)
- Weekly schedule (Mondays 02:00 UTC)
- Manual trigger

#### OPA Policy Check
- On push to `main` (when policies/infrastructure change)
- On pull requests (when policies/infrastructure change)
- Manual trigger

## Manual Workflow Execution

To manually trigger any workflow:
1. Go to the **Actions** tab in GitHub
2. Select the workflow from the left sidebar
3. Click **Run workflow** button
4. Select the branch and click **Run workflow**

## Workflow Permissions

All workflows have appropriate permissions configured:
- `contents: read` - Read repository contents
- `security-events: write` - Upload security findings
- `issues: write` - Create issues for findings
- `pull-requests: write` - Comment on PRs

## Viewing Results

### Security Findings
- **Security** tab → **Code scanning alerts**
- View findings from Checkov and Dependency-Check

### Workflow Logs
- **Actions** tab → Select workflow run
- View detailed logs for each step

### Artifacts
- Available in workflow run summary
- Download reports for offline analysis

## Troubleshooting

If workflows fail:
1. Check workflow logs in Actions tab
2. Verify required secrets are configured
3. Check permissions in workflow file
4. Review tool-specific documentation

## Adding New Workflows

When adding new workflows:
1. Create YAML file in `.github/workflows/`
2. Define appropriate triggers
3. Set required permissions
4. Add documentation here
5. Test with manual trigger first

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Security Tools Documentation](../../docs/SECURITY_TOOLS.md)
- [Security Checks Overview](../../docs/SECURITY_CHECKS.md)
