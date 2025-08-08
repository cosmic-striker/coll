from flask import Blueprint, jsonify, request
from app.models import Alert, Device
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.routes.auth import admin_required, operator_required
from datetime import datetime

alerts_bp = Blueprint('alerts', __name__)

@alerts_bp.route('/', methods=['GET'])
@jwt_required()
def list_alerts():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        severity = request.args.get('severity')
        acknowledged = request.args.get('acknowledged')
        
        query = Alert.query
        
        if severity:
            query = query.filter_by(severity=severity)
        
        if acknowledged is not None:
            ack_filter = acknowledged.lower() == 'true'
            query = query.filter_by(acknowledged=ack_filter)
        
        alerts = query.order_by(Alert.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        result = []
        for alert in alerts.items:
            device_name = None
            if alert.device_id:
                device = Device.query.get(alert.device_id)
                device_name = device.name if device else None
            
            result.append({
                'id': alert.id,
                'device_id': alert.device_id,
                'device_name': device_name,
                'severity': alert.severity,
                'message': alert.message,
                'created_at': alert.created_at.isoformat(),
                'acknowledged': alert.acknowledged,
                'acknowledged_at': alert.acknowledged_at.isoformat() if alert.acknowledged_at else None
            })
        
        return jsonify({
            'alerts': result,
            'pagination': {
                'page': alerts.page,
                'pages': alerts.pages,
                'per_page': alerts.per_page,
                'total': alerts.total
            }
        })
    except Exception as e:
        return jsonify({'msg': 'Failed to list alerts', 'error': str(e)}), 500

@alerts_bp.route('/<int:alert_id>', methods=['GET'])
@jwt_required()
def get_alert(alert_id):
    try:
        alert = Alert.query.get_or_404(alert_id)
        
        device_name = None
        if alert.device_id:
            device = Device.query.get(alert.device_id)
            device_name = device.name if device else None
        
        return jsonify({
            'id': alert.id,
            'device_id': alert.device_id,
            'device_name': device_name,
            'severity': alert.severity,
            'message': alert.message,
            'created_at': alert.created_at.isoformat(),
            'acknowledged': alert.acknowledged,
            'acknowledged_at': alert.acknowledged_at.isoformat() if alert.acknowledged_at else None
        })
    except Exception as e:
        return jsonify({'msg': 'Alert not found', 'error': str(e)}), 404

@alerts_bp.route('/', methods=['POST'])
@operator_required
def create_alert():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'msg': 'No input data provided'}), 400
        
        device_id = data.get('device_id')
        severity = data.get('severity', 'info')
        message = data.get('message')
        
        if not message:
            return jsonify({'msg': 'Message is required'}), 400
        
        if severity not in ['critical', 'high', 'medium', 'low', 'info']:
            return jsonify({'msg': 'Invalid severity level'}), 400
        
        # Validate device exists if device_id provided
        if device_id:
            device = Device.query.get(device_id)
            if not device:
                return jsonify({'msg': 'Device not found'}), 404
        
        alert = Alert(
            device_id=device_id,
            severity=severity,
            message=message,
            created_at=datetime.utcnow(),
            acknowledged=False
        )
        
        db.session.add(alert)
        db.session.commit()
        
        # Trigger alert notification if severity is high
        if severity in ['critical', 'high']:
            from app.services.alerting import send_alert_notification
            send_alert_notification.delay(alert.id)
        
        return jsonify({
            'id': alert.id,
            'device_id': alert.device_id,
            'severity': alert.severity,
            'message': alert.message,
            'created_at': alert.created_at.isoformat(),
            'acknowledged': alert.acknowledged
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to create alert', 'error': str(e)}), 500

@alerts_bp.route('/<int:alert_id>/acknowledge', methods=['POST'])
@operator_required
def acknowledge_alert(alert_id):
    try:
        alert = Alert.query.get_or_404(alert_id)
        
        if alert.acknowledged:
            return jsonify({'msg': 'Alert already acknowledged'}), 400
        
        alert.acknowledged = True
        alert.acknowledged_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'id': alert.id,
            'acknowledged': alert.acknowledged,
            'acknowledged_at': alert.acknowledged_at.isoformat(),
            'msg': 'Alert acknowledged successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to acknowledge alert', 'error': str(e)}), 500

@alerts_bp.route('/acknowledge-all', methods=['POST'])
@operator_required
def acknowledge_all_alerts():
    try:
        data = request.get_json() or {}
        severity = data.get('severity')
        
        query = Alert.query.filter_by(acknowledged=False)
        if severity:
            query = query.filter_by(severity=severity)
        
        alerts = query.all()
        count = 0
        
        for alert in alerts:
            alert.acknowledged = True
            alert.acknowledged_at = datetime.utcnow()
            count += 1
        
        db.session.commit()
        
        return jsonify({
            'msg': f'Acknowledged {count} alerts',
            'count': count
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to acknowledge alerts', 'error': str(e)}), 500

@alerts_bp.route('/<int:alert_id>', methods=['DELETE'])
@admin_required
def delete_alert(alert_id):
    try:
        alert = Alert.query.get_or_404(alert_id)
        db.session.delete(alert)
        db.session.commit()
        return jsonify({'msg': 'Alert deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to delete alert', 'error': str(e)}), 500

@alerts_bp.route('/summary', methods=['GET'])
@jwt_required()
def alerts_summary():
    try:
        total_alerts = Alert.query.count()
        unacknowledged_alerts = Alert.query.filter_by(acknowledged=False).count()
        critical_alerts = Alert.query.filter_by(severity='critical', acknowledged=False).count()
        high_alerts = Alert.query.filter_by(severity='high', acknowledged=False).count()
        
        recent_alerts = Alert.query.filter_by(acknowledged=False)\
            .order_by(Alert.created_at.desc()).limit(5).all()
        
        recent_list = []
        for alert in recent_alerts:
            device_name = None
            if alert.device_id:
                device = Device.query.get(alert.device_id)
                device_name = device.name if device else None
            
            recent_list.append({
                'id': alert.id,
                'device_name': device_name,
                'severity': alert.severity,
                'message': alert.message,
                'created_at': alert.created_at.isoformat()
            })
        
        return jsonify({
            'total': total_alerts,
            'unacknowledged': unacknowledged_alerts,
            'critical': critical_alerts,
            'high': high_alerts,
            'recent': recent_list
        })
    except Exception as e:
        return jsonify({'msg': 'Failed to get alerts summary', 'error': str(e)}), 500