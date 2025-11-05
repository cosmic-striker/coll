# Device Monitoring Backend API

A comprehensive, production-ready Flask-based backend system for centralized monitoring of network devices and IP cameras with real-time alerting, role-based access control, and automated background processing.

## 🎯 Overview

This backend provides a complete REST API for monitoring network infrastructure, featuring:

- **Network Device Monitoring**: Automated health checks for switches, routers, access points, and other network equipment
- **IP Camera Management**: RTSP stream monitoring and connection testing for security cameras
- **Real-time Alerting**: Multi-channel notifications (Email, Slack) with configurable severity levels
- **Role-based Security**: JWT authentication with admin/operator/viewer permissions
- **Background Processing**: Celery-powered asynchronous tasks for polling and notifications
- **Production Deployment**: Docker containerization with Redis, comprehensive logging, and scalability features

## 🏗️ Architecture

### Core Components

```
backend/
├── app/                          # Main application package
│   ├── __init__.py              # Flask app factory with Celery integration
│   ├── config.py                # Environment-based configuration
│   ├── models.py                # SQLAlchemy database models
│   ├── routes/                  # API blueprint modules
│   │   ├── auth.py             # Authentication & user management
│   │   ├── devices.py          # Device CRUD and polling
│   │   ├── cameras.py          # Camera management and testing
│   │   └── alerts.py           # Alert creation and management
│   ├── services/               # Background processing services
│   │   ├── poller.py           # Device/camera polling logic
│   │   └── alerting.py         # Email/Slack notification services
│   ├── static/                 # Static assets (CSS/JS)
│   ├── templates/              # HTML templates
│   └── utils.py                # Helper functions
├── celery_worker.py             # Celery worker entry point
├── run.py                       # Flask development server
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Production container
├── docker-compose.yml           # Multi-service orchestration
└── test_*.py                    # Testing scripts
```

### Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Framework** | Flask | 2.3.3 | REST API development |
| **Database** | SQLAlchemy | 2.0.23 | ORM with SQLite/PostgreSQL support |
| **Authentication** | Flask-JWT-Extended | 4.5.3 | JWT token management |
| **Background Tasks** | Celery | 5.3.4 | Asynchronous processing |
| **Message Broker** | Redis | 5.0.1 | Task queue and caching |
| **Migrations** | Flask-Migrate | 4.0.5 | Database schema management |
| **Containerization** | Docker | - | Deployment and scaling |
| **WSGI Server** | Gunicorn | 21.2.0 | Production server |

## 🚀 Quick Start

### Prerequisites

- **Python**: 3.10 or higher
- **Docker**: For containerized deployment
- **Redis**: For background task processing (handled by Docker Compose)

### Local Development Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   # Windows PowerShell
   $env:FLASK_ENV="development"
   $env:FLASK_DEBUG="true"
   $env:SECRET_KEY="your-secret-key-here"
   $env:JWT_SECRET_KEY="your-jwt-secret-here"

   # Linux/Mac
   export FLASK_ENV=development
   export FLASK_DEBUG=true
   export SECRET_KEY=your-secret-key-here
   export JWT_SECRET_KEY=your-jwt-secret-here
   ```

5. **Initialize database**
   ```bash
   python run.py
   ```
   The application will create tables and a default admin user.

6. **Start Redis (separate terminal)**
   ```bash
   docker run -d -p 6379:6379 redis:7
   ```

7. **Start Celery worker (separate terminal)**
   ```bash
   celery -A celery_worker.celery worker --loglevel=info
   ```

8. **Start Celery beat scheduler (separate terminal)**
   ```bash
   celery -A celery_worker.celery beat --loglevel=info
   ```

9. **Test the API**
   ```bash
   python test_api.py
   ```

### Docker Deployment (Recommended)

1. **Build and run services**
   ```bash
   docker-compose up -d
   ```

2. **View application logs**
   ```bash
   docker-compose logs -f backend
   ```

3. **Scale Celery workers**
   ```bash
   docker-compose up -d --scale celery_worker=3
   ```

4. **Stop services**
   ```bash
   docker-compose down
   ```

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Authentication

All API endpoints (except login) require JWT authentication via Authorization header:
```
Authorization: Bearer <access_token>
```

#### POST /auth/login
Authenticate user and receive JWT tokens.

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAi...",
  "refresh_token": "eyJ0eXAi...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "admin"
  }
}
```

#### POST /auth/refresh
Refresh access token using refresh token.

#### GET /auth/profile
Get current user profile information.

#### GET /auth/users (Admin only)
List all users with pagination.

#### POST /auth/users (Admin only)
Create new user.

#### PUT /auth/users/{user_id} (Admin only)
Update user information.

#### DELETE /auth/users/{user_id} (Admin only)
Delete user account.

### Device Management

#### GET /devices/
List all devices with optional filtering.

**Query Parameters:**
- `status`: Filter by device status (online/offline/unknown)

**Response:**
```json
[
  {
    "id": 1,
    "name": "Core-Switch-01",
    "ip_address": "192.168.1.10",
    "vendor": "Cisco",
    "device_type": "switch",
    "snmp_community": "public",
    "last_seen": "2024-01-15T10:30:00Z",
    "status": "online",
    "meta": {"interfaces": 24, "firmware": "15.2"}
  }
]
```

#### GET /devices/{device_id}
Get detailed information for specific device.

#### POST /devices/ (Operator+)
Create new device for monitoring.

**Request:**
```json
{
  "name": "Access-Point-01",
  "ip_address": "192.168.1.15",
  "vendor": "Ubiquiti",
  "device_type": "access_point",
  "snmp_community": "public",
  "meta": {"model": "UAP-AC-Pro"}
}
```

#### PUT /devices/{device_id} (Operator+)
Update device information.

#### DELETE /devices/{device_id} (Admin only)
Remove device from monitoring.

#### POST /devices/{device_id}/poll (Operator+)
Trigger immediate device polling.

**Response:**
```json
{
  "msg": "Polling initiated",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "device_id": 1
}
```

#### GET /devices/status
Get device status summary.

**Response:**
```json
{
  "total": 25,
  "online": 22,
  "offline": 2,
  "unknown": 1
}
```

### Camera Management

#### GET /cameras/
List all IP cameras.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Front-Entrance-Cam",
    "ip_address": "192.168.1.20",
    "rtsp_url": "rtsp://192.168.1.20:554/stream1",
    "username": "admin",
    "location": "Main Entrance",
    "status": "online",
    "last_snapshot": "/snapshots/camera_1_20240115_103000.jpg"
  }
]
```

#### GET /cameras/{camera_id}
Get camera details.

#### POST /cameras/ (Operator+)
Register new IP camera.

**Request:**
```json
{
  "name": "Parking-Lot-Cam",
  "ip_address": "192.168.1.25",
  "rtsp_url": "rtsp://192.168.1.25:554/live",
  "username": "admin",
  "password": "securepass123",
  "location": "Parking Lot North"
}
```

#### PUT /cameras/{camera_id} (Operator+)
Update camera configuration.

#### DELETE /cameras/{camera_id} (Admin only)
Remove camera from system.

#### GET /cameras/{camera_id}/stream
Get camera stream information for frontend consumption.

#### POST /cameras/{camera_id}/test (Operator+)
Test camera RTSP connection.

**Response:**
```json
{
  "msg": "Camera connection test completed",
  "result": {
    "camera_id": 1,
    "status": "online",
    "status_changed": false
  }
}
```

#### GET /cameras/status
Get camera status summary.

### Alert Management

#### GET /alerts/
List alerts with pagination and filtering.

**Query Parameters:**
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 50)
- `severity`: Filter by severity (critical/high/medium/low/info)
- `acknowledged`: Filter by acknowledgment status (true/false)

**Response:**
```json
{
  "alerts": [
    {
      "id": 1,
      "device_id": 1,
      "device_name": "Core-Switch-01",
      "severity": "high",
      "message": "Device Core-Switch-01 went offline",
      "created_at": "2024-01-15T10:25:00Z",
      "acknowledged": false,
      "acknowledged_at": null
    }
  ],
  "pagination": {
    "page": 1,
    "pages": 1,
    "per_page": 50,
    "total": 1
  }
}
```

#### GET /alerts/{alert_id}
Get specific alert details.

#### POST /alerts/ (Operator+)
Create manual alert.

**Request:**
```json
{
  "device_id": 1,
  "severity": "medium",
  "message": "Manual maintenance alert"
}
```

#### POST /alerts/{alert_id}/acknowledge (Operator+)
Acknowledge specific alert.

#### POST /alerts/acknowledge-all (Operator+)
Acknowledge multiple alerts.

**Request:**
```json
{
  "severity": "low"
}
```

#### DELETE /alerts/{alert_id} (Admin only)
Delete alert from system.

#### GET /alerts/summary
Get alerts summary with recent alerts.

**Response:**
```json
{
  "total": 15,
  "unacknowledged": 3,
  "critical": 0,
  "high": 1,
  "recent": [
    {
      "id": 15,
      "device_name": "Server-Rack-01",
      "severity": "high",
      "message": "High CPU usage detected",
      "created_at": "2024-01-15T11:00:00Z"
    }
  ]
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_ENV` | Environment mode | development | No |
| `FLASK_DEBUG` | Debug mode | false | No |
| `SECRET_KEY` | Flask session secret | auto-generated | Yes (production) |
| `JWT_SECRET_KEY` | JWT signing secret | auto-generated | Yes (production) |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration | 30 | No |
| `DATABASE_URL` | Database connection | sqlite:///devices.db | No |
| `CELERY_BROKER_URL` | Redis broker URL | redis://localhost:6379/0 | Yes (for background tasks) |
| `CELERY_RESULT_BACKEND` | Redis result backend | redis://localhost:6379/0 | Yes (for background tasks) |
| `SMTP_SERVER` | SMTP server | smtp.gmail.com | No (for email alerts) |
| `SMTP_PORT` | SMTP port | 587 | No |
| `SMTP_USERNAME` | SMTP username | - | No |
| `SMTP_PASSWORD` | SMTP password | - | No |
| `ALERT_EMAIL_FROM` | Alert sender email | alerts@example.com | No |
| `ALERT_EMAIL_TO` | Alert recipient email | admin@example.com | No |
| `SLACK_WEBHOOK_URL` | Slack webhook URL | - | No |
| `POLL_INTERVAL_SECONDS` | Device poll interval | 60 | No |
| `CORS_ORIGINS` | Allowed CORS origins | http://localhost:3000,http://localhost:5000 | No |
| `RATE_LIMIT_DEFAULT` | Default rate limit | 100 per minute | No |
| `RATE_LIMIT_LOGIN` | Login rate limit | 5 per minute | No |
| `RATE_LIMIT_API` | API rate limit | 1000 per hour | No |
| `PASSWORD_MIN_LENGTH` | Minimum password length | 8 | No |
| `PASSWORD_REQUIRE_UPPERCASE` | Require uppercase letters | true | No |
| `PASSWORD_REQUIRE_LOWERCASE` | Require lowercase letters | true | No |
| `PASSWORD_REQUIRE_DIGITS` | Require digits | true | No |
| `PASSWORD_REQUIRE_SPECIAL` | Require special characters | false | No |

### Security Configuration

#### Password Policy
- Minimum 8 characters
- Must contain uppercase and lowercase letters
- Must contain at least one digit
- Special characters recommended but not required

#### Rate Limiting
- Login attempts: 5 per minute per IP
- General API: 100 requests per minute per IP
- Authenticated API: 1000 requests per hour per user

#### CORS Settings
- Default allowed origins: localhost:3000, localhost:5000
- Supports credentials for authenticated requests
- Configurable via `CORS_ORIGINS` environment variable

#### Security Headers
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `Content-Security-Policy: default-src 'self'`

#### JWT Configuration
- Access tokens expire in 30 minutes
- Refresh tokens supported for extended sessions
- Secure token storage recommended

### Default Configuration

The application creates a default admin user on first startup:
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@example.com`
- **Role**: `admin`

⚠️ **Important**: Change the default password immediately in production!

### User Roles & Permissions

| Role | Description | Permissions |
|------|-------------|-------------|
| **Admin** | Full system access | All operations including user management |
| **Operator** | Device/camera management | CRUD operations, polling, alert acknowledgment |
| **Viewer** | Read-only access | View devices, cameras, alerts, and status |

## 🔒 Security Features

### Authentication & Authorization
- **JWT-based authentication** with access and refresh tokens
- **Role-based access control** (Admin, Operator, Viewer)
- **Password complexity validation** with configurable requirements
- **Secure password hashing** using Werkzeug security

### Rate Limiting
- **Login protection**: 5 attempts per minute per IP address
- **API protection**: 100 requests per minute per IP (unauthenticated)
- **Authenticated API**: 1000 requests per hour per user
- **Configurable limits** via environment variables

### Cross-Origin Resource Sharing (CORS)
- **Configurable origins** for frontend integration
- **Credentials support** for authenticated requests
- **Secure defaults** with localhost support

### Security Headers
- **XSS Protection**: Prevents cross-site scripting attacks
- **Content Sniffing Protection**: Prevents MIME type confusion
- **Frame Options**: Prevents clickjacking attacks
- **Strict Transport Security**: Enforces HTTPS connections
- **Content Security Policy**: Restricts resource loading

### Input Validation
- **Password strength requirements** (8+ chars, mixed case, digits)
- **SQL injection prevention** via SQLAlchemy ORM
- **XSS prevention** through proper escaping
- **Input sanitization** on all user inputs

### Secure Configuration
- **Auto-generated secrets** for production deployments
- **Environment variable validation** for sensitive data
- **Secure defaults** with production-ready settings
- **Comprehensive logging** for security events

### Security Testing
Run security tests to validate all security features:
```bash
python test_security.py
```

This includes tests for:
- Rate limiting functionality
- Security headers presence
- CORS configuration
- Password validation rules
- Authentication requirements

## 🔄 Background Processing

### Scheduled Tasks

The system runs automated background tasks using Celery Beat:

| Task | Schedule | Description |
|------|----------|-------------|
| `poll_all_devices` | Every 5 minutes | Health check all network devices |
| `poll_all_cameras` | Every 10 minutes | Test all camera connections |
| `send_daily_summary` | Daily at midnight | Email/Slack daily status report |

### Manual Task Triggers

- **Device Polling**: `POST /api/devices/{id}/poll`
- **Camera Testing**: `POST /api/cameras/{id}/test`
- **Alert Notifications**: Automatic on alert creation

### Task Monitoring

Monitor Celery tasks through Docker logs:
```bash
docker-compose logs -f celery_worker
```

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(20) DEFAULT 'viewer'
);
```

### Devices Table
```sql
CREATE TABLE device (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    vendor VARCHAR(50),
    device_type VARCHAR(50),
    snmp_community VARCHAR(50) DEFAULT 'public',
    last_seen DATETIME,
    status VARCHAR(20) DEFAULT 'unknown',
    meta JSON
);
```

### Cameras Table
```sql
CREATE TABLE camera (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    rtsp_url VARCHAR(255) NOT NULL,
    username VARCHAR(64),
    password VARCHAR(64),
    location VARCHAR(100),
    status VARCHAR(20) DEFAULT 'unknown',
    last_snapshot VARCHAR(255)
);
```

### Alerts Table
```sql
CREATE TABLE alert (
    id INTEGER PRIMARY KEY,
    device_id INTEGER REFERENCES device(id),
    severity VARCHAR(20),
    message VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_at DATETIME
);
```

## 🧪 Testing

### API Testing Script

Run comprehensive API tests:
```bash
python test_api.py
```

### Manual Testing

Test individual endpoints using curl:
```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# List devices (replace TOKEN with actual token)
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:5000/api/devices/
```

### Unit Tests

Run unit tests (when implemented):
```bash
python -m pytest
```

## 🚀 Production Deployment

### Security Checklist

- ✅ Change default admin credentials immediately
- ✅ Use strong, auto-generated SECRET_KEY and JWT_SECRET_KEY
- ✅ Configure HTTPS with SSL/TLS certificates
- ✅ Set up proper firewall rules and network segmentation
- ✅ Use environment variables for all sensitive configuration
- ✅ Enable comprehensive logging and monitoring
- ✅ Configure rate limiting for API protection
- ✅ Set up CORS policies for frontend integration
- ✅ Enable all security headers (XSS, CSRF, HSTS, CSP)
- ✅ Implement password complexity requirements
- ✅ Regular security updates and dependency scanning
- ✅ Set up intrusion detection and log monitoring

### Environment Setup

#### Production Environment Variables
```bash
# Security (auto-generated in production)
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
export JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"

# Database
export DATABASE_URL="postgresql://user:password@localhost:5432/devices_db"

# Redis/Celery
export CELERY_BROKER_URL="redis://localhost:6379/0"
export CELERY_RESULT_BACKEND="redis://localhost:6379/0"

# Email/Slack alerts
export SMTP_SERVER="smtp.company.com"
export SMTP_USERNAME="alerts@company.com"
export SMTP_PASSWORD="secure_password"
export ALERT_EMAIL_TO="admin@company.com"
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/.../.../..."

# Security settings
export CORS_ORIGINS="https://yourdomain.com,https://app.yourdomain.com"
export RATE_LIMIT_DEFAULT="100/minute"
export RATE_LIMIT_LOGIN="5/minute"
export RATE_LIMIT_API="1000/hour"
```

#### Docker Production Deployment
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy with environment file
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

### Scaling Considerations

#### Horizontal Scaling
```bash
# Scale Flask application
docker-compose up -d --scale backend=3

# Scale Celery workers
docker-compose up -d --scale celery_worker=5
```

#### Database Scaling
- Migrate from SQLite to PostgreSQL for production
- Configure connection pooling
- Set up database replication for high availability

#### Redis Clustering
- Use Redis Cluster for distributed task processing
- Configure Redis Sentinel for automatic failover

### Monitoring & Logging

#### Application Logs
- Flask application: `logs/backend.log`
- Celery workers: Docker container logs
- Database queries: Enable SQLAlchemy echo in debug mode

#### Health Checks
```bash
# Application health
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:5000/api/auth/profile

# Redis connectivity
docker-compose exec redis redis-cli ping

# Celery worker status
docker-compose exec celery_worker celery -A app.celery inspect active
```

### Backup Strategy

1. **Database Backup**:
   ```bash
   # SQLite backup
   cp devices.db devices_backup_$(date +%Y%m%d_%H%M%S).db

   # PostgreSQL backup
   pg_dump devices_db > backup_$(date +%Y%m%d_%H%M%S).sql
   ```

2. **Configuration Backup**:
   ```bash
   # Environment variables
   env > env_backup_$(date +%Y%m%d_%H%M%S).txt
   ```

## 🔧 Development

### Database Migrations

```bash
# Create migration
flask db migrate -m "Add new field to device table"

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade
```

### Adding New Features

#### New Device Types
1. Update `Device` model in `app/models.py`
2. Add polling logic in `app/services/poller.py`
3. Update API endpoints in `app/routes/devices.py`

#### New Alert Channels
1. Implement notification function in `app/services/alerting.py`
2. Add configuration variables to `app/config.py`
3. Update `send_alert_notification` task

#### New API Endpoints
1. Create new blueprint in `app/routes/`
2. Register blueprint in `app/__init__.py`
3. Add authentication and validation

### Code Style

Follow PEP 8 guidelines:
```bash
# Install development dependencies
pip install flake8 black

# Check code style
flake8 app/

# Format code
black app/
```

## 🐛 Troubleshooting

### Common Issues

#### Redis Connection Failed
```
Error: redis.ConnectionError: Connection refused
```
**Solution**: Ensure Redis is running
```bash
docker-compose up -d redis
```

#### Database Lock Errors (SQLite)
```
Error: database is locked
```
**Solution**: Use PostgreSQL for concurrent access or implement connection pooling

#### SMTP Authentication Failed
```
Error: smtplib.SMTPAuthenticationError
```
**Solution**: Verify email credentials and enable app passwords for Gmail

#### Celery Tasks Not Processing
**Solution**: Check worker logs and Redis connectivity
```bash
docker-compose logs celery_worker
docker-compose exec redis redis-cli ping
```

### Debug Mode

Enable detailed logging:
```bash
export FLASK_DEBUG=true
export LOG_LEVEL=DEBUG
```

### Performance Tuning

1. **Gunicorn Workers**: Adjust based on CPU cores
   ```dockerfile
   CMD ["gunicorn", "-w", "8", "-b", "0.0.0.0:5000", "run:app"]
   ```

2. **Database Connection Pooling**: Configure SQLAlchemy pool settings

3. **Redis Persistence**: Enable Redis AOF for task persistence

## 📊 API Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 500 | Internal Server Error |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Follow PEP 8 style guidelines
4. Add tests for new functionality
5. Update documentation
6. Submit pull request

## 📄 License

This project is intended for enterprise use. All rights reserved.

## 📞 Support

For support and questions:
- Check application logs: `docker-compose logs -f`
- Review API documentation above
- Test with provided scripts: `python test_api.py`

---

**Version**: 1.0.0
**Last Updated**: November 2025
**Maintained by**: Cosmic Striker 
