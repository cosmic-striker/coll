#!/usr/bin/env python3
"""
Production server using Flask's built-in WSGI server (Windows-compatible)
Note: For production, you should use a proper WSGI server behind a reverse proxy
"""
import os
import sys

# Set environment variables
os.environ['FLASK_DEBUG'] = 'False'
os.environ['FLASK_ENV'] = 'production'

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app import create_app, db
    from app.models import User
    
    print("=" * 70)
    print(" Device Monitoring Backend Server")
    print("=" * 70)
    print("\nCreating Flask application...")
    app = create_app('app.config.Config')
    
    # Initialize database
    with app.app_context():
        print("Initializing database...")
        db.create_all()
        
        # Create default admin user if none exists
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print('[OK] Created default admin user')
            print('  Username: admin')
            print('  Password: admin123')
            print('  [WARNING] CHANGE THIS PASSWORD IN PRODUCTION!')
        else:
            print('[OK] Admin user already exists')
        
        print('[OK] Database initialized successfully\n')
    
    print("-" * 70)
    print("Server Information:")
    print(f"  - Backend API: http://localhost:5000/api")
    print(f"  - Frontend UI: http://localhost:5000")
    print(f"  - Default Credentials: admin / admin123")
    print("-" * 70)
    print("\n[STARTING] Server starting on port 5000...")
    print("[RUNNING] Press CTRL+C to stop the server\n")
    print("=" * 70)
    
    # Run using Flask's built-in server without reloader  
    import time
    import threading
    
    server_error = None
    
    def run_server():
        global server_error
        try:
            from werkzeug.serving import run_simple
            print("[SERVER] Werkzeug server starting...")
            run_simple('0.0.0.0', 5000, app, use_reloader=False, use_debugger=False, threaded=True)
        except Exception as e:
            server_error = e
            print(f"[SERVER ERROR] {e}")
            import traceback
            traceback.print_exc()
    
    # Start server in a thread
    server_thread = threading.Thread(target=run_server, daemon=False)
    server_thread.start()
    
    # Give the server a moment to start
    time.sleep(2)
    
    if server_error:
        raise server_error
    
    print("\n[SUCCESS] Server is running!")
    print("  Access the application at: http://localhost:5000")
    print("  API endpoints at: http://localhost:5000/api")
    print("\n  Press CTRL+C to stop the server\n")
    
    # Keep the main thread alive
    try:
        while server_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[STOP] Received interrupt signal")
        raise
    
except KeyboardInterrupt:
    print("\n\n" + "=" * 70)
    print("[STOPPED] Server stopped by user")
    print("=" * 70)
    sys.exit(0)
except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
