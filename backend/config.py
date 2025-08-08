import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///devices.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')

    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

    POLL_INTERVAL_SECONDS = 60  # polling interval, configurable
    ALERT_EMAIL_FROM = os.environ.get('ALERT_EMAIL_FROM', 'alerts@example.com')
    ALERT_EMAIL_TO = os.environ.get('ALERT_EMAIL_TO', 'admin@example.com')

    # Add SMTP and Slack config here if needed
