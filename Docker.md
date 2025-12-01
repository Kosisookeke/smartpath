# Docker Setup for SmartPath Learning Platform

This document provides instructions for running the SmartPath Learning Platform using Docker.

## Prerequisites

- Docker Engine 20.10 or higher
- Docker Compose 2.0 or higher

## Architecture

The application consists of two services:

- **Backend**: Python Flask API (port 5000)
- **Frontend**: React application served by Nginx (port 80)

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository** (if not already done)

2. **Build and start all services:**
   ```bash
   docker-compose up -d
   ```

3. **Access the application:**
   - Frontend: http://localhost
   - Backend API: http://localhost:5000
   - Health check: http://localhost:5000/api/health

4. **View logs:**
   ```bash
   # All services
   docker-compose logs -f

   # Specific service
   docker-compose logs -f backend
   docker-compose logs -f frontend
   ```

5. **Stop services:**
   ```bash
   docker-compose down
   ```

6. **Stop and remove volumes (reset database):**
   ```bash
   docker-compose down -v
   ```

## Building Individual Services

### Backend Only

```bash
cd backend
docker build -t smartpath-backend .
docker run -p 5000:5000 smartpath-backend
```

### Frontend Only

```bash
cd frontend
docker build -t smartpath-frontend .
docker run -p 80:80 smartpath-frontend
```

## Environment Variables

You can customize the deployment by creating a `.env` file in the root directory:

```env
# Backend
SECRET_KEY=your-production-secret-key
FLASK_ENV=production

# Frontend
REACT_APP_API_URL=http://localhost:5000
```

Then run:
```bash
docker-compose --env-file .env up -d
```

## Default Test Accounts

The application comes with pre-configured test accounts:

- **Admin**:
  - Email: `admin@smartpath.com`
  - Password: `admin123`

- **Student**:
  - Email: `student@smartpath.com`
  - Password: `student123`

## Data Persistence

The backend database is stored in a Docker volume named `backend-data`. This ensures data persists across container restarts.

To backup the database:
```bash
docker cp smartpath-backend:/app/database/smartpath.db ./backup.db
```

To restore the database:
```bash
docker cp ./backup.db smartpath-backend:/app/database/smartpath.db
docker-compose restart backend
```

## Health Checks

Both services include health checks:

- **Backend**: Checks `/api/health` endpoint every 30 seconds
- **Frontend**: Checks root endpoint every 30 seconds

View health status:
```bash
docker ps
```

## Troubleshooting

### Port Already in Use

If port 80 or 5000 is already in use, modify the `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "5001:5000"  # Change host port
  frontend:
    ports:
      - "8080:80"    # Change host port
```

### Database Not Initializing

If the database isn't initializing properly:

```bash
docker-compose down -v
docker-compose up -d
```

### View Container Logs

```bash
docker-compose logs backend
docker-compose logs frontend
```

### Rebuild After Code Changes

```bash
docker-compose up -d --build
```

## Production Deployment

For production deployment:

1. **Update the SECRET_KEY** in your environment variables
2. **Use a reverse proxy** (e.g., Nginx, Traefik) for SSL/TLS termination
3. **Consider using a production database** instead of SQLite
4. **Enable HTTPS** for secure communication
5. **Set up monitoring and logging**

## Cleaning Up

Remove all containers, networks, and volumes:

```bash
docker-compose down -v
docker rmi smartpath-backend smartpath-frontend
```

## Support

For issues or questions, refer to the main README.md or create an issue in the repository.
