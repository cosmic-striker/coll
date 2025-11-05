import os
import secrets

class Config:
    # Generate secure secrets if not provided
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///devices.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Generate secure JWT secret if not provided
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or secrets.token_hex(32)

    # Security headers
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # JWT configuration
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7

    # Celery (new-style config)
    broker_url = os.environ.get('CELERY_BROKER_URL', os.environ.get('broker_url', 'redis://localhost:6379/0'))
    result_backend = os.environ.get('CELERY_RESULT_BACKEND', os.environ.get('result_backend', 'redis://localhost:6379/0'))
    imports = (
        'app.services.poller',
        'app.services.alerting',
    )

    POLL_INTERVAL_SECONDS = 60  # polling interval, configurable
    ALERT_EMAIL_FROM = os.environ.get('ALERT_EMAIL_FROM', 'alerts@example.com')
    ALERT_EMAIL_TO = os.environ.get('ALERT_EMAIL_TO', 'admin@example.com')

    # Rate limiting (can be implemented later)
    RATELIMIT_DEFAULT = "100 per minute"
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

    # CORS settings (if needed for frontend)
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000').split(',')

    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/backend.log')
