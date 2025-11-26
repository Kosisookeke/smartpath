# Output values for Terraform configuration
# These outputs provide important information after infrastructure deployment

output "bastion_public_ip" {
  description = "Public IP address of the Bastion Host"
  value       = azurerm_public_ip.bastion.ip_address
}

output "app_vm_private_ip" {
  description = "Private IP address of the Application VM"
  value       = azurerm_network_interface.app.private_ip_address
}

output "container_registry_url" {
  description = "URL of the Azure Container Registry"
  value       = azurerm_container_registry.main.login_server
}

output "container_registry_name" {
  description = "Name of the Azure Container Registry"
  value       = azurerm_container_registry.main.name
}

output "database_host" {
  description = "FQDN of the PostgreSQL database server"
  value       = azurerm_postgresql_flexible_server.main.fqdn
}

output "database_name" {
  description = "Name of the PostgreSQL database server"
  value       = azurerm_postgresql_flexible_server.main.name
}

output "ssh_private_key_path" {
  description = "Path to the generated SSH private key file"
  value       = local_file.private_key.filename
  sensitive   = true
}

output "ssh_connection_bastion" {
  description = "SSH command to connect to Bastion Host"
  value       = "ssh -i ${local_file.private_key.filename} ${var.admin_username}@${azurerm_public_ip.bastion.ip_address}"
}

output "ssh_connection_app_via_bastion" {
  description = "SSH command to connect to Application VM via Bastion Host"
  value       = "ssh -i ${local_file.private_key.filename} -J ${var.admin_username}@${azurerm_public_ip.bastion.ip_address} ${var.admin_username}@${azurerm_network_interface.app.private_ip_address}"
}

