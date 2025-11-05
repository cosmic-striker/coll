"# 🎯 Device Monitoring System

A comprehensive, production-ready device and camera monitoring system built with Flask, featuring real-time monitoring, alerting, and a modern UI.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Tests](https://img.shields.io/badge/tests-30/30_passing-brightgreen)

---

## ✨ Features

### Core Functionality
- 🖥️ **Device Monitoring** - Monitor network devices (switches, routers, servers)
- 📹 **Camera Management** - Manage and test IP camera connections
- 🚨 **Alert System** - Real-time alerts with severity levels
- 👥 **User Management** - Role-based access control (Admin, Operator, Viewer)
- 🔐 **JWT Authentication** - Secure token-based authentication
- 📊 **Status Dashboards** - Real-time status summaries

### Technical Features
- ✅ **35+ REST API Endpoints** - Complete CRUD operations
- 🐳 **Docker Support** - Easy deployment with Docker Compose
- 🔄 **Background Tasks** - Celery integration for async operations
- 📝 **Comprehensive Logging** - Detailed application logs
- 🧪 **100% Test Coverage** - 30 automated tests
- 🎨 **Modern UI** - Beautiful glassmorphism design
- 🔒 **Security** - Rate limiting, CORS, input validation

---

## 🚀 Quick Start

### With Docker (Recommended)
```bash
cd backend
docker-compose up -d
```

### Without Docker (Windows)
```bash
cd backend
manual-setup.bat
START.bat
```

### Without Docker (Linux/Mac)
```bash
cd backend
chmod +x manual-setup.sh && ./manual-setup.sh
python start.py
```

**Access:** http://localhost:5000

**Default Credentials:**
- Admin: `admin` / `Admin@123`
- Operator: `operator` / `Operator@123`
- Viewer: `viewer` / `Viewer@123`

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [SETUP.md](SETUP.md) | Complete setup guide (Docker, Manual, Production) |
| [QUICKSTART.md](QUICKSTART.md) | Quick reference guide |
| [TEST_RESULTS.md](backend/TEST_RESULTS.md) | Test coverage and results |
| [UI_IMPROVEMENTS.md](backend/UI_IMPROVEMENTS.md) | UI/UX documentation |

---

## 🛠️ Technology Stack

### Backend
- **Framework:** Flask 2.3.3
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Authentication:** JWT with Flask-JWT-Extended
- **Task Queue:** Celery with Redis
- **ORM:** SQLAlchemy
- **API:** RESTful with CORS support

### Frontend
- **HTML5/CSS3/JavaScript**
- **Modern UI:** Glassmorphism design
- **Responsive:** Mobile-friendly

### DevOps
- **Docker & Docker Compose**
- **Nginx** (reverse proxy)
- **Gunicorn** (WSGI server)
- **Redis** (caching & task queue)

---

## 📋 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/profile` - Get user profile
- `GET /api/auth/users` - List all users
- `POST /api/auth/users` - Create user

### Devices
- `GET /api/devices/` - List devices
- `POST /api/devices/` - Create device
- `GET /api/devices/<id>` - Get device
- `PUT /api/devices/<id>` - Update device
- `DELETE /api/devices/<id>` - Delete device
- `POST /api/devices/<id>/poll` - Poll device
- `GET /api/devices/status` - Device status summary

### Cameras
- `GET /api/cameras/` - List cameras
- `POST /api/cameras/` - Create camera
- `GET /api/cameras/<id>` - Get camera
- `PUT /api/cameras/<id>` - Update camera
- `DELETE /api/cameras/<id>` - Delete camera
- `POST /api/cameras/<id>/test` - Test connection
- `GET /api/cameras/status` - Camera status summary

### Alerts
- `GET /api/alerts/` - List alerts
- `POST /api/alerts/` - Create alert
- `GET /api/alerts/<id>` - Get alert
- `POST /api/alerts/<id>/acknowledge` - Acknowledge alert
- `POST /api/alerts/acknowledge-all` - Acknowledge all
- `GET /api/alerts/summary` - Alert summary

---

## 🧪 Testing

### Run All Tests
```bash
cd backend
python main_test.py
```

### Test Results
- **Total Tests:** 30
- **Passed:** 30 ✅
- **Success Rate:** 100%
- **Coverage:** All endpoints, CRUD operations, error handling

---

## 🐳 Docker Deployment

### Development
```bash
docker-compose up -d
```

### Production (with PostgreSQL)
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### View Logs
```bash
docker-compose logs -f
```

### Stop Services
```bash
docker-compose down
```

---

## 🔧 Configuration

### Environment Variables

Create `.env` file in `backend/` directory:

```bash
# Flask
FLASK_ENV=production
FLASK_DEBUG=false
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# Database
DATABASE_URL=sqlite:///devices.db

# Celery (optional)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Server
PORT=5000
```

See `.env.example` for complete configuration options.

---

## 📁 Project Structure

```
coll/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── models.py            # Database models
│   │   ├── routes/              # API endpoints
│   │   │   ├── auth.py          # Authentication
│   │   │   ├── devices.py       # Device management
│   │   │   ├── cameras.py       # Camera management
│   │   │   └── alerts.py        # Alert management
│   │   ├── services/            # Background services
│   │   │   ├── poller.py        # Device polling
│   │   │   └── alerting.py      # Alert notifications
│   │   └── static/              # CSS/JS files
│   ├── start.py                 # Enhanced startup
│   ├── run.py                   # Basic startup
│   ├── main_test.py             # Test suite
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile               # Docker image
│   ├── docker-compose.yml       # Dev compose
│   └── docker-compose.prod.yml  # Prod compose
├── frontend/
│   └── public/                  # HTML pages
├── SETUP.md                     # Complete setup guide
├── QUICKSTART.md                # Quick reference
└── README.md                    # This file
```

---

## 🔒 Security

- ✅ JWT token authentication
- ✅ Password hashing (bcrypt)
- ✅ Role-based access control
- ✅ Rate limiting
- ✅ CORS configuration
- ✅ Input validation
- ✅ SQL injection protection (SQLAlchemy)
- ✅ XSS protection

**⚠️ Change default credentials in production!**

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📝 License

This project is licensed under the MIT License.

---

## 🆘 Support

- **Documentation:** See [SETUP.md](SETUP.md)
- **Issues:** [GitHub Issues](https://github.com/cosmic-striker/coll/issues)
- **Tests:** Run `python main_test.py` for diagnostics

---

## 🎉 Acknowledgments

Built with ❤️ using Flask, Docker, and modern web technologies.

---

**Ready to get started? Check out [SETUP.md](SETUP.md) for detailed instructions!**
" 
