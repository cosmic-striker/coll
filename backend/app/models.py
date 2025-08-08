from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='viewer')  # admin, operator, viewer

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    vendor = db.Column(db.String(50))
    device_type = db.Column(db.String(50))  # switch, router, camera, etc
    snmp_community = db.Column(db.String(50), default='public')
    last_seen = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='unknown')  # online, offline, unknown
    meta = db.Column(db.JSON)

class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    rtsp_url = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    location = db.Column(db.String(100))
    status = db.Column(db.String(20), default='unknown')
    last_snapshot = db.Column(db.String(255))

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=True)
    severity = db.Column(db.String(20))
    message = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    acknowledged = db.Column(db.Boolean, default=False)
    acknowledged_at = db.Column(db.DateTime)
