# 🚀 Quick Setup Reference

## Choose Your Setup Method

### 1️⃣ Docker (Recommended - Fastest)
```bash
cd backend
docker-compose up -d
```
**Access:** http://localhost:5000

---

### 2️⃣ Manual Setup (Windows)
```bash
cd backend
manual-setup.bat    # One-time setup
START.bat           # Run application
```
**Access:** http://localhost:5000

---

### 3️⃣ Manual Setup (Linux/Mac)
```bash
cd backend
chmod +x manual-setup.sh
./manual-setup.sh   # One-time setup
./start.sh          # Run application (or python start.py)
```
**Access:** http://localhost:5000

---

## Default Login Credentials

| Role     | Username  | Password      | Access Level        |
|----------|-----------|---------------|---------------------|
| Admin    | admin     | Admin@123     | Full access         |
| Operator | operator  | Operator@123  | Manage devices      |
| Viewer   | viewer    | Viewer@123    | Read-only           |

⚠️ **Change passwords after first login!**

---

## Quick Commands

### Docker
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Rebuild
docker-compose up -d --build
```

### Manual (with virtual environment activated)
```bash
# Start server
python start.py

# Run tests
python main_test.py

# Initialize database
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### Dependencies Not Found
```bash
# Ensure virtual environment is activated
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Then reinstall
pip install -r requirements.txt
```

### Docker Issues
```bash
# Clean everything and restart
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```

---

## Need More Help?

📖 **Full Documentation:** See `SETUP.md` in root directory
🧪 **Testing Guide:** See `TEST_RESULTS.md`
🎨 **UI Guide:** See `UI_IMPROVEMENTS.md`

---

## Project Structure
```
backend/
├── app/                    # Application code
│   ├── routes/            # API endpoints
│   ├── models.py          # Database models
│   └── services/          # Background tasks
├── start.py               # Enhanced startup
├── run.py                 # Basic startup
├── main_test.py           # Test suite
├── docker-compose.yml     # Docker setup
└── requirements.txt       # Dependencies
```

---

**Happy Monitoring! 🎉**
