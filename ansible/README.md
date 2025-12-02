# Ansible Configuration Management for SmartPath

This directory contains Ansible playbooks for configuring and deploying the SmartPath application.

## Directory Structure

```
ansible/
├── ansible.cfg              # Ansible configuration
├── inventory.ini.example    # Inventory template
├── setup.yml               # VM setup playbook (Docker, packages)
├── deploy.yml              # Application deployment playbook
└── README.md               # This file
```

## Prerequisites

1. Ansible installed on your local machine or CI/CD runner
2. SSH access to the target VM
3. SSH private key configured
4. Azure Container Registry credentials

## Playbooks

### 1. setup.yml - Initial VM Configuration

Sets up a fresh VM with all required dependencies.

**What it does:**
- Updates system packages
- Installs Docker Engine and Docker Compose
- Installs required system packages (curl, git, vim, etc.)
- Configures firewall (UFW)
- Creates application directory
- Installs monitoring tools
- Optimizes system settings

**Usage:**
```bash
# Run the full setup
ansible-playbook -i inventory.ini setup.yml

# Run specific tags only
ansible-playbook -i inventory.ini setup.yml --tags docker
ansible-playbook -i inventory.ini setup.yml --tags system,packages
```

**Available tags:**
- `system` - System updates and configuration
- `packages` - Package installation
- `docker` - Docker installation
- `docker-compose` - Docker Compose installation
- `security` - Security configuration (firewall)
- `app` - Application directory setup
- `monitoring` - Monitoring tools installation
- `verify` - Verification steps

### 2. deploy.yml - Application Deployment

Deploys the SmartPath application using Docker Compose.

**What it does:**
- Logs in to Azure Container Registry
- Creates production docker-compose file
- Pulls latest images from ACR
- Stops existing containers
- Starts new containers
- Verifies deployment health
- Cleans up old images

**Usage:**
```bash
# Deploy with required variables
ansible-playbook -i inventory.ini deploy.yml \
  -e "acr_login_server=yourregistry.azurecr.io" \
  -e "acr_username=your-username" \
  -e "acr_password=your-password" \
  -e "db_host=your-db-host" \
  -e "db_name=smartpath" \
  -e "db_user=your-db-user" \
  -e "db_password=your-db-password"

# Deploy with specific tags
ansible-playbook -i inventory.ini deploy.yml --tags deploy,verify
```

**Available tags:**
- `deploy` - All deployment steps
- `setup` - Directory setup
- `acr` - ACR login
- `config` - Configuration file creation
- `pull` - Pull Docker images
- `start` - Start containers
- `stop` - Stop containers
- `verify` - Deployment verification
- `cleanup` - Clean up old images

## Getting Started

### Two Ways to Configure Inventory

You can configure your Ansible inventory in two ways:

#### Option 1: Using Environment Variables (Recommended)

This approach uses the same method as the CI/CD pipeline and keeps secrets out of files.

```bash
# 1. Copy the environment template
cp .env.example .env

# 2. Edit .env with your actual values
vim .env

# 3. Source the environment variables
source .env

# 4. Generate inventory.ini automatically
./generate_inventory.sh
```

The script will validate required variables and create `inventory.ini` automatically.

#### Option 2: Manual Inventory File

For quick testing or if you prefer manual configuration:

```bash
# Copy the example inventory
cp inventory.ini.example inventory.ini

# Edit with your values
vim inventory.ini
```

**Note:** `inventory.ini` and `.env` are in `.gitignore` to prevent committing secrets.

### 1. Setup Environment Variables

```bash
# Required variables
export APP_VM_PRIVATE_IP="10.0.2.4"
export BASTION_PUBLIC_IP="20.x.x.x"

# For deployment (optional for setup.yml)
export ACR_LOGIN_SERVER="yourregistry.azurecr.io"
export ACR_USERNAME="your-username"
export ACR_PASSWORD="your-password"
export DB_HOST="your-db-host"
export DB_NAME="smartpath"
export DB_USER="your-db-user"
export DB_PASSWORD="your-db-password"

# Generate inventory
./generate_inventory.sh
```

### 2. Test Connection

```bash
# Test Ansible can connect to your server
ansible app_server -i inventory.ini -m ping
```

### 3. Setup VM (First Time Only)

```bash
# Run the setup playbook
ansible-playbook -i inventory.ini setup.yml
```

### 4. Deploy Application

If you used `generate_inventory.sh` with all deployment variables in `.env`, simply run:

```bash
# Deploy with variables from inventory
ansible-playbook -i inventory.ini deploy.yml
```

Or pass variables explicitly:

```bash
# Deploy with explicit variables
ansible-playbook -i inventory.ini deploy.yml \
  -e "acr_login_server=$ACR_LOGIN_SERVER" \
  -e "acr_username=$ACR_USERNAME" \
  -e "acr_password=$ACR_PASSWORD" \
  -e "db_host=$DB_HOST" \
  -e "db_name=$DB_NAME" \
  -e "db_user=$DB_USER" \
  -e "db_password=$DB_PASSWORD"
```

## CI/CD Integration

The playbooks are integrated into GitHub Actions workflows:

- **CD Pipeline** (`.github/workflows/cd.yml`): Automatically runs `deploy.yml` when code is merged to main
- **Manual Setup**: Run `setup.yml` manually for initial VM configuration

### How CI/CD Uses Inventory

The CD pipeline dynamically generates `inventory.ini` from GitHub Secrets during deployment:

```yaml
- name: Update Ansible inventory with secrets
  run: |
    cat > ansible/inventory.ini << EOF
    [app_server]
    app-vm ansible_host=${{ secrets.APP_VM_PRIVATE_IP }}

    [app_server:vars]
    ansible_user=azureuser
    ansible_ssh_private_key_file=~/.ssh/id_rsa
    ansible_ssh_common_args='-o ProxyCommand="ssh -W %h:%p -q -i ~/.ssh/id_rsa azureuser@${{ secrets.BASTION_PUBLIC_IP }}"'
    ansible_python_interpreter=/usr/bin/python3
    EOF
```

This is the same approach used by `generate_inventory.sh` for local development, ensuring consistency between local and CI/CD environments.

## Bastion Host / Jump Server

If your VM is behind a bastion host, configure SSH proxy in `inventory.ini`:

```ini
ansible_ssh_common_args='-o ProxyCommand="ssh -W %h:%p -q -i ~/.ssh/id_rsa azureuser@BASTION_IP"'
```

## Troubleshooting

### Check Ansible connectivity
```bash
ansible app_server -i inventory.ini -m ping
```

### View running containers
```bash
ansible app_server -i inventory.ini -m shell -a "cd /opt/smartpath && docker compose ps"
```

### Check application logs
```bash
ansible app_server -i inventory.ini -m shell -a "docker logs smartpath-backend --tail 50"
ansible app_server -i inventory.ini -m shell -a "docker logs smartpath-frontend --tail 50"
```

### Restart application
```bash
ansible-playbook -i inventory.ini deploy.yml --tags stop,start
```

## Security Notes

- Store sensitive variables in GitHub Secrets or Ansible Vault
- Never commit `inventory.ini` with real credentials to version control
- Use SSH key authentication, not passwords
- Firewall is configured to allow only necessary ports (22, 80, 443, 5000)

## Variables

### Required Variables (deploy.yml)
- `acr_login_server`: Azure Container Registry URL
- `acr_username`: ACR username
- `acr_password`: ACR password
- `db_host`: Database host
- `db_name`: Database name
- `db_user`: Database user
- `db_password`: Database password

### Optional Variables
- `app_directory`: Application directory (default: `/opt/smartpath`)
- `docker_compose_version`: Docker Compose version (default: `2.24.0`)
