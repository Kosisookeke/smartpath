# Terraform Infrastructure for SmartPath

This directory contains Terraform configuration files to provision Azure infrastructure for the SmartPath application.

## Architecture Overview

The infrastructure includes:

1. **Virtual Network (VNet)** - Private network with public and private subnets
2. **Bastion Host** - Jumpbox VM in public subnet for secure SSH access
3. **Application VM** - VM in private subnet (not directly accessible from internet)
4. **Managed Database** - Azure Database for PostgreSQL Flexible Server
5. **Network Security Groups (NSGs)** - Firewall rules for secure access
6. **Azure Container Registry (ACR)** - Private container registry

## Security Architecture

- **Application VM is NEVER directly accessible from the internet**
- All SSH access must go through the Bastion Host
- HTTP/HTTPS traffic is allowed from internet to Application VM
- Database is only accessible from Application VM
- Container Registry is private and accessible only from VNet

## Prerequisites

1. **Azure CLI** installed and configured
   ```bash
   # Install Azure CLI (if not installed)
   # Windows: https://aka.ms/installazurecliwindows
   # macOS: brew install azure-cli
   # Linux: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
   
   # Login to Azure
   az login
   
   # Set subscription (if you have multiple)
   az account set --subscription "YOUR_SUBSCRIPTION_ID"
   ```

2. **Terraform** installed (version >= 1.0)
   ```bash
   # Download from: https://www.terraform.io/downloads
   # Or use package manager:
   # Windows: choco install terraform
   # macOS: brew install terraform
   # Linux: https://learn.hashicorp.com/tutorials/terraform/install-cli
   ```

3. **SSH client** (for accessing VMs)

## Quick Start

### 1. Configure Variables

Copy the example variables file and update with your values:

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` and set:
- `my_ip`: Your public IP address (find it at https://www.whatismyip.com/)
  - Format: `"YOUR_IP/32"` (e.g., `"203.0.113.0/32"`)
  - For testing only: `"0.0.0.0/0"` (allows SSH from anywhere - NOT recommended for production)
- `db_admin_username`: Database administrator username
- `db_admin_password`: Strong database password

### 2. Initialize Terraform

```bash
terraform init
```

This downloads the required providers (Azure, TLS).

### 3. Review Plan

```bash
terraform plan
```

Review the planned changes before applying.

### 4. Apply Configuration

```bash
terraform apply
```

Type `yes` when prompted to create the resources. This will take approximately 10-15 minutes.

### 5. Access Outputs

After successful deployment, Terraform will output:
- Bastion Host public IP
- Application VM private IP
- Container Registry URL
- Database connection details
- SSH connection commands

## File Structure

```
terraform/
├── main.tf              # Main configuration with all resources
├── variables.tf         # Input variable definitions
├── outputs.tf           # Output values
├── terraform.tfvars     # Variable values (git-ignored, create from example)
├── terraform.tfvars.example  # Example variables file
└── README.md            # This file
```

## Resource Details

### Virtual Network
- **Address Space**: 10.0.0.0/16 (configurable)
- **Public Subnet**: 10.0.1.0/24 (Bastion Host)
- **Private Subnet**: 10.0.2.0/24 (Application VM and Database)

### Bastion Host
- **VM Size**: Standard_B1s (1 vCPU, 1 GB RAM)
- **OS**: Ubuntu 22.04 LTS
- **Access**: SSH from your IP address only (configurable)

### Application VM
- **VM Size**: Standard_B1s (1 vCPU, 1 GB RAM)
- **OS**: Ubuntu 22.04 LTS
- **Access**: 
  - SSH via Bastion Host only
  - HTTP/HTTPS from internet

### Database
- **Type**: Azure Database for PostgreSQL Flexible Server
- **Version**: PostgreSQL 14
- **SKU**: B_Standard_B1ms (Basic tier, 1 vCore)
- **Storage**: 32 GB (configurable)
- **Access**: Only from Application VM

### Container Registry
- **SKU**: Basic (configurable: Basic, Standard, Premium)
- **Access**: Private, accessible from VNet only

## Network Security Rules

### Public Subnet NSG (Bastion)
- **Allow**: SSH (port 22) from your IP address

### Private Subnet NSG (Application VM)
- **Allow**: HTTP (port 80) from Internet
- **Allow**: HTTPS (port 443) from Internet
- **Allow**: SSH (port 22) from Bastion subnet only
- **Allow**: PostgreSQL (port 5432) from Application VM subnet only

## Accessing the VMs

### Connect to Bastion Host

```bash
# Use the SSH command from terraform output
ssh -i ssh_key.pem azureuser@<BASTION_PUBLIC_IP>
```

Or use the output command:
```bash
terraform output -raw ssh_connection_bastion
```

### Connect to Application VM via Bastion

From your local machine (using SSH jump host):
```bash
ssh -i ssh_key.pem -J azureuser@<BASTION_PUBLIC_IP> azureuser@<APP_VM_PRIVATE_IP>
```

Or use the output command:
```bash
terraform output -raw ssh_connection_app_via_bastion
```

Alternatively, SSH to Bastion first, then SSH to Application VM:
```bash
# On Bastion Host
ssh azureuser@<APP_VM_PRIVATE_IP>
```

## Database Connection

The database is accessible only from the Application VM. To connect:

1. SSH to Application VM via Bastion
2. Install PostgreSQL client (if needed):
   ```bash
   sudo apt-get update
   sudo apt-get install postgresql-client
   ```
3. Connect to database:
   ```bash
   psql -h <DATABASE_HOST> -U <DB_ADMIN_USERNAME> -d postgres
   ```

Database connection details are available in Terraform outputs:
```bash
terraform output database_host
terraform output database_name
```

## Container Registry Usage

### Login to ACR

From Application VM (or any machine with Azure CLI):
```bash
az acr login --name <ACR_NAME>
```

Or using Docker:
```bash
az acr credential show --name <ACR_NAME> --query passwords[0].value
docker login <ACR_URL> -u <ACR_NAME> -p <PASSWORD>
```

### Push Image

```bash
docker tag <IMAGE> <ACR_URL>/<IMAGE>:<TAG>
docker push <ACR_URL>/<IMAGE>:<TAG>
```

Get ACR URL from outputs:
```bash
terraform output container_registry_url
```

## Best Practices

1. **Never commit `terraform.tfvars`** - It may contain sensitive information
2. **Use strong passwords** - Especially for database credentials
3. **Restrict SSH access** - Set `my_ip` to your actual IP, not `0.0.0.0/0`
4. **Regular backups** - Database has 7-day backup retention configured
5. **Monitor costs** - Use Azure Cost Management to track spending
6. **Use tags** - All resources are tagged for organization
7. **Format code** - Run `terraform fmt` before committing

## Formatting and Validation

```bash
# Format Terraform files
terraform fmt

# Validate configuration
terraform validate

# Check for security issues (requires tfsec or checkov)
# tfsec .
# checkov -d .
```

## Troubleshooting

### Error: Azure CLI not found
- Ensure Azure CLI is installed and in PATH
- For Terraform Cloud: Configure Azure CLI in the environment

### Error: Authentication failed
```bash
az login
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

### Error: Insufficient permissions
- Ensure your Azure account has Contributor or Owner role
- Check subscription permissions

### Cannot SSH to Bastion
- Verify `my_ip` is set correctly in `terraform.tfvars`
- Check NSG rules in Azure Portal
- Verify Bastion VM is running

### Cannot access Application VM
- Ensure you're connecting via Bastion Host
- Application VM has no public IP (by design)
- Check NSG rules allow SSH from Bastion subnet

### Database connection issues
- Verify database is in the same VNet/subnet
- Check NSG rules allow port 5432 from Application VM
- Ensure database credentials are correct

## Cost Estimation

Approximate monthly costs (varies by region and usage):
- **Bastion VM (B1s)**: ~$7-10/month
- **Application VM (B1s)**: ~$7-10/month
- **PostgreSQL Flexible Server (B1ms)**: ~$15-20/month
- **Container Registry (Basic)**: ~$5/month
- **VNet, NSGs, Public IPs**: ~$1-2/month

**Total**: Approximately $35-45/month

Use Azure Pricing Calculator for accurate estimates:
https://azure.microsoft.com/pricing/calculator/

## Cleanup

To destroy all resources:

```bash
terraform destroy
```

**Warning**: This will delete all resources. Make sure you have backups!

## Additional Resources

- [Terraform Azure Provider Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Azure Virtual Network Documentation](https://docs.microsoft.com/azure/virtual-network/)
- [Azure Database for PostgreSQL](https://docs.microsoft.com/azure/postgresql/)
- [Azure Container Registry](https://docs.microsoft.com/azure/container-registry/)

## Support

For issues or questions:
1. Check Terraform documentation
2. Review Azure service documentation
3. Check GitHub Issues
4. Contact the DevOps team

---

**Note**: This infrastructure follows security best practices. The Application VM is intentionally not directly accessible from the internet. All access must go through the Bastion Host.
