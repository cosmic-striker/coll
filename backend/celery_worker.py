#!/usr/bin/env python3
"""
Celery Worker Entry Point

This module initializes the Celery worker with the Flask application context
for background task processing including device polling and alert notifications.

Usage:
    celery -A celery_worker.celery worker --loglevel=info
    celery -A celery_worker.celery beat --loglevel=info (for scheduled tasks)
"""

import os
import logging
from app import create_app, make_celery

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

# Create Flask app with proper configuration
config_name = os.environ.get('FLASK_ENV', 'app.config.Config')
app = create_app(config_name)

# Initialize Celery with Flask app context
celery = make_celery(app)

# Import tasks to ensure they are registered
with app.app_context():
    import app.services.poller
    import app.services.alerting

if __name__ == '__main__':
    # This allows running the worker directly with python
    celery.start()
