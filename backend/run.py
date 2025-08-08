#!/usr/bin/env python3
"""
Flask Application Entry Point

This module creates and runs the Flask application for the device monitoring system.
It supports both development and production environments.

Environment Variables:
    FLASK_ENV: Environment (development/production)
    FLASK_DEBUG: Debug mode (true/false)
    PORT: Port to run the application on
"""

import os
import logging
from app import create_app, db

# Create Flask app with appropriate configuration
config_name = os.environ.get('FLASK_ENV', 'app.config.Config')
app = create_app(config_name)

def init_database():
    """Initialize database with tables and default data"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            
            # Create default admin user if none exists
            from app.models import User
            if not User.query.filter_by(username='admin').first():
                admin_user = User(
                    username='admin',
                    email='admin@example.com',
                    role='admin'
                )
                admin_user.set_password('admin123')  # Change this in production!
                db.session.add(admin_user)
                db.session.commit()
                app.logger.info('Created default admin user (username: admin, password: admin123)')
            
            app.logger.info('Database initialized successfully')
            
        except Exception as e:
            app.logger.error(f'Database initialization failed: {str(e)}')

if __name__ == '__main__':
    # Initialize database on startup
    init_database()
    
    # Get configuration from environment
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    
    if debug_mode:
        app.logger.info('Starting Flask app in development mode')
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        app.logger.info('Starting Flask app in production mode')
        app.run(host='0.0.0.0', port=port, debug=False)
