# Device Monitoring System - Quick Start Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- (Optional) Redis for Celery background tasks

### Installation Steps

1. **Navigate to backend directory**
   ```powershell
   cd f:\sen5\coll\coll\backend
   ```

2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Start the application**
   ```powershell
   python start.py
   ```

The application will:
- Create the database automatically
- Set up default users (admin, operator, viewer)
- Start the web server on http://localhost:5000

### Default User Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | Admin@123 | Administrator (full access) |
| operator | Operator@123 | Operator (can manage devices/cameras) |
| viewer | Viewer@123 | Viewer (read-only access) |

**⚠️ IMPORTANT: Change these passwords after first login!**

## 📋 Testing the Application

### Test All Endpoints
```powershell
python test_endpoints.py
```

This script will:
- Test all API endpoints
- Create test data
- Verify functionality
- Clean up test data

### Manual Testing

1. **Health Check**
   ```powershell
   curl http://localhost:5000/health
   curl http://localhost:5000/api/health
   ```

2. **Login (Get Auth Token)**
   ```powershell
   curl -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"Admin@123\"}"
   ```

3. **Access Protected Endpoint**
   ```powershell
   curl -H "Authorization: Bearer YOUR_TOKEN_HERE" http://localhost:5000/api/devices/
   ```

## 🎯 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/profile` - Get current user profile
- `GET /api/auth/users` - List all users (admin only)
- `POST /api/auth/users` - Create new user (admin only)
- `PUT /api/auth/users/<id>` - Update user (admin only)
- `DELETE /api/auth/users/<id>` - Delete user (admin only)

### Devices
- `GET /api/devices/` - List all devices
- `POST /api/devices/` - Create new device (operator+)
- `GET /api/devices/<id>` - Get device details
- `PUT /api/devices/<id>` - Update device (operator+)
- `DELETE /api/devices/<id>` - Delete device (admin only)
- `POST /api/devices/<id>/poll` - Poll device status (operator+)
- `GET /api/devices/status` - Get device status summary

### Cameras
- `GET /api/cameras/` - List all cameras
- `POST /api/cameras/` - Create new camera (operator+)
- `GET /api/cameras/<id>` - Get camera details
- `PUT /api/cameras/<id>` - Update camera (operator+)
- `DELETE /api/cameras/<id>` - Delete camera (admin only)
- `POST /api/cameras/<id>/test` - Test camera connection (operator+)
- `GET /api/cameras/<id>/stream` - Get camera stream info
- `GET /api/cameras/status` - Get camera status summary

### Alerts
- `GET /api/alerts/` - List alerts (supports pagination & filters)
- `POST /api/alerts/` - Create alert (operator+)
- `GET /api/alerts/<id>` - Get alert details
- `POST /api/alerts/<id>/acknowledge` - Acknowledge alert (operator+)
- `POST /api/alerts/acknowledge-all` - Acknowledge multiple alerts (operator+)
- `DELETE /api/alerts/<id>` - Delete alert (admin only)
- `GET /api/alerts/summary` - Get alerts summary

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=true
SECRET_KEY=your-secret-key-here
PORT=5000

# Database
DATABASE_URL=sqlite:///devices.db

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-here

# Celery (Optional - for background tasks)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email Alerts (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ALERT_EMAIL_FROM=alerts@example.com
ALERT_EMAIL_TO=admin@example.com

# Slack Alerts (Optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

## 🔄 Background Tasks (Optional)

If you want to enable background polling and alerts:

### 1. Install and Start Redis
```powershell
# Using Docker
docker run -d -p 6379:6379 redis:alpine

# Or install Redis for Windows
```

### 2. Start Celery Worker
```powershell
celery -A celery_worker.celery worker --loglevel=info --pool=solo
```

### 3. Start Celery Beat (Scheduler)
```powershell
celery -A celery_worker.celery beat --loglevel=info
```

## 📊 Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration
│   ├── models.py            # Database models
│   ├── routes/              # API endpoints
│   │   ├── auth.py          # Authentication routes
│   │   ├── devices.py       # Device routes
│   │   ├── cameras.py       # Camera routes
│   │   └── alerts.py        # Alert routes
│   └── services/            # Background services
│       ├── poller.py        # Device/camera polling
│       └── alerting.py      # Alert notifications
├── start.py                 # Main startup script
├── test_endpoints.py        # Endpoint testing script
├── celery_worker.py         # Celery worker configuration
└── requirements.txt         # Python dependencies
```

## 🐛 Troubleshooting

### Database Issues
```powershell
# Delete existing database and recreate
Remove-Item instance/devices.db
python start.py
```

### Port Already in Use
```powershell
# Use a different port
$env:PORT="5001"; python start.py
```

### Import Errors
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Check Logs
Application logs are stored in `logs/backend.log`

## 🎨 Frontend Access

After starting the backend, access the web interface at:
- **Home**: http://localhost:5000
- **Dashboard**: http://localhost:5000/dashboard.html
- **Devices**: http://localhost:5000/devices.html
- **Cameras**: http://localhost:5000/cameras.html
- **Alerts**: http://localhost:5000/alerts.html

## 📝 Development Tips

### Run in Debug Mode
```powershell
$env:FLASK_DEBUG="true"; python start.py
```

### Test Specific Endpoint
```powershell
# PowerShell
$token = (Invoke-RestMethod -Method Post -Uri "http://localhost:5000/api/auth/login" -Body (@{username="admin";password="Admin@123"} | ConvertTo-Json) -ContentType "application/json").access_token

Invoke-RestMethod -Uri "http://localhost:5000/api/devices/" -Headers @{Authorization="Bearer $token"}
```

### View Database
```powershell
# Install sqlite3 or use DB Browser for SQLite
sqlite3 instance/devices.db
.tables
SELECT * FROM user;
```

## 🔒 Security Notes

1. **Change default passwords** immediately
2. **Set strong SECRET_KEY** and **JWT_SECRET_KEY** in production
3. **Use HTTPS** in production (configure reverse proxy like nginx)
4. **Enable rate limiting** for API endpoints
5. **Regular backups** of the database
6. **Monitor logs** for suspicious activity

## 📞 Support

For issues or questions:
1. Check the logs: `logs/backend.log`
2. Run the test script: `python test_endpoints.py`
3. Review the API documentation in this README

## 🎉 Success Checklist

- [ ] Dependencies installed
- [ ] Application starts without errors
- [ ] Can access http://localhost:5000/health
- [ ] Can login with default credentials
- [ ] All endpoint tests pass
- [ ] Frontend pages load correctly
- [ ] Changed default passwords

**Your application should now be running successfully! 🚀**
