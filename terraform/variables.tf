# Input variables for Terraform configuration

variable "project_name" {
  description = "Name of the project (used for resource naming)"
  type        = string
  default     = "smartpath"
}

variable "location" {
  description = "Azure region where resources will be created (must be allowed by subscription policy)"
  type        = string
  default     = "centralindia"
}

variable "subscription_id" {
  description = "Azure subscription ID (optional - will use default from az login if not provided)"
  type        = string
  default     = null
  sensitive   = true
}

variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
  default     = "smartpath-rg"
}

variable "vnet_address_space" {
  description = "Address space for the Virtual Network (CIDR notation)"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet (Bastion Host)"
  type        = string
  default     = "10.0.1.0/24"
}

variable "private_subnet_cidr" {
  description = "CIDR block for the private subnet (Application VM)"
  type        = string
  default     = "10.0.2.0/24"
}

variable "database_subnet_cidr" {
  description = "CIDR block for the database subnet (separate subnet for PostgreSQL delegation)"
  type        = string
  default     = "10.0.3.0/24"
}

variable "vm_size" {
  description = "Size of the virtual machines (Bastion and Application VM)"
  type        = string
  default     = "Standard_B1s"  # Standard B1s - trying for capacity availability
}

variable "admin_username" {
  description = "Administrator username for the VMs"
  type        = string
  default     = "azureuser"
}

variable "my_ip" {
  description = "Your IP address for SSH access to Bastion Host (use 0.0.0.0/0 for anywhere, not recommended for production)"
  type        = string
  default     = "0.0.0.0/0"
}

variable "db_version" {
  description = "PostgreSQL version for the managed database"
  type        = string
  default     = "14"
}

variable "db_sku_name" {
  description = "SKU name for the PostgreSQL Flexible Server"
  type        = string
  default     = "B_Standard_B1ms"
}

variable "db_storage_mb" {
  description = "Storage size in MB for the database"
  type        = number
  default     = 32768
}

variable "db_admin_username" {
  description = "Administrator username for the database"
  type        = string
  sensitive   = true
  default     = "dbadmin"
}

variable "db_admin_password" {
  description = "Administrator password for the database"
  type        = string
  sensitive   = true
  default     = "TempPassword123!"
}

variable "acr_sku" {
  description = "SKU for Azure Container Registry (Basic, Standard, Premium)"
  type        = string
  default     = "Basic"
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default = {
    Environment = "dev"
    Project     = "SmartPath"
    ManagedBy   = "Terraform"
  }
}
