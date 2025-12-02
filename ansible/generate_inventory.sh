#!/bin/bash

# Script to generate Ansible inventory from environment variables
# This allows using the same approach as the CI/CD pipeline locally

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Generating Ansible inventory from environment variables...${NC}"

# Check required environment variables
REQUIRED_VARS=(
    "APP_VM_PRIVATE_IP"
    "BASTION_PUBLIC_IP"
)

MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        MISSING_VARS+=("$var")
    fi
done

if [ ${#MISSING_VARS[@]} -ne 0 ]; then
    echo -e "${RED}Error: Missing required environment variables:${NC}"
    for var in "${MISSING_VARS[@]}"; do
        echo -e "${RED}  - $var${NC}"
    done
    echo ""
    echo -e "${YELLOW}Please set these variables either:${NC}"
    echo "  1. Export them in your shell:"
    echo "     export APP_VM_PRIVATE_IP=your-ip"
    echo ""
    echo "  2. Create a .env file and source it:"
    echo "     cp .env.example .env"
    echo "     # Edit .env with your values"
    echo "     source .env"
    echo ""
    echo "  3. Pass them when running the script:"
    echo "     APP_VM_PRIVATE_IP=your-ip BASTION_PUBLIC_IP=your-ip ./generate_inventory.sh"
    exit 1
fi

# Set defaults for optional variables
ANSIBLE_USER="${ANSIBLE_USER:-azureuser}"
SSH_PRIVATE_KEY_FILE="${SSH_PRIVATE_KEY_FILE:-~/.ssh/id_rsa}"
PYTHON_INTERPRETER="${PYTHON_INTERPRETER:-/usr/bin/python3}"
APP_DIRECTORY="${APP_DIRECTORY:-/opt/smartpath}"

# Generate inventory.ini
INVENTORY_FILE="inventory.ini"

cat > "$INVENTORY_FILE" << EOF
# Ansible Inventory - Auto-generated from environment variables
# Generated at: $(date)
# DO NOT COMMIT THIS FILE - It contains sensitive information

[app_server]
app-vm ansible_host=${APP_VM_PRIVATE_IP}

[app_server:vars]
ansible_user=${ANSIBLE_USER}
ansible_ssh_private_key_file=${SSH_PRIVATE_KEY_FILE}
ansible_ssh_common_args='-o ProxyCommand="ssh -W %h:%p -q -i ${SSH_PRIVATE_KEY_FILE} ${ANSIBLE_USER}@${BASTION_PUBLIC_IP}"'
ansible_python_interpreter=${PYTHON_INTERPRETER}

[all:vars]
# Application variables
app_directory=${APP_DIRECTORY}
EOF

# Add ACR variables if provided (for deployment)
if [ -n "$ACR_LOGIN_SERVER" ]; then
    cat >> "$INVENTORY_FILE" << EOF
acr_login_server=${ACR_LOGIN_SERVER}
EOF
fi

if [ -n "$ACR_USERNAME" ]; then
    cat >> "$INVENTORY_FILE" << EOF
acr_username=${ACR_USERNAME}
EOF
fi

if [ -n "$ACR_PASSWORD" ]; then
    cat >> "$INVENTORY_FILE" << EOF
acr_password=${ACR_PASSWORD}
EOF
fi

# Add database variables if provided (for deployment)
if [ -n "$DB_HOST" ]; then
    cat >> "$INVENTORY_FILE" << EOF

# Database configuration
db_host=${DB_HOST}
EOF
fi

if [ -n "$DB_NAME" ]; then
    cat >> "$INVENTORY_FILE" << EOF
db_name=${DB_NAME}
EOF
fi

if [ -n "$DB_USER" ]; then
    cat >> "$INVENTORY_FILE" << EOF
db_user=${DB_USER}
EOF
fi

if [ -n "$DB_PASSWORD" ]; then
    cat >> "$INVENTORY_FILE" << EOF
db_password=${DB_PASSWORD}
EOF
fi

echo -e "${GREEN}✓ Inventory file generated successfully: ${INVENTORY_FILE}${NC}"
echo ""
echo -e "${YELLOW}Configuration:${NC}"
echo "  VM IP:        ${APP_VM_PRIVATE_IP}"
echo "  Bastion IP:   ${BASTION_PUBLIC_IP}"
echo "  User:         ${ANSIBLE_USER}"
echo "  SSH Key:      ${SSH_PRIVATE_KEY_FILE}"
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo "  1. Test connection:"
echo "     ansible app_server -i ${INVENTORY_FILE} -m ping"
echo ""
echo "  2. Run setup playbook:"
echo "     ansible-playbook -i ${INVENTORY_FILE} setup.yml"
echo ""
echo "  3. Run deployment playbook:"
echo "     ansible-playbook -i ${INVENTORY_FILE} deploy.yml"
echo ""
echo -e "${RED}Security Notice:${NC}"
echo "  - ${INVENTORY_FILE} is in .gitignore and won't be committed"
echo "  - Keep your environment variables secure"
echo "  - Use SSH keys, not passwords"
