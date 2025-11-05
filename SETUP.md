# 🚀 Device Monitoring System - Complete Setup Guide

This comprehensive guide covers all setup methods for the Device Monitoring System, including Docker, manual installation, and production deployment.

---

## 📋 Table of Contents

1. [Quick Start](#-quick-start)
2. [Prerequisites](#-prerequisites)
3. [Setup Methods](#-setup-methods)
   - [Method 1: Docker (Recommended)](#method-1-docker-recommended)
   - [Method 2: Docker Compose (Production)](#method-2-docker-compose-production)
   - [Method 3: Manual Setup (Development)](#method-3-manual-setup-development)
4. [Configuration](#-configuration)
5. [Running the Application](#-running-the-application)
6. [Testing](#-testing)
7. [Production Deployment](#-production-deployment)
8. [Troubleshooting](#-troubleshooting)

---

## ⚡ Quick Start

### Option A: With Docker (Fastest)
```bash
cd backend
docker-compose up -d
```
Access at: http://localhost:5000

### Option B: Without Docker (Windows)
```bash
cd backend
.\START.bat
```
Access at: http://localhost:5000

### Option C: Without Docker (Linux/Mac)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python start.py
```
Access at: http://localhost:5000

---

## 📦 Prerequisites

### For All Setups
- **Git** (to clone the repository)
- **Web Browser** (Chrome, Firefox, Edge, Safari)

### For Docker Setup
- **Docker** 20.10+ ([Download](https://www.docker.com/get-started))
- **Docker Compose** 2.0+ (included with Docker Desktop)

### For Manual Setup
- **Python** 3.9+ ([Download](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **Redis** 7+ (optional, for background tasks) ([Download](https://redis.io/download))

### System Requirements
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 500MB minimum
- **OS**: Windows 10+, Ubuntu 20.04+, macOS 11+

---

## 🐳 Setup Methods

### Method 1: Docker (Recommended)

**Best for:** Quick testing, consistent environments, easy deployment

#### Step 1: Clone Repository
```bash
git clone https://github.com/cosmic-striker/coll.git
cd coll/backend
```

#### Step 2: Build Docker Image
```bash
docker build -t device-monitoring:latest .
```

#### Step 3: Run Container
```bash
docker run -d \
  --name device-monitoring \
  -p 5000:5000 \
  -v $(pwd)/instance:/app/instance \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  -e JWT_SECRET_KEY=your-jwt-secret \
  device-monitoring:latest
```

#### Step 4: Check Logs
```bash
docker logs -f device-monitoring
```

#### Step 5: Access Application
Open browser: http://localhost:5000

**Default Credentials:**
- **Admin**: `admin` / `Admin@123`
- **Operator**: `operator` / `Operator@123`
- **Viewer**: `viewer` / `Viewer@123`

---

### Method 2: Docker Compose (Production)

**Best for:** Production deployments, multi-service setups

#### Step 1: Create Environment File
```bash
cd backend
cp .env.example .env
```

#### Step 2: Edit Configuration
Edit `.env` file and set your values:
```bash
# Generate secure keys
FLASK_ENV=production
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)
```

#### Step 3: Start All Services
```bash
docker-compose up -d
```

This starts:
- **Backend API** (Flask) on port 5000
- **Redis** (Celery broker) on port 6379
- **Celery Worker** (background tasks)

#### Step 4: View Services
```bash
docker-compose ps
```

#### Step 5: View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
```

#### Step 6: Stop Services
```bash
docker-compose down
```

#### Step 7: Stop and Remove All Data
```bash
docker-compose down -v
```

---

### Method 3: Manual Setup (Development)

**Best for:** Development, customization, debugging

#### Windows Setup

##### Step 1: Install Python
Download and install Python 3.9+ from https://www.python.org/downloads/

Check installation:
```powershell
python --version
pip --version
```

##### Step 2: Clone Repository
```powershell
git clone https://github.com/cosmic-striker/coll.git
cd coll\backend
```

##### Step 3: Create Virtual Environment
```powershell
python -m venv venv
venv\Scripts\activate
```

##### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

##### Step 5: Create Environment File
```powershell
copy .env.example .env
```

##### Step 6: Initialize Database
```powershell
python start.py
```

##### Step 7: Run Application
```powershell
# Development mode (with auto-reload)
$env:FLASK_DEBUG="true"
python start.py

# Or use the batch file
.\START.bat
```

---

#### Linux/Mac Setup

##### Step 1: Install Python
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# macOS (using Homebrew)
brew install python@3.11
```

Check installation:
```bash
python3 --version
pip3 --version
```

##### Step 2: Clone Repository
```bash
git clone https://github.com/cosmic-striker/coll.git
cd coll/backend
```

##### Step 3: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

##### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

##### Step 5: Create Environment File
```bash
cp .env.example .env
```

##### Step 6: Set Permissions (if needed)
```bash
chmod +x start.py
chmod +x run.py
```

##### Step 7: Initialize Database
```bash
python start.py
```

##### Step 8: Run Application
```bash
# Development mode
export FLASK_DEBUG=true
python start.py

# Production mode with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 run:app
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```bash
# Required Settings
FLASK_ENV=development              # or 'production'
FLASK_DEBUG=true                   # or 'false'
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Optional Settings
PORT=5000
DATABASE_URL=sqlite:///devices.db
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Generate Secure Keys

**Python Method:**
```python
import secrets
print("SECRET_KEY:", secrets.token_hex(32))
print("JWT_SECRET_KEY:", secrets.token_hex(32))
```

**OpenSSL Method:**
```bash
openssl rand -hex 32
```

### Database Configuration

#### SQLite (Default - Development)
```bash
DATABASE_URL=sqlite:///devices.db
```

#### PostgreSQL (Production)
```bash
# Install PostgreSQL
# Ubuntu: sudo apt install postgresql postgresql-contrib
# macOS: brew install postgresql

# Create database
sudo -u postgres psql
CREATE DATABASE device_monitoring;
CREATE USER dbuser WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE device_monitoring TO dbuser;

# Update .env
DATABASE_URL=postgresql://dbuser:password@localhost:5432/device_monitoring
```

#### MySQL (Alternative)
```bash
DATABASE_URL=mysql://username:password@localhost:3306/device_monitoring
```

---

## 🏃 Running the Application

### Development Mode

#### Windows
```powershell
cd backend
venv\Scripts\activate
$env:FLASK_DEBUG="true"
python start.py
```

#### Linux/Mac
```bash
cd backend
source venv/bin/activate
export FLASK_DEBUG=true
python start.py
```

### Production Mode

#### With Gunicorn (Linux/Mac)
```bash
gunicorn --bind 0.0.0.0:5000 \
         --workers 4 \
         --timeout 120 \
         --access-logfile logs/access.log \
         --error-logfile logs/error.log \
         run:app
```

#### With Waitress (Windows)
```powershell
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 run:app
```

#### With Docker
```bash
docker-compose up -d
```

### Running with Celery (Background Tasks)

#### Start Redis
```bash
# Docker
docker run -d --name redis -p 6379:6379 redis:7

# Linux
sudo systemctl start redis

# macOS
brew services start redis

# Windows (WSL or Docker)
docker run -d --name redis -p 6379:6379 redis:7
```

#### Start Celery Worker
```bash
# In a separate terminal
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
celery -A celery_worker.celery worker --loglevel=info
```

---

## 🧪 Testing

### Run Comprehensive Tests
```bash
cd backend
python main_test.py
```

### Run Specific Test Categories
```bash
# Test with custom URL
python main_test.py --url http://localhost:8080

# Test with different credentials
python main_test.py --username operator --password Operator@123
```

### Manual API Testing

#### Using cURL
```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin@123"}'

# Get devices (with token)
curl -X GET http://localhost:5000/api/devices/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### Using Python
```python
import requests

# Login
response = requests.post('http://localhost:5000/api/auth/login',
    json={'username': 'admin', 'password': 'Admin@123'})
token = response.json()['access_token']

# Get devices
response = requests.get('http://localhost:5000/api/devices/',
    headers={'Authorization': f'Bearer {token}'})
devices = response.json()
print(devices)
```

---

## 🌐 Production Deployment

### 1. Using Docker Compose

```bash
# Production docker-compose.yml
version: '3.8'

services:
  backend:
    build: .
    restart: always
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - ./instance:/app/instance
      - ./logs:/app/logs
    depends_on:
      - redis
      - postgres

  postgres:
    image: postgres:15
    restart: always
    environment:
      - POSTGRES_USER=dbuser
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=device_monitoring
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    restart: always

  celery:
    build: .
    restart: always
    command: celery -A celery_worker.celery worker --loglevel=info
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      - redis
      - postgres

volumes:
  postgres_data:
```

### 2. Using Nginx Reverse Proxy

#### Install Nginx
```bash
# Ubuntu
sudo apt install nginx

# macOS
brew install nginx
```

#### Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/device-monitoring
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/coll/backend/app/static;
    }
}
```

#### Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/device-monitoring /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 3. Using systemd (Linux)

Create `/etc/systemd/system/device-monitoring.service`:

```ini
[Unit]
Description=Device Monitoring System
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/device-monitoring/backend
Environment="PATH=/opt/device-monitoring/backend/venv/bin"
ExecStart=/opt/device-monitoring/backend/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 run:app
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Enable and Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable device-monitoring
sudo systemctl start device-monitoring
sudo systemctl status device-monitoring
```

### 4. SSL/HTTPS with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Error: Address already in use

# Find process using port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>

# Or use different port
export PORT=8080
python start.py
```

#### 2. Module Not Found
```bash
# Error: ModuleNotFoundError

# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. Database Locked (SQLite)
```bash
# Error: database is locked

# Close all connections
# Delete database and recreate
rm instance/devices.db
python start.py
```

#### 4. Celery Connection Error
```bash
# Error: Cannot connect to Redis

# Start Redis
docker run -d --name redis -p 6379:6379 redis:7

# Or disable Celery by not setting CELERY_BROKER_URL
```

#### 5. Permission Denied
```bash
# Linux/Mac
chmod +x start.py
chmod 755 logs/
```

#### 6. Docker Build Fails
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t device-monitoring .
```

### Debug Mode

Enable detailed logging:
```bash
export FLASK_DEBUG=true
export LOG_LEVEL=DEBUG
python start.py
```

Check logs:
```bash
tail -f logs/app.log
```

---

## 📚 Additional Resources

### Project Documentation
- `README.md` - Project overview
- `IMPLEMENTATION_COMPLETE.md` - Implementation details
- `TEST_RESULTS.md` - Test coverage report
- `UI_IMPROVEMENTS.md` - UI/UX documentation

### API Documentation
Once running, access:
- **Health Check**: http://localhost:5000/health
- **API Health**: http://localhost:5000/api/health

### Default Users
After first run, three users are created:
1. **Admin** - Full access
   - Username: `admin`
   - Password: `Admin@123`

2. **Operator** - Can manage devices/cameras/alerts
   - Username: `operator`
   - Password: `Operator@123`

3. **Viewer** - Read-only access
   - Username: `viewer`
   - Password: `Viewer@123`

**⚠️ Change default passwords in production!**

---

## 🎯 Next Steps

1. **Change default passwords** for security
2. **Configure environment variables** for your setup
3. **Set up SSL/HTTPS** for production
4. **Configure backups** for database
5. **Set up monitoring** and alerts
6. **Review security settings** before going live

---

## 🆘 Getting Help

- **Issues**: Report on [GitHub Issues](https://github.com/cosmic-striker/coll/issues)
- **Documentation**: Check the `/backend/` directory for detailed docs
- **Tests**: Run `python main_test.py` for diagnostics

---

## 📄 License

See LICENSE file in the repository.

---

**Happy Monitoring! 🎉**
