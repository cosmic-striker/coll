# 🚀 How to Run the Device Monitoring System

## Quick Start Guide

### Step 1: Start the Backend Server

Open PowerShell and run:

```powershell
cd f:\sen5\coll\net\coll\backend
python run.py
```

You should see output like:
```
[2025-11-08 23:06:48,527] INFO in run: Database initialized successfully
[2025-11-08 23:06:48,528] INFO in run: Starting Flask app in production mode
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://0.0.0.0:5000
```

### Step 2: Open in Browser

Open your web browser and navigate to:
```
http://localhost:5000
```

### Step 3: Login

Use one of these default credentials:

**Admin Account** (Full access including Settings):
- Username: `admin`
- Password: `Admin@123`

**Operator Account** (Can manage devices/cameras):
- Username: `operator`
- Password: `Operator@123`

**Viewer Account** (Read-only access):
- Username: `viewer`
- Password: `Viewer@123`

---

## 📋 Available Pages

Once logged in, you can access:

1. **Dashboard** - Overview of devices, cameras, and alerts
2. **Devices** - Manage network devices
3. **Cameras** - Manage IP cameras
4. **Alerts** - View and manage system alerts
5. **Settings** - Configure system settings (Admin only) ✨ **NOW WORKING!**
6. **Users** - Manage users (Admin only)

---

## 🔧 Troubleshooting

### Port Already in Use

If you see an error about port 5000 being in use:

```powershell
# Use a different port
$env:PORT="8080"
python run.py
```

Then access at: `http://localhost:8080`

### Module Not Found Errors

If you get import errors, install dependencies:

```powershell
pip install -r requirements.txt
```

### Database Issues

If you have database problems:

```powershell
# Delete the old database
Remove-Item -Force instance\devices.db

# Restart the server (it will create a new database)
python run.py
```

---

## 🛑 How to Stop the Server

Press `Ctrl + C` in the terminal where the server is running.

---

## ✨ Recent Fixes Applied

✅ **Settings page now works** - All API endpoints implemented
✅ **Logout improved** - Shows notification before redirecting
✅ **All pages updated** - Consistent logout behavior

---

## 🎯 What's Next?

After logging in:
1. Try the **Settings** page - it should load without errors now!
2. Click **Logout** - you'll see a toast notification
3. Explore the dashboard and other features

Enjoy! 🎉
