#!/usr/bin/env python3
"""
Complete Application Startup Script

This script:
1. Initializes the database
2. Creates default admin user
3. Starts the Flask development server

For production, use gunicorn or waitress instead.
"""

import os
import sys
import logging
from app import create_app, db
from app.models import User, Device, Camera

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_database(app):
    """Initialize database with tables and default data"""
    with app.app_context():
        try:
            # Create all tables
            logger.info("Creating database tables...")
            db.create_all()
            logger.info("Database tables created successfully")
            
            # Create default admin user if none exists
            if not User.query.filter_by(username='admin').first():
                logger.info("Creating default admin user...")
                admin_user = User(
                    username='admin',
                    email='admin@example.com',
                    role='admin'
                )
                admin_user.set_password('Admin@123')  # Strong default password
                db.session.add(admin_user)
                db.session.commit()
                logger.info('✓ Created default admin user')
                logger.info('  Username: admin')
                logger.info('  Password: Admin@123')
                logger.info('  IMPORTANT: Change this password after first login!')
            else:
                logger.info("Admin user already exists")
            
            # Create demo operator user if none exists
            if not User.query.filter_by(username='operator').first():
                logger.info("Creating demo operator user...")
                operator_user = User(
                    username='operator',
                    email='operator@example.com',
                    role='operator'
                )
                operator_user.set_password('Operator@123')
                db.session.add(operator_user)
                db.session.commit()
                logger.info('✓ Created operator user')
                logger.info('  Username: operator')
                logger.info('  Password: Operator@123')
            
            # Create demo viewer user if none exists
            if not User.query.filter_by(username='viewer').first():
                logger.info("Creating demo viewer user...")
                viewer_user = User(
                    username='viewer',
                    email='viewer@example.com',
                    role='viewer'
                )
                viewer_user.set_password('Viewer@123')
                db.session.add(viewer_user)
                db.session.commit()
                logger.info('✓ Created viewer user')
                logger.info('  Username: viewer')
                logger.info('  Password: Viewer@123')
            
            logger.info('✓ Database initialized successfully')
            
        except Exception as e:
            logger.error(f'✗ Database initialization failed: {str(e)}')
            sys.exit(1)

def check_environment():
    """Check and display environment configuration"""
    logger.info("=" * 60)
    logger.info("Environment Configuration:")
    logger.info("=" * 60)
    
    env_vars = {
        'FLASK_ENV': os.environ.get('FLASK_ENV', 'development'),
        'FLASK_DEBUG': os.environ.get('FLASK_DEBUG', 'false'),
        'DATABASE_URL': os.environ.get('DATABASE_URL', 'sqlite:///devices.db'),
        'PORT': os.environ.get('PORT', '5000'),
        'CELERY_BROKER_URL': os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    }
    
    for key, value in env_vars.items():
        # Mask sensitive values
        if 'PASSWORD' in key or 'SECRET' in key:
            value = '***HIDDEN***'
        logger.info(f"  {key}: {value}")
    
    logger.info("=" * 60)

def main():
    """Main entry point"""
    logger.info("Starting Device Monitoring Application...")
    
    # Check environment
    check_environment()
    
    # Create Flask app
    config_class = 'app.config.Config'
    logger.info(f"Loading configuration: {config_class}")
    app = create_app(config_class)
    
    # Initialize database
    init_database(app)
    
    # Get configuration
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info("=" * 60)
    logger.info("Application Ready!")
    logger.info("=" * 60)
    logger.info(f"  Server: http://localhost:{port}")
    logger.info(f"  API Documentation: http://localhost:{port}/api/health")
    logger.info(f"  Debug Mode: {debug_mode}")
    logger.info("=" * 60)
    logger.info("\nAPI Endpoints:")
    logger.info("  Authentication:")
    logger.info("    POST   /api/auth/login")
    logger.info("    POST   /api/auth/refresh")
    logger.info("    GET    /api/auth/profile")
    logger.info("    GET    /api/auth/users")
    logger.info("    POST   /api/auth/users")
    logger.info("  Devices:")
    logger.info("    GET    /api/devices/")
    logger.info("    POST   /api/devices/")
    logger.info("    GET    /api/devices/<id>")
    logger.info("    PUT    /api/devices/<id>")
    logger.info("    DELETE /api/devices/<id>")
    logger.info("    POST   /api/devices/<id>/poll")
    logger.info("    GET    /api/devices/status")
    logger.info("  Cameras:")
    logger.info("    GET    /api/cameras/")
    logger.info("    POST   /api/cameras/")
    logger.info("    GET    /api/cameras/<id>")
    logger.info("    PUT    /api/cameras/<id>")
    logger.info("    DELETE /api/cameras/<id>")
    logger.info("    POST   /api/cameras/<id>/test")
    logger.info("    GET    /api/cameras/status")
    logger.info("  Alerts:")
    logger.info("    GET    /api/alerts/")
    logger.info("    POST   /api/alerts/")
    logger.info("    GET    /api/alerts/<id>")
    logger.info("    POST   /api/alerts/<id>/acknowledge")
    logger.info("    POST   /api/alerts/acknowledge-all")
    logger.info("    GET    /api/alerts/summary")
    logger.info("=" * 60)
    logger.info("\nPress CTRL+C to stop the server\n")
    
    # Start Flask app
    try:
        app.run(host=host, port=port, debug=debug_mode)
    except KeyboardInterrupt:
        logger.info("\nShutting down gracefully...")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
