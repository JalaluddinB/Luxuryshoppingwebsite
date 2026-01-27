# NOTE: This configuration uses a standard Load Balancer for Development purposes to save costs.
# In a Production environment, an Application Gateway (WAF) should be used for better security.

# Azure Kubernetes Service (AKS)
resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.aks_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "oslp-aks"

  default_node_pool {
    name           = "default"
    node_count     = 2
    vm_size        = "Standard_B2s_v2"
    vnet_subnet_id = azurerm_subnet.compute_subnet.id
  }

  identity {
    type = "SystemAssigned"
  }

  # ingress_application_gateway block removed for Dev environment

  network_profile {
    network_plugin    = "azure"
    service_cidr      = "10.1.0.0/16"
    dns_service_ip    = "10.1.0.10"
    load_balancer_sku = "standard"
  }
}

# Grant AKS access to pull from ACR
resource "azurerm_role_assignment" "aks_acr_pull" {
  principal_id                     = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.acr.id
  skip_service_principal_aad_check = true
}
