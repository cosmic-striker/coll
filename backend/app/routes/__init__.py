from .auth import auth_bp
from .devices import devices_bp
from .cameras import cameras_bp
from .alerts import alerts_bp
from .network import network_bp

def register_blueprints(app):
    """Register all blueprint routes"""
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(devices_bp, url_prefix='/api/devices')
    app.register_blueprint(cameras_bp, url_prefix='/api/cameras')
    app.register_blueprint(alerts_bp, url_prefix='/api/alerts')
    app.register_blueprint(network_bp, url_prefix='/api/network')