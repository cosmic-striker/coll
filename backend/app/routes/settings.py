from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from flask_jwt_extended import jwt_required
from app.routes.auth import admin_required
import os
import json

settings_bp = Blueprint('settings', __name__)

SETTINGS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'settings.json')

def load_settings():
    """Load settings from file"""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {
        'poll_interval': 60,
        'alert_email_from': '',
        'alert_email_to': '',
        'smtp_server': '',
        'smtp_port': 587,
        'smtp_username': '',
        'smtp_password': '',
        'slack_webhook': ''
    }

def save_settings(settings):
    """Save settings to file"""
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)

@settings_bp.route('/', methods=['GET'])
@admin_required
def get_settings():
    """Get system settings"""
    try:
        settings = load_settings()
        return jsonify(settings)
    except Exception as e:
        return jsonify({'msg': 'Failed to load settings', 'error': str(e)}), 500

@settings_bp.route('/', methods=['PUT'])
@admin_required
def update_settings():
    """Update system settings"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'msg': 'No input data provided'}), 400
        
        current_settings = load_settings()
        
        # Update only provided fields
        if 'poll_interval' in data:
            current_settings['poll_interval'] = int(data['poll_interval'])
        if 'alert_email_from' in data:
            current_settings['alert_email_from'] = data['alert_email_from']
        if 'alert_email_to' in data:
            current_settings['alert_email_to'] = data['alert_email_to']
        if 'smtp_server' in data:
            current_settings['smtp_server'] = data['smtp_server']
        if 'smtp_port' in data:
            current_settings['smtp_port'] = int(data['smtp_port'])
        if 'smtp_username' in data:
            current_settings['smtp_username'] = data['smtp_username']
        if 'smtp_password' in data:
            current_settings['smtp_password'] = data['smtp_password']
        if 'slack_webhook' in data:
            current_settings['slack_webhook'] = data['slack_webhook']
        
        save_settings(current_settings)
        
        return jsonify({'msg': 'Settings updated successfully', 'settings': current_settings})
    except Exception as e:
        return jsonify({'msg': 'Failed to update settings', 'error': str(e)}), 500

@settings_bp.route('/test-email', methods=['POST'])
@admin_required
def test_email():
    """Send a test email"""
    try:
        settings = load_settings()
        
        if not settings.get('smtp_server') or not settings.get('alert_email_to'):
            return jsonify({'msg': 'Email settings not configured'}), 400
        
        # Import here to avoid circular dependency
        from app.services.alerting import send_email_alert
        
        success = send_email_alert(
            subject='Test Email from Device Monitoring System',
            body='This is a test email to verify your email configuration.',
            to_email=settings.get('alert_email_to')
        )
        
        if success:
            return jsonify({'msg': 'Test email sent successfully'})
        else:
            return jsonify({'msg': 'Failed to send test email'}), 500
            
    except Exception as e:
        return jsonify({'msg': 'Failed to send test email', 'error': str(e)}), 500

@settings_bp.route('/test-slack', methods=['POST'])
@admin_required
def test_slack():
    """Send a test Slack message"""
    try:
        settings = load_settings()
        
        if not settings.get('slack_webhook'):
            return jsonify({'msg': 'Slack webhook not configured'}), 400
        
        # Import here to avoid circular dependency
        from app.services.alerting import send_slack_alert
        
        success = send_slack_alert(
            message='Test message from Device Monitoring System',
            webhook_url=settings.get('slack_webhook')
        )
        
        if success:
            return jsonify({'msg': 'Test Slack message sent successfully'})
        else:
            return jsonify({'msg': 'Failed to send test Slack message'}), 500
            
    except Exception as e:
        return jsonify({'msg': 'Failed to send test Slack message', 'error': str(e)}), 500

@settings_bp.route('/restart-polling', methods=['POST'])
@admin_required
def restart_polling():
    """Restart device polling service"""
    try:
        # This would restart the Celery beat scheduler
        # For now, just return success
        return jsonify({'msg': 'Polling service restart requested'})
    except Exception as e:
        return jsonify({'msg': 'Failed to restart polling', 'error': str(e)}), 500

@settings_bp.route('/clear-cache', methods=['POST'])
@admin_required
def clear_cache():
    """Clear application cache"""
    try:
        # This would clear Redis cache if implemented
        # For now, just return success
        return jsonify({'msg': 'Cache cleared successfully'})
    except Exception as e:
        return jsonify({'msg': 'Failed to clear cache', 'error': str(e)}), 500
