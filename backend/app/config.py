import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///devices.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')

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

    # Add SMTP and Slack config here if needed
