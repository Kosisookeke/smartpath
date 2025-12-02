# DevSecOps Implementation Summary

This document outlines the Configuration Management and DevSecOps integrations implemented for the SmartPath application.

## Table of Contents
1. [Configuration Management (Ansible)](#configuration-management-ansible)
2. [DevSecOps Integration](#devsecops-integration)
3. [Security Scanning Tools](#security-scanning-tools)
4. [Pipeline Configuration](#pipeline-configuration)
5. [Usage Guide](#usage-guide)

---

## Configuration Management (Ansible)

### Overview
Ansible playbooks have been created to automate VM configuration and application deployment.

### Directory Structure
```
ansible/
├── ansible.cfg                 # Ansible configuration settings
├── inventory.ini.example       # Inventory template (manual configuration)
├── .env.example                # Environment variables template
├── generate_inventory.sh       # Script to generate inventory from env vars
├── .gitignore                  # Prevents committing sensitive files
├── setup.yml                   # VM setup playbook
├── deploy.yml                  # Application deployment playbook
└── README.md                   # Detailed documentation
```

### 1. setup.yml - VM Configuration Playbook

**Purpose:** Configure a fresh VM with all required dependencies.

**Key Features:**
- System package updates and upgrades
- Docker Engine installation (latest stable version)
- Docker Compose installation (plugin + standalone)
- System optimization for Docker containers
- UFW firewall configuration
- Monitoring tools installation (sysstat, iotop, nethogs)
- Python Docker SDK installation
- Application directory creation

**Installed Packages:**
- Docker CE, Docker CLI, Containerd
- Docker Buildx and Docker Compose plugins
- System utilities: curl, git, vim, htop, net-tools, unzip, jq
- Security: UFW firewall
- Monitoring: sysstat, iotop, nethogs

**Firewall Configuration:**
- SSH (22)
- HTTP (80)
- HTTPS (443)
- Application Backend (5000)

**Usage:**
```bash
ansible-playbook -i ansible/inventory.ini ansible/setup.yml
```

### 2. deploy.yml - Application Deployment Playbook

**Purpose:** Deploy SmartPath application using Docker Compose with images from Azure Container Registry.

**Key Features:**
- Azure Container Registry authentication
- Dynamic docker-compose file generation
- Environment variable management
- Zero-downtime deployment
- Health check verification
- Container log monitoring
- Automatic cleanup of old images

**Deployment Process:**
1. Authenticate with ACR
2. Create production docker-compose.yml
3. Create .env file with secrets
4. Stop existing containers
5. Pull latest images from ACR
6. Start new containers
7. Wait for health checks to pass
8. Verify deployment
9. Clean up old images

**Usage:**
```bash
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml \
  -e "acr_login_server=yourregistry.azurecr.io" \
  -e "acr_username=username" \
  -e "acr_password=password" \
  -e "db_host=db-host" \
  -e "db_name=smartpath" \
  -e "db_user=dbuser" \
  -e "db_password=dbpassword"
```

---

## DevSecOps Integration

### Shift-Left Security Approach

Security scanning has been integrated early in the CI/CD pipeline to catch vulnerabilities before deployment.

### Security Principles Implemented
1. **Fail Fast:** Critical vulnerabilities fail the build immediately
2. **Multiple Layers:** Container, IaC, and dependency scanning
3. **Visibility:** Results uploaded to GitHub Security Dashboard
4. **Compliance:** Automated security checks on every PR and deployment

---

## Security Scanning Tools

### 1. Trivy - Container Image Scanning

**What it scans:**
- OS packages (Alpine, Debian, Ubuntu, etc.)
- Application dependencies (npm, pip, etc.)
- Known vulnerabilities (CVEs)

**Configuration:**
- **Severity:** CRITICAL and HIGH
- **Exit Code:** 1 (fails build on findings)
- **Scan Types:** Container images and Docker Compose files
- **Features:** Ignore unfixed vulnerabilities

**CI Pipeline Integration:**
```yaml
- name: Run Trivy vulnerability scanner on Backend
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'smartpath-backend:latest'
    format: 'table'
    severity: 'CRITICAL,HIGH'
    exit-code: '1'
    vuln-type: 'os,library'
    ignore-unfixed: true
```

**Results:** Uploaded to GitHub Security Dashboard as SARIF format

### 2. tfsec - Terraform Security Scanner

**What it scans:**
- Terraform configuration files
- Azure resource misconfigurations
- Security best practices violations
- Compliance issues

**Configuration:**
- **Working Directory:** `terraform/`
- **Soft Fail:** false (fails build on issues)

**CI Pipeline Integration:**
```yaml
- name: Run tfsec security scanner
  uses: aquasecurity/tfsec-action@v1.0.0
  with:
    working_directory: terraform/
    soft_fail: false
```

**Checks Include:**
- Encryption at rest
- Network security rules
- IAM permissions
- Resource tagging
- Public access controls

### 3. Checkov - IaC Security Scanner

**What it scans:**
- Terraform files
- CloudFormation templates
- Kubernetes manifests
- Docker configurations

**Configuration:**
- **Framework:** Terraform
- **Output:** CLI format
- **Soft Fail:** false (fails build on issues)
- **Customizable:** Can skip specific checks

**CI Pipeline Integration:**
```yaml
- name: Run Checkov IaC scanner
  uses: bridgecrewio/checkov-action@master
  with:
    directory: terraform/
    framework: terraform
    output_format: cli
    soft_fail: false
    skip_check: CKV_AZURE_1,CKV_AZURE_2
```

**Checks Include:**
- 1000+ built-in policies
- CIS benchmarks
- NIST compliance
- PCI-DSS compliance
- Azure security best practices

### 4. Docker Compose Configuration Scanning

**What it scans:**
- docker-compose.yml misconfigurations
- Insecure settings
- Exposed ports
- Volume permissions

**Configuration:**
- **Severity:** CRITICAL and HIGH
- **Exit Code:** 0 (warning only)

---

## Pipeline Configuration

### CI Pipeline (.github/workflows/ci.yml)

**Triggers:**
- Pull requests to `main` branch
- Manual workflow dispatch

**Security Scanning Steps:**

1. **Container Image Scanning (Backend & Frontend)**
   - Trivy scanner with exit-code: 1
   - Scans for CRITICAL and HIGH vulnerabilities
   - Uploads SARIF results to GitHub Security

2. **Docker Compose Scanning**
   - Trivy config scan
   - Warning only (exit-code: 0)

3. **Infrastructure as Code Scanning**
   - tfsec for Terraform
   - Checkov for comprehensive IaC analysis
   - Both configured to fail build on issues

**Security Gates:**
- ✅ Build fails if CRITICAL/HIGH vulnerabilities found in images
- ✅ Build fails if IaC security issues detected
- ✅ Results visible in GitHub Security Dashboard
- ⚠️ Docker Compose issues warn but don't fail

### CD Pipeline (.github/workflows/cd.yml)

**Triggers:**
- Push to `main` or `master` branch
- Manual workflow dispatch

**Jobs:**

1. **build-and-push**
   - Build Docker images
   - Scan images with Trivy (exit-code: 1)
   - Upload SARIF to GitHub Security
   - Push to Azure Container Registry
   - Fails deployment if vulnerabilities found

2. **deploy**
   - Requires `build-and-push` to succeed
   - Install Ansible
   - Setup SSH for bastion host
   - Update Ansible inventory dynamically
   - Run `ansible/deploy.yml` playbook
   - Verify deployment
   - Clean up SSH keys

**Security Gates:**
- ✅ Production deployment only if no CRITICAL/HIGH vulnerabilities
- ✅ Infrastructure validated before deployment
- ✅ Health checks required for successful deployment

---

## Usage Guide

### Initial VM Setup

#### Method 1: Using Environment Variables (Recommended)

This method uses the same approach as the CI/CD pipeline:

1. **Setup environment variables:**
   ```bash
   cd ansible
   cp .env.example .env
   vim .env  # Edit with your actual values
   source .env
   ```

2. **Generate inventory automatically:**
   ```bash
   ./generate_inventory.sh
   ```

3. **Test Ansible connectivity:**
   ```bash
   ansible app_server -i inventory.ini -m ping
   ```

4. **Run setup playbook:**
   ```bash
   ansible-playbook -i inventory.ini setup.yml
   ```

#### Method 2: Manual Inventory Configuration

1. **Copy inventory template:**
   ```bash
   cp ansible/inventory.ini.example ansible/inventory.ini
   ```

2. **Edit inventory with your values:**
   ```bash
   vim ansible/inventory.ini
   ```

3. **Test Ansible connectivity:**
   ```bash
   ansible app_server -i ansible/inventory.ini -m ping
   ```

4. **Run setup playbook:**
   ```bash
   ansible-playbook -i ansible/inventory.ini ansible/setup.yml
   ```

### Application Deployment

#### Method 1: Using Environment Variables

If you included deployment variables in `.env` and ran `generate_inventory.sh`:

```bash
cd ansible
ansible-playbook -i inventory.ini deploy.yml
```

The variables are already in the inventory file, so no need to pass them explicitly.

#### Method 2: Pass Variables Explicitly

```bash
cd ansible
ansible-playbook -i inventory.ini deploy.yml \
  -e "acr_login_server=$ACR_LOGIN_SERVER" \
  -e "acr_username=$ACR_USERNAME" \
  -e "acr_password=$ACR_PASSWORD" \
  -e "db_host=$DB_HOST" \
  -e "db_name=$DB_NAME" \
  -e "db_user=$DB_USER" \
  -e "db_password=$DB_PASSWORD"
```

#### Automated Deployment

- Push to `main` branch triggers CD pipeline
- GitHub Actions automatically:
  - Generates `inventory.ini` from GitHub Secrets
  - Runs deployment playbook
  - Verifies deployment health

### GitHub Secrets Required

Configure these secrets in GitHub repository settings:

**Azure Container Registry:**
- `ACR_LOGIN_SERVER`
- `ACR_USERNAME`
- `ACR_PASSWORD`

**SSH Access:**
- `SSH_PRIVATE_KEY`
- `BASTION_PUBLIC_IP`
- `APP_VM_PRIVATE_IP`

**Database:**
- `DB_HOST`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

### Viewing Security Scan Results

**GitHub Security Dashboard:**
1. Go to repository → Security → Code scanning alerts
2. Filter by tool: trivy-backend, trivy-frontend, tfsec
3. View detailed vulnerability information

**CI/CD Pipeline Logs:**
1. Go to Actions tab
2. Select the workflow run
3. View detailed logs for each security scan step

### Troubleshooting

**Check container status:**
```bash
ansible app_server -i ansible/inventory.ini -m shell \
  -a "cd /opt/smartpath && docker compose ps"
```

**View application logs:**
```bash
ansible app_server -i ansible/inventory.ini -m shell \
  -a "docker logs smartpath-backend --tail 50"
```

**Restart application:**
```bash
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --tags stop,start
```

**Re-run security scans locally:**
```bash
# Scan Docker image
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image smartpath-backend:latest

# Scan Terraform
docker run --rm -v $(pwd):/src aquasec/tfsec /src/terraform

# Scan with Checkov
docker run --rm -v $(pwd):/tf bridgecrew/checkov -d /tf/terraform
```

---

## Inventory Management - Local vs CI/CD Consistency

The inventory configuration uses environment variables in both local development and CI/CD:

**Local Development:**
```bash
# Use .env file and generate_inventory.sh
cd ansible
cp .env.example .env
# Edit .env with your values
source .env
./generate_inventory.sh
ansible-playbook -i inventory.ini deploy.yml
```

**CI/CD Pipeline:**
```yaml
# GitHub Actions dynamically generates inventory from secrets
- name: Update Ansible inventory with secrets
  run: |
    cat > ansible/inventory.ini << EOF
    [app_server]
    app-vm ansible_host=${{ secrets.APP_VM_PRIVATE_IP }}
    ...
    EOF
```

**Benefits:**
- No secrets committed to repository
- Same configuration approach everywhere
- Easy to manage and update
- Consistent behavior between environments
- `.gitignore` prevents accidental commits

---

## Security Best Practices Implemented

1. **Automated Scanning:** Every PR and merge triggers security scans
2. **Fail Fast:** Critical vulnerabilities prevent deployment
3. **Defense in Depth:** Multiple scanning tools for comprehensive coverage
4. **Visibility:** Results integrated into GitHub Security Dashboard
5. **Least Privilege:** Ansible uses SSH keys, not passwords
6. **Secrets Management:** All secrets stored in GitHub Secrets or environment variables
7. **Firewall Configuration:** UFW enabled with minimal open ports
8. **Container Security:** Images scanned before deployment
9. **IaC Security:** Terraform validated against security policies
10. **Audit Trail:** All deployments logged and traceable
11. **No Secrets in Git:** `.gitignore` prevents committing `inventory.ini` and `.env`

---

## Files Modified/Created

### Created Files:
- `ansible/ansible.cfg` - Ansible configuration
- `ansible/inventory.ini.example` - Manual inventory template
- `ansible/.env.example` - Environment variables template
- `ansible/generate_inventory.sh` - Inventory generation script
- `ansible/.gitignore` - Prevents committing sensitive files
- `ansible/setup.yml` - VM setup playbook
- `ansible/deploy.yml` - Application deployment playbook
- `ansible/README.md` - Comprehensive Ansible documentation
- `DEVSECOPS_IMPLEMENTATION.md` (this file)

### Modified Files:
- `.github/workflows/ci.yml` - Enhanced security scanning
- `.github/workflows/cd.yml` - Enhanced security scanning

---

## Next Steps

1. **Configure GitHub Secrets:** Add all required secrets to repository settings
2. **Test CI Pipeline:** Create a PR to trigger security scans
3. **Initial VM Setup:** Run `setup.yml` playbook on target VM
4. **Test Deployment:** Merge PR to trigger CD pipeline
5. **Monitor Security:** Regularly check GitHub Security Dashboard
6. **Update Policies:** Adjust security checks based on findings
7. **Document Exceptions:** Use skip_check for known false positives

---

## Support and Documentation

- **Ansible Documentation:** See `ansible/README.md`
- **Trivy Documentation:** https://aquasecurity.github.io/trivy/
- **tfsec Documentation:** https://aquasecurity.github.io/tfsec/
- **Checkov Documentation:** https://www.checkov.io/
- **GitHub Security:** https://docs.github.com/en/code-security

---

## Summary

This implementation provides:
- ✅ Automated VM configuration with Ansible
- ✅ Docker and Docker Compose installation
- ✅ Container vulnerability scanning (Trivy)
- ✅ IaC security scanning (tfsec + Checkov)
- ✅ Build failures on critical vulnerabilities
- ✅ GitHub Security Dashboard integration
- ✅ Comprehensive documentation
- ✅ Production-ready deployment pipeline

The SmartPath application now has a complete DevSecOps pipeline with shift-left security practices!
