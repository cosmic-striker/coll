from celery import Celery
from app import db, create_app
from app.models import Alert, Device
import smtplib
import requests
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Create Flask app context for Celery tasks
app = create_app()
celery = Celery('alerting')
celery.conf.update(app.config)

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

@celery.task
def send_alert_notification(alert_id):
    """Send alert notification via configured channels"""
    try:
        alert = Alert.query.get(alert_id)
        if not alert:
            return {'error': 'Alert not found'}
        
        device_name = "System"
        device_ip = ""
        
        if alert.device_id:
            device = Device.query.get(alert.device_id)
            if device:
                device_name = device.name
                device_ip = device.ip_address
        
        # Prepare alert data
        alert_data = {
            'id': alert.id,
            'severity': alert.severity,
            'message': alert.message,
            'device_name': device_name,
            'device_ip': device_ip,
            'created_at': alert.created_at.isoformat(),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        results = {}
        
        # Send email notification
        email_result = send_email_alert(alert_data)
        results['email'] = email_result
        
        # Send Slack notification if configured
        slack_result = send_slack_alert(alert_data)
        results['slack'] = slack_result
        
        return results
        
    except Exception as e:
        logging.error(f"Error sending alert notification {alert_id}: {str(e)}")
        return {'error': str(e)}

def send_email_alert(alert_data):
    """Send email alert notification"""
    try:
        # Email configuration from environment
        smtp_server = app.config.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = app.config.get('SMTP_PORT', 587)
        smtp_username = app.config.get('SMTP_USERNAME')
        smtp_password = app.config.get('SMTP_PASSWORD')
        email_from = app.config.get('ALERT_EMAIL_FROM', 'alerts@example.com')
        email_to = app.config.get('ALERT_EMAIL_TO', 'admin@example.com')
        
        if not all([smtp_username, smtp_password]):
            return {'status': 'skipped', 'reason': 'SMTP credentials not configured'}
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = f"[{alert_data['severity'].upper()}] Device Alert: {alert_data['device_name']}"
        
        # Email body
        body = f"""
Device Monitoring Alert

Device: {alert_data['device_name']}
IP Address: {alert_data['device_ip']}
Severity: {alert_data['severity'].upper()}
Message: {alert_data['message']}
Time: {alert_data['created_at']}

Alert ID: {alert_data['id']}

Please check the monitoring dashboard for more details.
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        
        return {'status': 'sent', 'recipient': email_to}
        
    except Exception as e:
        logging.error(f"Failed to send email alert: {str(e)}")
        return {'status': 'failed', 'error': str(e)}

def send_slack_alert(alert_data):
    """Send Slack alert notification"""
    try:
        slack_webhook_url = app.config.get('SLACK_WEBHOOK_URL')
        
        if not slack_webhook_url:
            return {'status': 'skipped', 'reason': 'Slack webhook URL not configured'}
        
        # Determine color based on severity
        color_map = {
            'critical': '#FF0000',  # Red
            'high': '#FFA500',      # Orange
            'medium': '#FFFF00',    # Yellow
            'low': '#00FF00',       # Green
            'info': '#0000FF'       # Blue
        }
        
        color = color_map.get(alert_data['severity'], '#808080')
        
        # Create Slack message
        slack_message = {
            'username': 'Device Monitor',
            'icon_emoji': ':warning:',
            'attachments': [
                {
                    'color': color,
                    'title': f"{alert_data['severity'].upper()} Alert: {alert_data['device_name']}",
                    'text': alert_data['message'],
                    'fields': [
                        {
                            'title': 'Device',
                            'value': alert_data['device_name'],
                            'short': True
                        },
                        {
                            'title': 'IP Address',
                            'value': alert_data['device_ip'] or 'N/A',
                            'short': True
                        },
                        {
                            'title': 'Severity',
                            'value': alert_data['severity'].upper(),
                            'short': True
                        },
                        {
                            'title': 'Time',
                            'value': alert_data['created_at'],
                            'short': True
                        }
                    ],
                    'footer': 'Device Monitoring System',
                    'ts': int(datetime.utcnow().timestamp())
                }
            ]
        }
        
        # Send to Slack
        response = requests.post(
            slack_webhook_url,
            json=slack_message,
            timeout=10
        )
        
        if response.status_code == 200:
            return {'status': 'sent', 'webhook_url': slack_webhook_url}
        else:
            return {
                'status': 'failed',
                'error': f'HTTP {response.status_code}: {response.text}'
            }
            
    except Exception as e:
        logging.error(f"Failed to send Slack alert: {str(e)}")
        return {'status': 'failed', 'error': str(e)}

@celery.task
def send_daily_summary():
    """Send daily summary of alerts and device status"""
    try:
        from datetime import datetime, timedelta
        from sqlalchemy import func
        
        # Get yesterday's date
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        # Get alert counts for yesterday
        alert_counts = db.session.query(
            Alert.severity,
            func.count(Alert.id)
        ).filter(
            Alert.created_at >= yesterday.replace(hour=0, minute=0, second=0),
            Alert.created_at < datetime.utcnow().replace(hour=0, minute=0, second=0)
        ).group_by(Alert.severity).all()
        
        # Get device status counts
        from app.models import Device, Camera
        device_status = db.session.query(
            Device.status,
            func.count(Device.id)
        ).group_by(Device.status).all()
        
        camera_status = db.session.query(
            Camera.status,
            func.count(Camera.id)
        ).group_by(Camera.status).all()
        
        # Prepare summary data
        summary_data = {
            'date': yesterday.strftime('%Y-%m-%d'),
            'alerts': dict(alert_counts),
            'devices': dict(device_status),
            'cameras': dict(camera_status)
        }
        
        # Send summary notifications
        results = {}
        results['email'] = send_email_summary(summary_data)
        results['slack'] = send_slack_summary(summary_data)
        
        return results
        
    except Exception as e:
        logging.error(f"Error sending daily summary: {str(e)}")
        return {'error': str(e)}

def send_email_summary(summary_data):
    """Send daily summary via email"""
    try:
        smtp_server = app.config.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = app.config.get('SMTP_PORT', 587)
        smtp_username = app.config.get('SMTP_USERNAME')
        smtp_password = app.config.get('SMTP_PASSWORD')
        email_from = app.config.get('ALERT_EMAIL_FROM', 'alerts@example.com')
        email_to = app.config.get('ALERT_EMAIL_TO', 'admin@example.com')
        
        if not all([smtp_username, smtp_password]):
            return {'status': 'skipped', 'reason': 'SMTP credentials not configured'}
        
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = f"Daily Monitoring Summary - {summary_data['date']}"
        
        # Create summary body
        body = f"""
Daily Device Monitoring Summary
Date: {summary_data['date']}

ALERTS SUMMARY:
"""
        for severity, count in summary_data['alerts'].items():
            body += f"  {severity.upper()}: {count}\n"
        
        body += "\nDEVICE STATUS:\n"
        for status, count in summary_data['devices'].items():
            body += f"  {status.upper()}: {count}\n"
        
        body += "\nCAMERA STATUS:\n"
        for status, count in summary_data['cameras'].items():
            body += f"  {status.upper()}: {count}\n"
        
        body += "\nThis is an automated summary from the Device Monitoring System."
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        
        return {'status': 'sent', 'recipient': email_to}
        
    except Exception as e:
        logging.error(f"Failed to send email summary: {str(e)}")
        return {'status': 'failed', 'error': str(e)}

def send_slack_summary(summary_data):
    """Send daily summary to Slack"""
    try:
        slack_webhook_url = app.config.get('SLACK_WEBHOOK_URL')
        
        if not slack_webhook_url:
            return {'status': 'skipped', 'reason': 'Slack webhook URL not configured'}
        
        # Create summary fields
        fields = []
        
        if summary_data['alerts']:
            alert_text = "\n".join([f"{k.title()}: {v}" for k, v in summary_data['alerts'].items()])
            fields.append({
                'title': 'Alerts',
                'value': alert_text,
                'short': True
            })
        
        if summary_data['devices']:
            device_text = "\n".join([f"{k.title()}: {v}" for k, v in summary_data['devices'].items()])
            fields.append({
                'title': 'Devices',
                'value': device_text,
                'short': True
            })
        
        if summary_data['cameras']:
            camera_text = "\n".join([f"{k.title()}: {v}" for k, v in summary_data['cameras'].items()])
            fields.append({
                'title': 'Cameras',
                'value': camera_text,
                'short': True
            })
        
        slack_message = {
            'username': 'Device Monitor',
            'icon_emoji': ':chart_with_upwards_trend:',
            'attachments': [
                {
                    'color': '#36a64f',
                    'title': f'Daily Summary - {summary_data["date"]}',
                    'text': 'Device monitoring daily summary report',
                    'fields': fields,
                    'footer': 'Device Monitoring System',
                    'ts': int(datetime.utcnow().timestamp())
                }
            ]
        }
        
        response = requests.post(slack_webhook_url, json=slack_message, timeout=10)
        
        if response.status_code == 200:
            return {'status': 'sent', 'webhook_url': slack_webhook_url}
        else:
            return {
                'status': 'failed',
                'error': f'HTTP {response.status_code}: {response.text}'
            }
            
    except Exception as e:
        logging.error(f"Failed to send Slack summary: {str(e)}")
        return {'status': 'failed', 'error': str(e)}