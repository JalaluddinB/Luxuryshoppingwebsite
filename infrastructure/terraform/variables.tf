variable "resource_group_name" {
  description = "Name of the resource group"
  default     = "rg-oslp-prod-002"
}

variable "location" {
  description = "Azure region"
  default     = "eastasia"
}

variable "vnet_name" {
  description = "Name of the Virtual Network"
  default     = "vnet-oslp-prod-001"
}

variable "aks_name" {
  description = "Name of the AKS Cluster"
  default     = "aks-oslp-prod-001"
}
