# GitHub Secrets Setup Guide

This document lists all the secrets you need to configure in your GitHub repository for the CI/CD pipelines to work.

## 🔐 Required Secrets

### Azure Container Registry (ACR) Secrets

1. **ACR_LOGIN_SERVER**
   - Description: Azure Container Registry login server URL
   - How to get: Run `terraform output container_registry_url` or check Azure Portal
   - Example: `smartpathacruepjie.azurecr.io`

2. **ACR_USERNAME**
   - Description: ACR admin username
   - How to get: Run `terraform output acr_username` or check Azure Portal
   - Example: `smartpathacruepjie`

3. **ACR_PASSWORD**
   - Description: ACR admin password
   - How to get: Run `terraform output -raw acr_password` or check Azure Portal
   - ⚠️ **Sensitive**: Keep this secure!

### Infrastructure Secrets

4. **BASTION_PUBLIC_IP**
   - Description: Public IP address of the Bastion Host
   - How to get: Run `terraform output -raw bastion_public_ip`
   - Example: `4.213.170.37`

5. **APP_VM_PRIVATE_IP**
   - Description: Private IP address of the Application VM
   - How to get: Run `terraform output -raw app_vm_private_ip`
   - Example: `10.0.2.4`

6. **SSH_PRIVATE_KEY**
   - Description: SSH private key for accessing VMs
   - How to get: Copy contents of `terraform/ssh_key.pem`
   - ⚠️ **Sensitive**: Keep this secure!
   - Format: Include the entire key including `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----`

### Database Secrets

7. **DB_HOST**
   - Description: PostgreSQL database hostname
   - How to get: Run `terraform output -raw database_host`
   - Example: `smartpath-db-19m303.postgres.database.azure.com`

8. **DB_NAME**
   - Description: PostgreSQL database name
   - How to get: Run `terraform output -raw database_name`
   - Example: `smartpath-db-19m303`

9. **DB_USER**
   - Description: PostgreSQL database username
   - Default: `dbadmin`
   - ⚠️ **Sensitive**: Keep this secure!

10. **DB_PASSWORD**
    - Description: PostgreSQL database password
    - How to get: The password you set when creating the database (stored in Terraform Cloud variable `db_admin_password`)
    - ⚠️ **Sensitive**: Keep this secure!

## 📝 How to Add Secrets to GitHub

1. Go to your GitHub repository
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Enter the secret name and value
5. Click **Add secret**

## 🔍 Quick Setup Script

You can use this script to get all the values from Terraform:

```bash
cd terraform

echo "=== GitHub Secrets to Add ==="
echo ""
echo "ACR_LOGIN_SERVER=$(terraform output -raw container_registry_url)"
echo "ACR_USERNAME=$(terraform output -raw acr_username)"
echo "ACR_PASSWORD=$(terraform output -raw acr_password)"
echo "BASTION_PUBLIC_IP=$(terraform output -raw bastion_public_ip)"
echo "APP_VM_PRIVATE_IP=$(terraform output -raw app_vm_private_ip)"
echo "DB_HOST=$(terraform output -raw database_host)"
echo "DB_NAME=$(terraform output -raw database_name)"
echo ""
echo "SSH_PRIVATE_KEY=$(cat ssh_key.pem)"
echo ""
echo "DB_USER=dbadmin"
echo "DB_PASSWORD=<your-db-password-from-terraform-cloud>"
```

## ✅ Verification

After adding all secrets, verify they're set correctly:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. You should see all 10 secrets listed
3. Test the CD pipeline by pushing to `main` branch or using **workflow_dispatch**

## 🔒 Security Best Practices

1. **Never commit secrets** to the repository
2. **Rotate secrets regularly** (especially SSH keys and passwords)
3. **Use least privilege** - only grant necessary permissions
4. **Monitor secret usage** in GitHub Actions logs
5. **Use environment-specific secrets** for different environments (dev/staging/prod)

## 🐛 Troubleshooting

### Secret Not Found Error

If you see `Secret not found` errors:
- Verify the secret name matches exactly (case-sensitive)
- Check that you're in the correct repository
- Ensure the secret is added under **Actions** secrets, not **Dependabot** secrets

### SSH Connection Fails

If SSH connections fail:
- Verify `SSH_PRIVATE_KEY` includes the full key with headers
- Check that `BASTION_PUBLIC_IP` and `APP_VM_PRIVATE_IP` are correct
- Ensure the SSH key has correct permissions (600)

### ACR Authentication Fails

If ACR login fails:
- Verify `ACR_LOGIN_SERVER`, `ACR_USERNAME`, and `ACR_PASSWORD` are correct
- Check that ACR admin user is enabled in Azure Portal
- Ensure the password hasn't been rotated

## 📚 Additional Resources

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Azure Container Registry Authentication](https://docs.microsoft.com/azure/container-registry/container-registry-authentication)
- [Terraform Outputs](https://www.terraform.io/docs/language/values/outputs.html)

