# Device Monitoring Backend

A production-ready Flask backend API for centralized monitoring of network devices and IP cameras.

## Features

- **Device Management**: CRUD operations for network devices with SNMP support
- **Camera Management**: IP camera monitoring with RTSP stream management
- **Real-time Polling**: Background tasks for device health checks using Celery
- **Alert System**: Automated alerting with email and Slack notifications
- **Role-based Access Control**: JWT authentication with admin/operator/viewer roles
- **Production Ready**: Dockerized with Redis, comprehensive logging, and error handling

## Technology Stack

- **Framework**: Flask 2.3.3 with app factory pattern
- **Database**: SQLAlchemy with SQLite (extensible to PostgreSQL)
- **Authentication**: Flask-JWT-Extended with role-based access
- **Background Tasks**: Celery with Redis broker
- **Containerization**: Docker with Docker Compose
- **Production Server**: Gunicorn WSGI server

## Quick Start

### Prerequisites

- Python 3.10+
- Docker and Docker Compose
- Redis (handled by Docker Compose)

### Local Development Setup

1. **Clone and navigate to the project**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   export FLASK_ENV=development
   export FLASK_DEBUG=true
   export SECRET_KEY=your-secret-key
   export JWT_SECRET_KEY=your-jwt-secret
   ```

5. **Initialize database**
   ```bash
   python run.py
   ```

6. **Run Redis (in separate terminal)**
   ```bash
   docker run -d -p 6379:6379 redis:7
   ```

7. **Run Celery worker (in separate terminal)**
   ```bash
   celery -A celery_worker.celery worker --loglevel=info
   ```

8. **Run Celery beat for scheduled tasks (in separate terminal)**
   ```bash
   celery -A celery_worker.celery beat --loglevel=info
   ```

### Docker Deployment (Recommended)

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **View logs**
   ```bash
   docker-compose logs -f backend
   ```

3. **Scale Celery workers**
   ```bash
   docker-compose up -d --scale celery_worker=3
   ```

## API Documentation

### Authentication

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

#### Get Profile
```http
GET /api/auth/profile
Authorization: Bearer <token>
```

### Device Management

#### List Devices
```http
GET /api/devices/
Authorization: Bearer <token>
```

#### Create Device
```http
POST /api/devices/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Switch-01",
  "ip_address": "192.168.1.10",
  "vendor": "Cisco",
  "device_type": "switch",
  "snmp_community": "public"
}
```

#### Poll Device
```http
POST /api/devices/1/poll
Authorization: Bearer <token>
```

### Camera Management

#### List Cameras
```http
GET /api/cameras/
Authorization: Bearer <token>
```

#### Create Camera
```http
POST /api/cameras/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Camera-01",
  "ip_address": "192.168.1.20",
  "rtsp_url": "rtsp://192.168.1.20:554/stream1",
  "username": "admin",
  "password": "password",
  "location": "Main Entrance"
}
```

### Alert Management

#### List Alerts
```http
GET /api/alerts/?page=1&per_page=20&severity=high
Authorization: Bearer <token>
```

#### Acknowledge Alert
```http
POST /api/alerts/1/acknowledge
Authorization: Bearer <token>
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment (development/production) | development |
| `FLASK_DEBUG` | Debug mode | false |
| `SECRET_KEY` | Flask secret key | auto-generated |
| `JWT_SECRET_KEY` | JWT secret key | auto-generated |
| `DATABASE_URL` | Database connection string | sqlite:///devices.db |
| `CELERY_BROKER_URL` | Redis broker URL | redis://redis:6379/0 |
| `CELERY_RESULT_BACKEND` | Redis result backend | redis://redis:6379/0 |
| `SMTP_SERVER` | SMTP server for email alerts | smtp.gmail.com |
| `SMTP_PORT` | SMTP port | 587 |
| `SMTP_USERNAME` | SMTP username | - |
| `SMTP_PASSWORD` | SMTP password | - |
| `ALERT_EMAIL_FROM` | Email sender address | alerts@example.com |
| `ALERT_EMAIL_TO` | Email recipient address | admin@example.com |
| `SLACK_WEBHOOK_URL` | Slack webhook for notifications | - |

### Default Users

The system creates a default admin user on first startup:
- **Username**: admin
- **Password**: admin123 (change immediately in production!)
- **Role**: admin

## User Roles

- **Admin**: Full access to all operations including user management
- **Operator**: Can create, update, and poll devices/cameras, acknowledge alerts
- **Viewer**: Read-only access to devices, cameras, and alerts

## Background Tasks

### Polling Schedule

- **Device Polling**: Every 5 minutes
- **Camera Polling**: Every 10 minutes
- **Daily Summary**: Once per day at midnight

### Manual Task Triggers

- Device polling can be triggered via API endpoints
- Camera connection tests can be initiated on-demand
- Alerts are sent immediately for high/critical severity events

## Production Deployment

### Security Considerations

1. **Change Default Credentials**: Update admin password immediately
2. **Environment Variables**: Use proper secret management
3. **HTTPS**: Configure reverse proxy with SSL/TLS
4. **Database**: Use PostgreSQL for production
5. **Monitoring**: Set up application monitoring and logging

### Scaling

- **Horizontal Scaling**: Add more Celery workers
- **Database**: Migrate to PostgreSQL with connection pooling
- **Redis**: Use Redis Cluster for high availability
- **Load Balancing**: Use nginx or similar for multiple Flask instances

### Monitoring

The application provides comprehensive logging:
- Application logs: `logs/backend.log`
- Celery worker logs via Docker Compose
- Database query logging (debug mode)

## Development

### Adding New Device Types

1. Extend the `Device` model in `app/models.py`
2. Add device-specific polling logic in `app/services/poller.py`
3. Update API endpoints in `app/routes/devices.py`

### Adding New Alert Channels

1. Implement new notification function in `app/services/alerting.py`
2. Add configuration variables
3. Update the `send_alert_notification` task

### Database Migrations

```bash
# Create migration
flask db migrate -m "Add new field"

# Apply migration
flask db upgrade
```

## Troubleshooting

### Common Issues

1. **Redis Connection Error**: Ensure Redis is running and accessible
2. **Database Lock**: SQLite limitations in concurrent environments
3. **SMTP Authentication**: Verify email credentials and app passwords
4. **Celery Tasks Not Running**: Check worker logs and Redis connectivity

### Debug Mode

Enable debug logging:
```bash
export FLASK_DEBUG=true
export LOG_LEVEL=DEBUG
```

### Health Checks

- Flask app: `GET /api/auth/profile` (requires authentication)
- Redis: Check Docker container logs
- Celery: Monitor task execution in worker logs

## Contributing

1. Follow PEP 8 style guidelines
2. Add tests for new features
3. Update documentation
4. Ensure Docker builds successfully

## License

This project is intended for enterprise use. All rights reserved."# col" 
