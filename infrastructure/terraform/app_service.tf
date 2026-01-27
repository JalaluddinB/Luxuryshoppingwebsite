resource "azurerm_service_plan" "plan" {
  name                = "asp-oslp-prod"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "web" {
  name                = "app-oslp-prod-002"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_service_plan.plan.location
  service_plan_id     = azurerm_service_plan.plan.id

  site_config {
    # Free tier doesn't support always_on, but Basic (B1) does.
    always_on = true
    
    # Example container config - connects to the ACR created in main.tf
    application_stack {
      docker_image     = "zhengqunkoo/Luxuryshoppingwebsite"
      docker_image_tag = "latest"
    }
  }

  app_settings = {
    "WEBSITES_PORT" = "8000" # Flask usually runs on 5000 or 8000
    "DOCKER_REGISTRY_SERVER_URL"      = "https://${azurerm_container_registry.acr.login_server}"
    "DOCKER_REGISTRY_SERVER_USERNAME" = azurerm_container_registry.acr.admin_username
    "DOCKER_REGISTRY_SERVER_PASSWORD" = azurerm_container_registry.acr.admin_password
  }
}
