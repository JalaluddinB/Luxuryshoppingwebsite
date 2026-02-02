package compliance.general

# General Compliance Policy
# Ensures general compliance requirements are met

import future.keywords.contains
import future.keywords.if
import future.keywords.in

# Check for required tags on Azure resources
deny contains msg if {
    resource_types := ["azurerm_resource_group", "azurerm_app_service", "azurerm_container_registry"]
    resource_type := resource_types[_]
    input.resource[resource_type][name]
    resource := input.resource[resource_type][name]
    not resource.tags
    msg = sprintf("Resource '%s' of type '%s' should have tags for compliance tracking", [name, resource_type])
}

# Ensure environment tag exists
warn contains msg if {
    resource_types := ["azurerm_resource_group", "azurerm_app_service"]
    resource_type := resource_types[_]
    input.resource[resource_type][name]
    resource := input.resource[resource_type][name]
    resource.tags
    not resource.tags.environment
    msg = sprintf("Resource '%s' should have an 'environment' tag", [name])
}

# Ensure owner/team tag exists for accountability
warn contains msg if {
    resource_types := ["azurerm_resource_group", "azurerm_app_service"]
    resource_type := resource_types[_]
    input.resource[resource_type][name]
    resource := input.resource[resource_type][name]
    resource.tags
    not resource.tags.owner
    not resource.tags.team
    msg = sprintf("Resource '%s' should have an 'owner' or 'team' tag for accountability", [name])
}
