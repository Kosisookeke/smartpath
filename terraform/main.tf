# Terraform configuration for SmartPath Azure Infrastructure
# This file defines all Azure resources required for the application

terraform {
  required_version = ">= 1.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

# Configure the Azure Provider
# This will automatically use credentials from 'az login' (similar to AWS 'aws configure')
# For local use: Run 'az login' before running terraform commands
# For Terraform Cloud: Set ARM_* environment variables in workspace settings
provider "azurerm" {
  features {
    resource_group {
      # Allow resource group deletion even if it contains resources
      # This is needed when replacing resource groups due to location changes
      prevent_deletion_if_contains_resources = false
    }
  }
  
  # Optional: Specify subscription ID (uses default from az login if not provided)
  subscription_id = var.subscription_id
}

# Generate SSH key pair for VM access
resource "tls_private_key" "vm_ssh" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Save private key locally (for SSH access)
resource "local_file" "private_key" {
  content         = tls_private_key.vm_ssh.private_key_pem
  filename        = "${path.module}/ssh_key.pem"
  file_permission = "0600"
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location

  tags = var.tags
}

# Virtual Network
resource "azurerm_virtual_network" "main" {
  name                = "${var.project_name}-vnet"
  address_space       = [var.vnet_address_space]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  tags = var.tags
}

# Public Subnet (for Bastion Host)
resource "azurerm_subnet" "public" {
  name                 = "${var.project_name}-public-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = [var.public_subnet_cidr]
}

# Private Subnet (for Application VM)
resource "azurerm_subnet" "private" {
  name                 = "${var.project_name}-private-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = [var.private_subnet_cidr]
}

# Database Subnet (separate subnet with delegation for PostgreSQL)
resource "azurerm_subnet" "database" {
  name                 = "${var.project_name}-database-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = [var.database_subnet_cidr]

  # Delegation required for PostgreSQL Flexible Server
  delegation {
    name = "Microsoft.DBforPostgreSQL.flexibleServers"
    service_delegation {
      name    = "Microsoft.DBforPostgreSQL/flexibleServers"
      actions = ["Microsoft.Network/virtualNetworks/subnets/join/action"]
    }
  }
}

# Network Security Group for Public Subnet (Bastion)
resource "azurerm_network_security_group" "public" {
  name                = "${var.project_name}-public-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  # Allow SSH from your IP (or anywhere if my_ip is 0.0.0.0/0)
  security_rule {
    name                       = "AllowSSHFromMyIP"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = var.my_ip
    destination_address_prefix = "*"
  }

  tags = var.tags
}

# Network Security Group for Private Subnet (Application VM)
resource "azurerm_network_security_group" "private" {
  name                = "${var.project_name}-private-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  # Allow HTTP from internet
  security_rule {
    name                       = "AllowHTTPFromInternet"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
  }

  # Allow HTTPS from internet
  security_rule {
    name                       = "AllowHTTPSFromInternet"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
  }

  # Allow SSH from Bastion Host only
  security_rule {
    name                       = "AllowSSHFromBastion"
    priority                   = 1003
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = var.public_subnet_cidr
    destination_address_prefix = "*"
  }

  # Allow database connections from Application VM only
  security_rule {
    name                       = "AllowDatabaseFromAppVM"
    priority                   = 1004
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "5432"
    source_address_prefix      = var.private_subnet_cidr
    destination_address_prefix = "*"
  }
  
  # Allow database connections from Database subnet (for PostgreSQL)
  security_rule {
    name                       = "AllowDatabaseFromDatabaseSubnet"
    priority                   = 1005
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "5432"
    source_address_prefix      = var.database_subnet_cidr
    destination_address_prefix = "*"
  }

  tags = var.tags
}

# Associate NSG with subnets
resource "azurerm_subnet_network_security_group_association" "public" {
  subnet_id                 = azurerm_subnet.public.id
  network_security_group_id = azurerm_network_security_group.public.id
}

resource "azurerm_subnet_network_security_group_association" "private" {
  subnet_id                 = azurerm_subnet.private.id
  network_security_group_id = azurerm_network_security_group.private.id
}

# Public IP for Bastion Host
resource "azurerm_public_ip" "bastion" {
  name                = "${var.project_name}-bastion-pip"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  allocation_method   = "Static"
  sku                 = "Standard"

  tags = var.tags
}

# Network Interface for Bastion Host
resource "azurerm_network_interface" "bastion" {
  name                = "${var.project_name}-bastion-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.public.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.bastion.id
  }

  tags = var.tags
}

# Bastion Host VM
resource "azurerm_linux_virtual_machine" "bastion" {
  name                = "${var.project_name}-bastion-vm"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  size                = var.vm_size
  # Removed zone specification - let Azure choose available zone
  # Removed Spot priority - trying regular VMs for capacity
  admin_username      = var.admin_username

  network_interface_ids = [
    azurerm_network_interface.bastion.id,
  ]

  admin_ssh_key {
    username   = var.admin_username
    public_key = tls_private_key.vm_ssh.public_key_openssh
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  tags = var.tags
}

# Network Interface for Application VM (no public IP)
resource "azurerm_network_interface" "app" {
  name                = "${var.project_name}-app-vm-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.private.id
    private_ip_address_allocation = "Dynamic"
  }

  tags = var.tags
}

# Application VM (in private subnet, no public IP)
resource "azurerm_linux_virtual_machine" "app" {
  name                = "${var.project_name}-app-vm"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  size                = var.vm_size
  # Removed zone specification - let Azure choose available zone
  # Removed Spot priority - trying regular VMs for capacity
  admin_username      = var.admin_username

  network_interface_ids = [
    azurerm_network_interface.app.id,
  ]

  admin_ssh_key {
    username   = var.admin_username
    public_key = tls_private_key.vm_ssh.public_key_openssh
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  tags = var.tags
}

# Azure Database for PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "${var.project_name}-db-${random_string.db_suffix.result}"
  resource_group_name    = azurerm_resource_group.main.name
  location               = azurerm_resource_group.main.location
  version                = var.db_version
  delegated_subnet_id    = azurerm_subnet.database.id
  private_dns_zone_id    = azurerm_private_dns_zone.postgres.id
  administrator_login    = var.db_admin_username
  administrator_password = var.db_admin_password
  zone                   = "1"

  # Disable public network access when using private endpoint (delegated_subnet_id)
  public_network_access_enabled = false

  sku_name = var.db_sku_name

  storage_mb = var.db_storage_mb

  backup_retention_days        = 7
  geo_redundant_backup_enabled = false

  tags = var.tags
}

# Private DNS Zone for PostgreSQL
resource "azurerm_private_dns_zone" "postgres" {
  name                = "${var.project_name}.postgres.database.azure.com"
  resource_group_name = azurerm_resource_group.main.name

  tags = var.tags
}

# Link Private DNS Zone to VNet
resource "azurerm_private_dns_zone_virtual_network_link" "postgres" {
  name                  = "${var.project_name}-postgres-dns-link"
  resource_group_name   = azurerm_resource_group.main.name
  private_dns_zone_name = azurerm_private_dns_zone.postgres.name
  virtual_network_id    = azurerm_virtual_network.main.id
  registration_enabled  = false

  tags = var.tags
}

# Random string for database name uniqueness
resource "random_string" "db_suffix" {
  length  = 6
  special = false
  upper   = false
}

# Random string for ACR name uniqueness
resource "random_string" "acr_suffix" {
  length  = 6
  special = false
  upper   = false
}

# Azure Container Registry (Private)
resource "azurerm_container_registry" "main" {
  name                = "${var.project_name}acr${random_string.acr_suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = var.acr_sku
  admin_enabled       = true

  # Network rules - only allow access from VNet
  # Note: network_rule_set requires Premium SKU. For Basic SKU, we'll use public access with IP restrictions
  network_rule_bypass_option = "AzureServices"
  
  # For Basic SKU, we can't use network_rule_set. ACR will be accessible from VNet via public endpoint.
  # To restrict access, upgrade to Premium SKU or use firewall rules.

  tags = var.tags
}

