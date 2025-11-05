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
from app import create_app
from celery.schedules import crontab

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

# Create Flask app with proper configuration
app = create_app('app.config.Config')

# Get the Celery instance from the app
from app import celery

# Configure Celery beat schedule for periodic tasks
celery.conf.beat_schedule = {
    'poll-all-devices': {
        'task': 'app.services.poller.poll_all_devices',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
    'poll-all-cameras': {
        'task': 'app.services.poller.poll_all_cameras',
        'schedule': crontab(minute='*/10'),  # Every 10 minutes
    },
    'send-daily-summary': {
        'task': 'app.services.alerting.send_daily_summary',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight
    },
}

celery.conf.timezone = 'UTC'

# Import tasks to ensure they are registered with Celery
with app.app_context():
    import app.services.poller
    import app.services.alerting
    logging.info("Celery tasks imported successfully")

if __name__ == '__main__':
    # This allows running the worker directly with python
    celery.start()
