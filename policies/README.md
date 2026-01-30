# Open Policy Agent (OPA) Policies

This directory contains Open Policy Agent (OPA) policies for enforcing security and compliance rules across the infrastructure and application.

## Directory Structure

```
policies/
├── security/          # Security-focused policies
│   ├── dockerfile.rego    # Docker security best practices
│   └── terraform.rego     # Azure/Terraform security policies
├── compliance/        # Compliance and governance policies
│   └── general.rego       # General compliance requirements
└── README.md          # This file
```

## Policy Categories

### Security Policies (`security/`)

#### Dockerfile Security (`dockerfile.rego`)
- Ensures base images specify version tags (no `latest`)
- Requires non-root USER specification
- Checks for proper cleanup after apt-get operations
- Recommends HEALTHCHECK instructions

#### Terraform Security (`terraform.rego`)
- Enforces HTTPS-only for App Services
- Ensures encryption for SQL databases
- Checks for secure storage account configurations
- Validates network security group rules
- Ensures Key Vault soft delete is enabled
- Warns about admin accounts on Container Registry

### Compliance Policies (`compliance/`)

#### General Compliance (`general.rego`)
- Requires resource tagging for tracking
- Enforces environment tags
- Ensures accountability with owner/team tags

## Using OPA Policies

### Installation

Install OPA CLI:
```bash
# macOS
brew install opa

# Linux
curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64
chmod +x opa
sudo mv opa /usr/local/bin/

# Windows
# Download from https://openpolicyagent.org/downloads/
```

### Testing Policies

Check policy syntax:
```bash
opa check policies/
```

Run policy tests:
```bash
opa test policies/ -v
```

### Evaluating Infrastructure

Evaluate Terraform plans:
```bash
# Generate Terraform plan as JSON
cd infrastructure/terraform
terraform plan -out=tfplan.binary
terraform show -json tfplan.binary > tfplan.json

# Evaluate with OPA
opa eval --data ../../policies/security/terraform.rego \
         --input tfplan.json \
         --format pretty \
         "data.security.terraform"
```

Evaluate Dockerfile:
```bash
# Parse Dockerfile to JSON (requires dockerfile-json tool or manual conversion)
opa eval --data policies/security/dockerfile.rego \
         --input dockerfile.json \
         --format pretty \
         "data.security.dockerfile"
```

## CI/CD Integration

OPA policies are automatically evaluated in GitHub Actions:
- **Workflow**: `.github/workflows/opa-policy-check.yml`
- **Trigger**: On push/PR to main, or when policies/infrastructure/Dockerfile changes
- **Actions**: Validates policy syntax and runs available tests

## Writing New Policies

### Policy Structure

```rego
package category.name

# Import future keywords for better syntax
import future.keywords.contains
import future.keywords.if
import future.keywords.in

# Deny rules (violations that must be fixed)
deny[msg] {
    # Your condition here
    msg = "Error message describing the violation"
}

# Warn rules (recommendations)
warn[msg] {
    # Your condition here
    msg = "Warning message describing the recommendation"
}
```

### Best Practices

1. **Clear Messages**: Provide actionable error messages
2. **Specific Checks**: Make policies targeted and specific
3. **Document Intent**: Add comments explaining the policy purpose
4. **Test Thoroughly**: Create test cases for your policies
5. **Version Control**: Track policy changes through git

## Resources

- [OPA Documentation](https://www.openpolicyagent.org/docs/latest/)
- [Rego Language Guide](https://www.openpolicyagent.org/docs/latest/policy-language/)
- [OPA Playground](https://play.openpolicyagent.org/)
- [Policy Examples](https://www.openpolicyagent.org/docs/latest/policy-library/)

## Contributing

When adding new policies:
1. Place security policies in `security/`
2. Place compliance policies in `compliance/`
3. Document the policy purpose in comments
4. Add test cases if possible
5. Update this README if adding new categories
