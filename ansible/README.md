# Ansible Configuration Management for SmartPath

This directory contains Ansible playbooks and configuration files for deploying and managing the SmartPath application infrastructure.

## 📁 Directory Structure

```
ansible/
├── deploy.yml              # Main deployment playbook
├── inventory.ini           # Ansible inventory file
├── ansible.cfg             # Ansible configuration
├── docker-compose.yml.j2   # Docker Compose template
├── .env.j2                 # Environment variables template
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Ansible installed** (version 2.9+)
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install ansible

   # macOS
   brew install ansible

   # Or via pip
   pip install ansible
   ```

2. **SSH access configured**
   - SSH private key at `../terraform/ssh_key.pem`
   - Bastion host accessible
   - App VM accessible via bastion

3. **Terraform outputs available**
   - Get values from `terraform output` command

### Running the Playbook

1. **Update inventory.ini** with your infrastructure details:
   ```ini
   [app_server]
   app-vm ansible_host=<app-vm-private-ip>

   [app_server:vars]
   ansible_user=azureuser
   ansible_ssh_private_key_file=../terraform/ssh_key.pem
   ansible_ssh_common_args='-o ProxyCommand="ssh -W %h:%p -q -i ../terraform/ssh_key.pem azureuser@<bastion-public-ip>"'
   ```

2. **Get Terraform outputs**:
   ```bash
   cd terraform
   terraform output
   ```

3. **Run the playbook** with required variables:
   ```bash
   cd ansible
   ansible-playbook deploy.yml \
     -e "acr_login_server=$(cd ../terraform && terraform output -raw container_registry_url)" \
     -e "acr_username=$(cd ../terraform && terraform output -raw acr_username)" \
     -e "acr_password=$(cd ../terraform && terraform output -raw acr_password)" \
     -e "db_host=$(cd ../terraform && terraform output -raw database_host)" \
     -e "db_name=$(cd ../terraform && terraform output -raw database_name)" \
     -e "db_user=dbadmin" \
     -e "db_password=<your-db-password>"
   ```

   Or use environment variables:
   ```bash
   export ACR_LOGIN_SERVER=$(cd ../terraform && terraform output -raw container_registry_url)
   export ACR_USERNAME=$(cd ../terraform && terraform output -raw acr_username)
   export ACR_PASSWORD=$(cd ../terraform && terraform output -raw acr_password)
   export DB_HOST=$(cd ../terraform && terraform output -raw database_host)
   export DB_NAME=$(cd ../terraform && terraform output -raw database_name)
   export DB_PASSWORD=<your-db-password>

   ansible-playbook deploy.yml \
     -e "acr_login_server=$ACR_LOGIN_SERVER" \
     -e "acr_username=$ACR_USERNAME" \
     -e "acr_password=$ACR_PASSWORD" \
     -e "db_host=$DB_HOST" \
     -e "db_name=$DB_NAME" \
     -e "db_password=$DB_PASSWORD"
   ```

## 📋 Playbook Tasks

The `deploy.yml` playbook performs the following tasks:

1. **System Package Installation**
   - Updates apt cache
   - Installs git, curl, wget, and other essential packages

2. **Docker Installation**
   - Adds Docker GPG key and repository
   - Installs Docker CE and Docker Compose
   - Starts and enables Docker service
   - Adds user to docker group

3. **ACR Authentication**
   - Logs into Azure Container Registry
   - Pulls latest Docker images

4. **Application Deployment**
   - Creates application directory (`/opt/smartpath`)
   - Generates `docker-compose.yml` from template
   - Generates `.env` file with database configuration
   - Pulls latest images
   - Deploys application using `docker-compose up -d`

5. **Verification**
   - Checks Docker and Docker Compose versions
   - Verifies containers are running

## 🔧 Configuration Files

### inventory.ini

Defines the target hosts and connection settings. Key variables:
- `ansible_host`: Private IP of the app VM
- `ansible_user`: SSH username (azureuser)
- `ansible_ssh_private_key_file`: Path to SSH private key
- `ansible_ssh_common_args`: ProxyCommand for bastion host access

### docker-compose.yml.j2

Jinja2 template for Docker Compose configuration. Defines:
- Backend service (port 5000)
- Frontend service (port 3000)
- Network configuration
- Health checks

### .env.j2

Jinja2 template for environment variables. Includes:
- Database connection details
- Application configuration
- Security settings

## 🔐 Security Best Practices

1. **Never commit sensitive data**
   - Pass passwords via `-e` flag or environment variables
   - Use `no_log: true` in playbooks for sensitive tasks

2. **SSH Key Management**
   - Keep `ssh_key.pem` secure
   - Use proper file permissions (600)
   - Rotate keys regularly

3. **ACR Credentials**
   - Store in GitHub Secrets for CI/CD
   - Never hardcode in playbooks

## 🧪 Testing

### Test SSH Connection

```bash
# Test bastion connection
ssh -i ../terraform/ssh_key.pem azureuser@<bastion-ip>

# Test app VM via bastion
ssh -i ../terraform/ssh_key.pem -J azureuser@<bastion-ip> azureuser@<app-vm-private-ip>
```

### Test Ansible Connection

```bash
ansible app_server -i inventory.ini -m ping
```

### Dry Run

```bash
ansible-playbook deploy.yml --check --diff
```

## 🐛 Troubleshooting

### SSH Connection Issues

**Problem**: Cannot connect to app VM
```bash
# Verify bastion is accessible
ssh -i ../terraform/ssh_key.pem azureuser@<bastion-ip>

# Check inventory.ini ProxyCommand syntax
# Ensure SSH key path is correct
```

### Docker Installation Fails

**Problem**: Docker installation errors
```bash
# Manually test on VM
ansible app_server -i inventory.ini -m shell -a "sudo apt-get update"
ansible app_server -i inventory.ini -m shell -a "docker --version"
```

### ACR Authentication Fails

**Problem**: Cannot pull images
```bash
# Verify credentials
ansible app_server -i inventory.ini -m shell -a "echo $ACR_PASSWORD | docker login smartpathacruepjie.azurecr.io -u smartpathacruepjie --password-stdin"
```

### Containers Not Starting

**Problem**: Docker Compose fails
```bash
# Check logs
ansible app_server -i inventory.ini -m shell -a "cd /opt/smartpath && docker compose logs"
```

## 📚 Additional Resources

- [Ansible Documentation](https://docs.ansible.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Azure Container Registry](https://docs.microsoft.com/azure/container-registry/)

## 🔄 Integration with CI/CD

This playbook is designed to be called from GitHub Actions CD pipeline:

```yaml
- name: Deploy to Production
  run: |
    cd ansible
    ansible-playbook deploy.yml \
      -e "acr_login_server=${{ secrets.ACR_LOGIN_SERVER }}" \
      -e "acr_username=${{ secrets.ACR_USERNAME }}" \
      -e "acr_password=${{ secrets.ACR_PASSWORD }}" \
      -e "db_host=${{ secrets.DB_HOST }}" \
      -e "db_name=${{ secrets.DB_NAME }}" \
      -e "db_password=${{ secrets.DB_PASSWORD }}"
```

## 📝 Notes

- The playbook uses `become: yes` to run tasks with sudo privileges
- Docker Compose is installed both as a plugin and standalone binary
- Health checks are configured for both frontend and backend services
- The application directory is created at `/opt/smartpath`

