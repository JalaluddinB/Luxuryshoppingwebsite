# Azure SQL Database
resource "azurerm_mssql_server" "sql" {
  name                         = "sql-oslp-prod-001"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "ChangeThisPassword123!" 
}

resource "azurerm_mssql_database" "db" {
  name      = "sqldb-oslp-prod"
  server_id = azurerm_mssql_server.sql.id
  sku_name  = "S0"
}

# Azure Key Vault
resource "azurerm_key_vault" "kv" {
  name                        = "kv-oslp-prod-001"
  location                    = azurerm_resource_group.rg.location
  resource_group_name         = azurerm_resource_group.rg.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false
}

data "azurerm_client_config" "current" {}

# NOTE: Production Deployment requires Private Endpoints
# Below is an example placeholder for connecting SQL to the PaaS Subnet.
# Repeat similar blocks for Redis, OpenAI, and KeyVault.

/*
resource "azurerm_private_endpoint" "sql_pe" {
  name                = "pe-sql-prod"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  subnet_id           = azurerm_subnet.paas_subnet.id

  private_service_connection {
    name                           = "psc-sql"
    private_connection_resource_id = azurerm_mssql_server.sql.id
    subresource_names              = ["sqlServer"]
    is_manual_connection           = false
  }
}
*/
