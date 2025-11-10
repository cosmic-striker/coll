from flask import Flask, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from celery import Celery
import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)

celery = None  # initialized in create_app


def create_app(config_class=None):
    # Get absolute path to frontend directory
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_root = os.path.dirname(backend_dir)
    frontend_path = os.path.join(project_root, 'frontend', 'public')
    
    app = Flask(__name__,
                template_folder=frontend_path)
    app.config.from_object(config_class or 'app.config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)

    # Configure CORS
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

    # Configure logging
    configure_logging(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.devices import devices_bp
    from app.routes.cameras import cameras_bp
    from app.routes.alerts import alerts_bp
    from app.routes.settings import settings_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(devices_bp, url_prefix='/api/devices')
    app.register_blueprint(cameras_bp, url_prefix='/api/cameras')
    app.register_blueprint(alerts_bp, url_prefix='/api/alerts')
    app.register_blueprint(settings_bp, url_prefix='/api/settings')

    # Initialize Celery
    global celery
    celery = make_celery(app)

    # Add security headers
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })

    @app.route('/api/health')
    def api_health_check():
        try:
            # Check database connectivity
            db.session.execute('SELECT 1')
            db_status = 'connected'
        except Exception as e:
            db_status = f'error: {str(e)}'
        
        return jsonify({
            'status': 'healthy',
            'database': db_status,
            'timestamp': datetime.now().isoformat()
        })

    # Serve frontend files
    @app.route('/')
    def index():
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_root = os.path.dirname(backend_dir)
        frontend_path = os.path.join(project_root, 'frontend', 'public')
        index_path = os.path.join(frontend_path, 'index.html')
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                return f.read()
        return 'Index file not found. Please check if frontend is properly set up.', 404

    @app.route('/<path:path>')
    def serve_static(path):
        # Don't serve API routes as static files
        if path.startswith('api/'):
            return {'error': 'Not found'}, 404
        # Skip Flask's default static files
        if path.startswith('static/'):
            return {'error': 'Not found'}, 404
        
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_root = os.path.dirname(backend_dir)
        frontend_path = os.path.join(project_root, 'frontend', 'public')
        file_path = os.path.join(frontend_path, path)
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
            # Set appropriate content type
            if path.endswith('.js'):
                return content, 200, {'Content-Type': 'application/javascript'}
            elif path.endswith('.css'):
                return content, 200, {'Content-Type': 'text/css'}
            elif path.endswith('.html'):
                return content, 200, {'Content-Type': 'text/html'}
            else:
                return content
        # For SPA routing, serve index.html for non-API routes
        if not path.startswith('api/'):
            index_path = os.path.join(frontend_path, 'index.html')
            if os.path.exists(index_path):
                with open(index_path, 'r', encoding='utf-8') as f:
                    return f.read()
        return {'error': 'Not found'}, 404

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


# Export celery instance for external access
def get_celery_app():
    """Get the global celery app instance"""
    return celery
