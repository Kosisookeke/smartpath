# Ansible Quick Start Guide

## 🚀 Quick Test (Local)

### Prerequisites
1. Ansible installed: `pip install ansible` or `brew install ansible`
2. SSH key at `../terraform/ssh_key.pem`
3. Terraform outputs available

### Step 1: Get Terraform Outputs
```bash
cd terraform
terraform output
```

### Step 2: Update Inventory
Edit `ansible/inventory.ini` with your values:
- `ansible_host`: App VM private IP
- `ansible_ssh_common_args`: Bastion public IP

### Step 3: Test Connection
```bash
cd ansible
ansible app_server -i inventory.ini -m ping
```

### Step 4: Run Playbook
```bash
ansible-playbook deploy.yml \
  -e "acr_login_server=smartpathacruepjie.azurecr.io" \
  -e "acr_username=smartpathacruepjie" \
  -e "acr_password=<your-acr-password>" \
  -e "db_host=smartpath-db-19m303.postgres.database.azure.com" \
  -e "db_name=smartpath-db-19m303" \
  -e "db_user=dbadmin" \
  -e "db_password=<your-db-password>"
```

## 🔍 Verify Deployment

```bash
# Check containers
ansible app_server -i inventory.ini -m shell -a "cd /opt/smartpath && docker compose ps"

# Check logs
ansible app_server -i inventory.ini -m shell -a "cd /opt/smartpath && docker compose logs backend"
ansible app_server -i inventory.ini -m shell -a "cd /opt/smartpath && docker compose logs frontend"
```

## 📝 Common Commands

```bash
# Dry run (check mode)
ansible-playbook deploy.yml --check --diff

# Verbose output
ansible-playbook deploy.yml -v

# Run specific task
ansible-playbook deploy.yml --tags "docker"

# Skip specific task
ansible-playbook deploy.yml --skip-tags "verify"
```

