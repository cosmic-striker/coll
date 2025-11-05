#!/usr/bin/env python3
"""
Simple server starter script
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
    
    print("Creating Flask application...")
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
            print('Created default admin user (username: admin, password: admin123)')
        
        print('Database initialized successfully')
    
    print(f"Starting Flask server on http://127.0.0.1:5000")
    print("Press CTRL+C to stop the server")
    print("-" * 60)
    
    # Run the Flask app without reloader to avoid issues on Windows
    # Using 127.0.0.1 instead of 0.0.0.0 for Windows compatibility
    try:
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False, threaded=True)
    except OSError as e:
        print(f"OSError while starting server: {e}")
        if "10048" in str(e) or "Address already in use" in str(e):
            print("\nPort 5000 is already in use. Trying port 5001...")
            app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False, threaded=True)
        else:
            raise
    
except KeyboardInterrupt:
    print("\nServer stopped by user")
    sys.exit(0)
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
