package security.terraform

# Terraform Security Policy
# Ensures Infrastructure as Code follows security best practices

import future.keywords.contains
import future.keywords.if
import future.keywords.in

# Deny public access to storage accounts
deny[msg] {
    input.resource.azurerm_storage_account[name]
    input.resource.azurerm_storage_account[name].public_network_access_enabled != false
    msg = sprintf("Storage account '%s' should disable public network access", [name])
}

# Ensure encryption is enabled for SQL databases
deny[msg] {
    input.resource.azurerm_mssql_database[name]
    input.resource.azurerm_mssql_database[name].transparent_data_encryption_enabled != true
    msg = sprintf("SQL Database '%s' should have transparent data encryption enabled", [name])
}

# Check for HTTPS-only enforcement on App Services
deny[msg] {
    input.resource.azurerm_app_service[name]
    input.resource.azurerm_app_service[name].https_only != true
    msg = sprintf("App Service '%s' should enforce HTTPS only", [name])
}

# Ensure minimum TLS version is set
warn[msg] {
    input.resource.azurerm_app_service[name]
    site_config := input.resource.azurerm_app_service[name].site_config[_]
    not site_config.min_tls_version
    msg = sprintf("App Service '%s' should specify minimum TLS version (1.2 or higher)", [name])
}

# Ensure Container Registry has admin account disabled
warn[msg] {
    input.resource.azurerm_container_registry[name]
    input.resource.azurerm_container_registry[name].admin_enabled == true
    msg = sprintf("Container Registry '%s' should have admin account disabled for production", [name])
}

# Check for network security group rules
warn[msg] {
    input.resource.azurerm_network_security_rule[name]
    rule := input.resource.azurerm_network_security_rule[name]
    rule.access == "Allow"
    rule.direction == "Inbound"
    rule.source_address_prefix == "*"
    msg = sprintf("Network Security Rule '%s' allows inbound traffic from any source", [name])
}

# Ensure Key Vault has soft delete retention configured
# Note: In azurerm provider v3.0+, soft delete is enabled by default
warn[msg] {
    input.resource.azurerm_key_vault[name]
    not input.resource.azurerm_key_vault[name].soft_delete_retention_days
    msg = sprintf("Key Vault '%s' should specify soft_delete_retention_days (recommended: 90)", [name])
}
