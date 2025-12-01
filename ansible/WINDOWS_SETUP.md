# Running Ansible on Windows

Ansible has compatibility issues with Python 3.13 on Windows. Here are your options:

## Option 1: Use WSL (Recommended)

### Step 1: Access WSL
```powershell
wsl
```

### Step 2: Install Ansible in WSL
```bash
sudo apt-get update
sudo apt-get install -y python3-pip
pip3 install ansible
```

### Step 3: Navigate to your project
```bash
cd /mnt/c/Users/USER/smartpath/ansible
```

### Step 4: Run Ansible playbook
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

## Option 2: Use Docker

### Run Ansible in a Docker container:
```powershell
docker run --rm -it `
  -v ${PWD}:/ansible `
  -v ${PWD}/../terraform/ssh_key.pem:/root/.ssh/id_rsa:ro `
  -w /ansible `
  cytopia/ansible:latest `
  ansible-playbook deploy.yml `
  -e "acr_login_server=smartpathacruepjie.azurecr.io" `
  -e "acr_username=smartpathacruepjie" `
  -e "acr_password=<your-acr-password>" `
  -e "db_host=smartpath-db-19m303.postgres.database.azure.com" `
  -e "db_name=smartpath-db-19m303" `
  -e "db_user=dbadmin" `
  -e "db_password=<your-db-password>"
```

## Option 3: Use GitHub Actions CD Pipeline (Easiest)

The CD pipeline will automatically run Ansible when you:
1. Merge to `main` branch, OR
2. Manually trigger the workflow

No local setup needed! Just ensure all GitHub Secrets are configured.

## Quick Test via CD Pipeline

1. Go to your GitHub repository
2. Click **Actions** tab
3. Select **CD Pipeline - Deploy to Production**
4. Click **Run workflow** → **Run workflow**
5. The pipeline will build images and deploy using Ansible automatically

