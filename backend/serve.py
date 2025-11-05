#!/usr/bin/env python3
"""
Production server starter using Waitress (Windows-compatible)
"""
import os
import sys

# Set environment variables
os.environ['FLASK_DEBUG'] = 'False'
os.environ['FLASK_ENV'] = 'production'

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from waitress import serve
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
    print(f"  - Server: Waitress (Production WSGI Server)")
    print("-" * 70)
    print("\n[STARTING] Server starting...")
    print("[RUNNING] The server is now running and accepting connections")
    print("[STOP] Press CTRL+C to stop the server\n")
    print("=" * 70)
    
    # Serve the application using Waitress
    try:
        print("[DEBUG] About to call waitress.serve()...")
        print(f"[DEBUG] App object type: {type(app)}")
        print(f"[DEBUG] App is callable: {callable(app)}")
        print(f"[DEBUG] App name: {app.name}")
        
        # Test if app works
        with app.test_client() as client:
            resp = client.get('/')
            print(f"[DEBUG] Test request status: {resp.status_code}")
        
        print("[DEBUG] Starting waitress...")
        serve(app, host='0.0.0.0', port=5000, threads=4, _quiet=False)
        print("[DEBUG] waitress.serve() returned (this shouldn't print)")
    except Exception as serve_error:
        print(f"\n[ERROR] Waitress server error: {serve_error}")
        import traceback
        traceback.print_exc()
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
