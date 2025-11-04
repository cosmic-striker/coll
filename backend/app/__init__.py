from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from celery import Celery
import logging
from logging.handlers import RotatingFileHandler
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

celery = None  # initialized in create_app


def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object(config_class or 'app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Configure logging
    configure_logging(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.devices import devices_bp
    from app.routes.cameras import cameras_bp
    from app.routes.alerts import alerts_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(devices_bp, url_prefix='/api/devices')
    app.register_blueprint(cameras_bp, url_prefix='/api/cameras')
    app.register_blueprint(alerts_bp, url_prefix='/api/alerts')

    # Initialize Celery
    global celery
    celery = make_celery(app)

    return app


def configure_logging(app):
    """Configure application logging"""
    if not app.debug and not app.testing:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Configure file handler
        file_handler = RotatingFileHandler(
            'logs/backend.log', 
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        # Configure console handler for production
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s'
        ))
        console_handler.setLevel(logging.INFO)
        app.logger.addHandler(console_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Backend application startup')
    
    # Configure werkzeug logger
    logging.getLogger('werkzeug').setLevel(logging.WARNING)


def make_celery(app):
    from celery import Celery

    # Fallbacks to avoid None when Flask drops lowercase config keys
    default_broker = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    default_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    default_imports = ('app.services.poller', 'app.services.alerting')

    broker_url = app.config.get('broker_url') or default_broker
    result_backend = app.config.get('result_backend') or default_backend
    imports = app.config.get('imports') or default_imports

    celery_app = Celery(app.import_name)
    celery_app.conf.update(
        broker_url=broker_url,
        result_backend=result_backend,
        imports=imports,
        timezone='UTC',
        task_serializer='json',
        result_serializer='json',
        accept_content=['json']
    )

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app
