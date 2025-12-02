# Troubleshooting Guide - SmartPath Deployment

This guide helps you resolve common issues with the SmartPath CI/CD pipeline and Ansible deployments.

## Table of Contents
1. [SSH Connection Issues](#ssh-connection-issues)
2. [GitHub Actions Failures](#github-actions-failures)
3. [Ansible Connection Problems](#ansible-connection-problems)
4. [Deployment Failures](#deployment-failures)
5. [Security Scan Failures](#security-scan-failures)

---

## SSH Connection Issues

### Error: "Process completed with exit code 1" during SSH Setup

**Symptoms:**
- CD pipeline fails at "Setup SSH" step
- Error shows `exit code 1`
- SSH-related commands failing

**Possible Causes & Solutions:**

#### 1. Missing GitHub Secrets

**Check if all secrets are set:**

Go to GitHub Repository → Settings → Secrets and variables → Actions

Required secrets:
- `SSH_PRIVATE_KEY` - Your SSH private key (complete key including headers)
- `BASTION_PUBLIC_IP` - Public IP of your bastion host
- `APP_VM_PRIVATE_IP` - Private IP of your application VM
- `ACR_LOGIN_SERVER` - Azure Container Registry URL
- `ACR_USERNAME` - ACR username
- `ACR_PASSWORD` - ACR password
- `DB_HOST` - Database host
- `DB_NAME` - Database name
- `DB_USER` - Database username
- `DB_PASSWORD` - Database password

**How to set SSH_PRIVATE_KEY:**

```bash
# On your local machine, get your private key
cat ~/.ssh/id_rsa

# Copy the ENTIRE output including:
# -----BEGIN OPENSSH PRIVATE KEY-----
# (all the key content)
# -----END OPENSSH PRIVATE KEY-----

# Paste this into the SSH_PRIVATE_KEY secret in GitHub
```

**Important:** Make sure to include the BEGIN and END lines!

#### 2. SSH Key Format Issues

**Symptoms:**
- Error: "SSH_PRIVATE_KEY is not a valid SSH private key"

**Solution:**

The key must be in OpenSSH format. If you have an older key format:

```bash
# Convert to OpenSSH format
ssh-keygen -p -f ~/.ssh/id_rsa -m pem -P "" -N ""

# Or generate a new key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
```

Then copy the key to GitHub Secrets.

#### 3. Bastion Host Unreachable

**Symptoms:**
- Error during `ssh-keyscan` for bastion host
- Can't connect to bastion IP

**Solutions:**

1. **Verify bastion IP is correct:**
   ```bash
   # Test from your local machine
   ping <BASTION_PUBLIC_IP>
   ssh azureuser@<BASTION_PUBLIC_IP>
   ```

2. **Check Azure Network Security Group:**
   - Ensure SSH (port 22) is open to GitHub Actions IPs
   - Or open to 0.0.0.0/0 (less secure but works)

3. **Check if bastion VM is running:**
   - Go to Azure Portal
   - Check VM status
   - Start if stopped

4. **Verify DNS resolution:**
   - Use IP address instead of hostname in secrets

#### 4. SSH Key Not Authorized on Servers

**Symptoms:**
- SSH setup succeeds but Ansible ping fails
- "Permission denied (publickey)"

**Solution:**

Ensure the public key is in `~/.ssh/authorized_keys` on both:
1. Bastion host
2. Application VM

```bash
# On your local machine, get public key
cat ~/.ssh/id_rsa.pub

# SSH to bastion and app VM, then add to authorized_keys
echo "your-public-key-here" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

---

## GitHub Actions Failures

### CI Pipeline Fails on Security Scans

**Symptoms:**
- Trivy fails with CRITICAL/HIGH vulnerabilities
- tfsec or Checkov fails on IaC issues

**Expected Behavior:**
The pipeline is configured to **fail on critical vulnerabilities** (shift-left security).

**Solutions:**

#### Option 1: Fix the Vulnerabilities (Recommended)

1. **Review the scan results:**
   - Go to GitHub Security tab
   - Check "Code scanning alerts"
   - Review each vulnerability

2. **Update dependencies:**
   ```bash
   # For backend (Python)
   cd backend
   pip install --upgrade <package-name>
   pip freeze > requirements.txt

   # For frontend (Node.js)
   cd frontend
   npm audit fix
   npm update
   ```

3. **Update base images:**
   ```dockerfile
   # In backend/Dockerfile and frontend/Dockerfile
   # Use newer base images
   FROM python:3.11-slim  # Use latest patch version
   FROM node:18-alpine    # Use latest LTS
   ```

4. **Fix IaC issues:**
   - Review tfsec/Checkov output
   - Update Terraform configurations
   - Add required security settings

#### Option 2: Temporarily Allow Vulnerabilities (Not Recommended)

Only use this for testing or if vulnerabilities are false positives:

Edit `.github/workflows/ci.yml`:

```yaml
# Change exit-code from 1 to 0
- name: Run Trivy vulnerability scanner on Backend
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'smartpath-backend:latest'
    exit-code: '0'  # Changed from 1 to 0
```

### CD Pipeline Fails During Deployment

**Symptoms:**
- Build succeeds but deployment fails
- Ansible playbook errors

**Solutions:**

See [Ansible Connection Problems](#ansible-connection-problems) and [Deployment Failures](#deployment-failures) sections.

---

## Ansible Connection Problems

### Ansible Ping Fails

**Symptoms:**
- "UNREACHABLE" error
- "Failed to connect to the host via ssh"

**Diagnostic Steps:**

1. **Test SSH manually from GitHub Actions runner:**

   Add a temporary debug step to `.github/workflows/cd.yml`:

   ```yaml
   - name: Debug SSH
     run: |
       ssh -vvv -o ProxyCommand="ssh -W %h:%p -i ~/.ssh/id_rsa azureuser@${{ secrets.BASTION_PUBLIC_IP }}" \
         azureuser@${{ secrets.APP_VM_PRIVATE_IP }} "echo 'Connection successful'"
   ```

2. **Check bastion SSH forwarding:**

   SSH to your bastion host and verify `/etc/ssh/sshd_config`:

   ```bash
   AllowTcpForwarding yes
   PermitTunnel yes
   ```

   Restart SSH if changed:
   ```bash
   sudo systemctl restart sshd
   ```

3. **Verify app VM is accessible from bastion:**

   ```bash
   # SSH to bastion
   ssh azureuser@<BASTION_PUBLIC_IP>

   # From bastion, try to reach app VM
   ping <APP_VM_PRIVATE_IP>
   ssh azureuser@<APP_VM_PRIVATE_IP>
   ```

### Ansible "Authentication failed"

**Solution:**

Ensure the same SSH key is authorized on both bastion and app VM:

```bash
# Copy public key to both servers
ssh-copy-id -i ~/.ssh/id_rsa.pub azureuser@<BASTION_PUBLIC_IP>

# Then from bastion:
ssh-copy-id -i ~/.ssh/id_rsa.pub azureuser@<APP_VM_PRIVATE_IP>
```

---

## Deployment Failures

### Docker Compose Fails to Start

**Symptoms:**
- Containers fail to start
- "Unhealthy" status
- Health checks failing

**Solutions:**

1. **Check container logs:**
   ```bash
   ansible app_server -i ansible/inventory.ini -m shell \
     -a "docker logs smartpath-backend --tail 100"

   ansible app_server -i ansible/inventory.ini -m shell \
     -a "docker logs smartpath-frontend --tail 100"
   ```

2. **Check if ports are already in use:**
   ```bash
   ansible app_server -i ansible/inventory.ini -m shell \
     -a "netstat -tulpn | grep -E ':(80|443|5000)'"
   ```

3. **Verify ACR authentication:**
   ```bash
   # Test ACR login manually
   ansible app_server -i ansible/inventory.ini -m shell \
     -a "docker login ${{ secrets.ACR_LOGIN_SERVER }} -u ${{ secrets.ACR_USERNAME }} -p ${{ secrets.ACR_PASSWORD }}"
   ```

### Database Connection Fails

**Symptoms:**
- Backend logs show database errors
- "Could not connect to database"

**Solutions:**

1. **Verify database secrets:**
   - Check DB_HOST, DB_NAME, DB_USER, DB_PASSWORD are correct

2. **Test database connection:**
   ```bash
   # From app VM
   ansible app_server -i ansible/inventory.ini -m shell \
     -a "nc -zv <DB_HOST> 5432"
   ```

3. **Check Azure PostgreSQL firewall rules:**
   - Add app VM's IP to allowed IPs
   - Or enable "Allow Azure services"

---

## Security Scan Failures

### Trivy Scans Fail

**Common Issues:**

1. **Trivy database update fails:**
   - Usually transient network issues
   - Retry the pipeline

2. **Too many vulnerabilities:**
   - Review and fix critical issues
   - Update base images and dependencies

3. **False positives:**
   - Add to skip list if confirmed false positive:
     ```yaml
     trivyignores: |
       CVE-2021-1234
     ```

### tfsec or Checkov Fails

**Common Issues:**

1. **Missing encryption:**
   - Enable encryption at rest for storage accounts
   - Use HTTPS-only for web apps

2. **Network security:**
   - Configure NSG rules properly
   - Don't expose unnecessary ports

3. **Skip specific checks (if needed):**
   ```yaml
   - name: Run Checkov IaC scanner
     uses: bridgecrewio/checkov-action@master
     with:
       skip_check: CKV_AZURE_1,CKV_AZURE_2
   ```

---

## Quick Diagnostic Commands

### Check Pipeline Status

```bash
# View recent Actions runs
gh run list

# View specific run details
gh run view <run-id>

# View logs for a specific job
gh run view <run-id> --log
```

### Check Ansible Connectivity

```bash
# From your local machine (after setting up .env)
cd ansible
source .env
./generate_inventory.sh
ansible app_server -i inventory.ini -m ping -vvv
```

### Check VM Status

```bash
# SSH to bastion
ssh azureuser@<BASTION_PUBLIC_IP>

# From bastion, SSH to app VM
ssh azureuser@<APP_VM_PRIVATE_IP>

# Check Docker status
sudo systemctl status docker
docker ps
docker compose -f /opt/smartpath/docker-compose.prod.yml ps
```

### Check Application Health

```bash
# Backend health check
curl http://<APP_VM_IP>:5000/api/health

# Frontend health check
curl http://<APP_VM_IP>/

# Check logs
docker logs smartpath-backend --tail 50
docker logs smartpath-frontend --tail 50
```

---

## Getting Help

If you're still having issues:

1. **Check GitHub Actions logs:**
   - Go to Actions tab
   - Click on failed run
   - Review detailed logs for each step

2. **Enable verbose Ansible output:**
   Add `-vvv` flag to ansible commands for detailed debugging

3. **Check Azure Portal:**
   - VM status and network settings
   - NSG rules
   - Database firewall rules

4. **Review recent changes:**
   - What changed since last successful deployment?
   - New dependencies or configuration?

5. **Test components individually:**
   - Test SSH connectivity first
   - Test Ansible ping
   - Test manual Docker commands
   - Then try full deployment

---

## Common Error Messages and Solutions

| Error Message | Solution |
|--------------|----------|
| "SSH_PRIVATE_KEY secret is not set" | Add SSH_PRIVATE_KEY to GitHub Secrets |
| "Permission denied (publickey)" | Add public key to authorized_keys on servers |
| "UNREACHABLE" (Ansible) | Check SSH connectivity and bastion forwarding |
| "exit code 1" (SSH setup) | Check if secrets are valid and correctly formatted |
| "Could not scan bastion host key" | Verify bastion IP and firewall rules |
| "Unhealthy" (Docker) | Check container logs and health check configuration |
| "Failed to connect to database" | Verify DB credentials and firewall rules |
| "Trivy scan failed" | Review vulnerabilities and update dependencies |
| "tfsec found issues" | Fix Terraform security misconfigurations |

---

## Prevention Tips

1. **Test locally first:**
   - Use ansible playbooks locally before pushing
   - Test with `./generate_inventory.sh`

2. **Keep secrets updated:**
   - Rotate SSH keys periodically
   - Update GitHub Secrets when credentials change

3. **Monitor security scans:**
   - Review GitHub Security Dashboard regularly
   - Fix vulnerabilities promptly

4. **Document changes:**
   - Keep track of infrastructure changes
   - Document any manual configurations

5. **Use staging environment:**
   - Test deployments in staging before production
   - Validate security scans pass
