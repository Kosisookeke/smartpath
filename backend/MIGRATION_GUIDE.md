# PostgreSQL Database Migration Guide

This guide explains how to run the database migration on your Azure app server.

## Prerequisites

1. SSH access to bastion host
2. SSH access from bastion to app server
3. Database connection details from Terraform outputs

## Step 1: Get Database Connection Details

Get the database connection details from Terraform Cloud or Azure Portal:

```bash
# From Terraform Cloud, get these values:
# - database_host (FQDN)
# - db_admin_username
# - db_admin_password
```

Or from Terraform outputs (if running locally):
```bash
cd terraform
terraform output database_host
terraform output database_name
```

## Step 2: Connect to App Server

```bash
# 1. SSH to bastion (from your local machine)
ssh -i ssh_key.pem azureuser@<BASTION_IP>

# 2. SSH to app server (from bastion)
ssh azureuser@<APP_VM_PRIVATE_IP>
```

## Step 3: Navigate to Application Directory

```bash
cd /opt/e-library/backend
```

## Step 4: Set Environment Variables

Create or update `.env` file with database connection details:

```bash
# Create .env file
cat > .env << EOF
DB_HOST=<database_host_fqdn>
DB_PORT=5432
DB_NAME=postgres
DB_USER=<db_admin_username>
DB_PASSWORD=<db_admin_password>
EOF
```

**Example:**
```bash
cat > .env << EOF
DB_HOST=smartpath-db-xxxxxx.smartpath.postgres.database.azure.com
DB_PORT=5432
DB_NAME=postgres
DB_USER=smartpath_admin
DB_PASSWORD=YourSecurePassword123!
EOF
```

## Step 5: Install Dependencies (if not already installed)

```bash
# Activate virtual environment (if using one)
source venv/bin/activate  # or python3 -m venv venv && source venv/bin/activate

# Install psycopg2-binary
pip install psycopg2-binary python-dotenv
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

## Step 6: Run Migration

```bash
python3 init_postgres_db.py
```

## Expected Output

```
============================================================
SmartPath PostgreSQL Database Initialization
============================================================
Creating database tables...
✓ Database tables created successfully

Seeding sample data...
✓ Created default users:
  - Admin: admin@smartpath.com / admin123
  - Student: student@smartpath.com / student123
✓ Created 3 sample courses
✓ Created 3 sample quizzes with questions

✅ Database initialization completed successfully!
============================================================
```

## Troubleshooting

### Error: "could not connect to server"

- Verify database host is correct
- Check NSG rules allow port 5432 from app VM subnet
- Verify database is running in Azure Portal

### Error: "password authentication failed"

- Double-check DB_USER and DB_PASSWORD in .env
- Verify credentials match Terraform variables

### Error: "module 'psycopg2' has no attribute 'connect'"

- Install psycopg2-binary: `pip install psycopg2-binary`

### Error: "relation already exists"

- Tables already exist, this is normal if migration was run before
- The script will skip data seeding if users already exist

## Verify Migration

After migration, verify tables were created:

```bash
# Connect to PostgreSQL (from app server)
psql -h <DB_HOST> -U <DB_USER> -d postgres

# List tables
\dt

# Check users
SELECT email, name, role FROM users;

# Exit
\q
```

## Next Steps

After successful migration:
1. Update backend code to use PostgreSQL instead of SQLite
2. Update `app/utils.py` to use psycopg2 instead of sqlite3
3. Restart backend application


