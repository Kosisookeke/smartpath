# GitHub Actions & ACR Setup Guide

This guide walks you through setting up the CI pipeline to automatically build and push Docker images to Azure Container Registry (ACR).

## Prerequisites

1. ✅ Terraform infrastructure deployed (ACR already created)
2. ✅ GitHub repository set up
3. ✅ Azure CLI authenticated (`az login`)

## Step 1: Get ACR Credentials from Terraform

After running `terraform apply`, get your ACR credentials:

```bash
cd terraform

# Get the ACR login server URL
terraform output container_registry_url

# Get the ACR username
terraform output acr_username

# Get the ACR password (sensitive)
terraform output -raw acr_password
```

**Example output:**
```
container_registry_url = "smartpathacr12345.azurecr.io"
acr_username = "smartpathacr12345"
acr_password = "AbCdEfGhIjKlMnOpQrStUvWxYz1234567890"
```

## Step 2: Add GitHub Secrets

1. Go to your GitHub repository: `https://github.com/YOUR_USERNAME/smartpath`
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add these three secrets:

### Secret 1: ACR_LOGIN_SERVER
- **Name:** `ACR_LOGIN_SERVER`
- **Value:** The output from `terraform output container_registry_url`
  - Example: `smartpathacr12345.azurecr.io`

### Secret 2: ACR_USERNAME
- **Name:** `ACR_USERNAME`
- **Value:** The output from `terraform output acr_username`
  - Example: `smartpathacr12345`

### Secret 3: ACR_PASSWORD
- **Name:** `ACR_PASSWORD`
- **Value:** The output from `terraform output -raw acr_password`
  - Example: `AbCdEfGhIjKlMnOpQrStUvWxYz1234567890`

## Step 3: Verify Setup

1. Create a test branch:
   ```bash
   git checkout -b test-ci-pipeline
   ```

2. Make a small change (e.g., update README.md)

3. Commit and push:
   ```bash
   git add .
   git commit -m "test: verify CI pipeline"
   git push origin test-ci-pipeline
   ```

4. Create a Pull Request to `main` branch

5. Go to **Actions** tab in GitHub and watch the pipeline run!

## Step 4: Verify Image in ACR

1. Go to Azure Portal: https://portal.azure.com
2. Navigate to: **Container registries** → Your ACR name
3. Click **Repositories** → **smartpath-app**
4. You should see your image tagged with the commit SHA!

## Troubleshooting

### Pipeline fails at "Log in to Azure Container Registry"
- ✅ Check that all three secrets are set correctly
- ✅ Verify ACR_LOGIN_SERVER doesn't have `https://` prefix
- ✅ Ensure ACR admin user is enabled (check in Terraform: `admin_enabled = true`)

### Pipeline fails at "Build Docker image"
- ✅ Check that `backend/Dockerfile` exists
- ✅ Verify Dockerfile syntax is correct
- ✅ Check that `requirements.txt` is in the backend directory

### Image not appearing in ACR
- ✅ Check pipeline logs for push errors
- ✅ Verify ACR credentials are correct
- ✅ Ensure ACR is in the same region as your resources

## Next Steps

After CI is working:
1. Set up CD pipeline (`.github/workflows/cd.yml`) for automatic deployment
2. Configure Ansible playbook to pull and deploy from ACR
3. Set up branch protection rules requiring CI to pass before merge

