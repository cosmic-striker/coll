from flask import Blueprint, jsonify, request
from app.models import Device, Alert
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.routes.auth import admin_required, operator_required
from datetime import datetime

devices_bp = Blueprint('devices', __name__)

@devices_bp.route('/', methods=['GET'])
@jwt_required()
def list_devices():
    try:
        devices = Device.query.all()
        result = []
        for d in devices:
            result.append({
                'id': d.id,
                'name': d.name,
                'ip_address': d.ip_address,
                'vendor': d.vendor,
                'device_type': d.device_type,
                'snmp_community': d.snmp_community,
                'last_seen': d.last_seen.isoformat() if d.last_seen else None,
                'status': d.status,
                'meta': d.meta
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({'msg': 'Failed to list devices', 'error': str(e)}), 500

@devices_bp.route('/<int:device_id>', methods=['GET'])
@jwt_required()
def get_device(device_id):
    try:
        device = Device.query.get_or_404(device_id)
        return jsonify({
            'id': device.id,
            'name': device.name,
            'ip_address': device.ip_address,
            'vendor': device.vendor,
            'device_type': device.device_type,
            'snmp_community': device.snmp_community,
            'last_seen': device.last_seen.isoformat() if device.last_seen else None,
            'status': device.status,
            'meta': device.meta
        })
    except Exception as e:
        return jsonify({'msg': 'Device not found', 'error': str(e)}), 404

@devices_bp.route('/', methods=['POST'])
@operator_required
def create_device():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'msg': 'No input data provided'}), 400
        
        name = data.get('name')
        ip_address = data.get('ip_address')
        vendor = data.get('vendor', '')
        device_type = data.get('device_type', '')
        snmp_community = data.get('snmp_community', 'public')
        meta = data.get('meta', {})
        
        if not name or not ip_address:
            return jsonify({'msg': 'Name and IP address required'}), 400
        
        # Check if device with same IP exists
        if Device.query.filter_by(ip_address=ip_address).first():
            return jsonify({'msg': 'Device with this IP already exists'}), 409
        
        device = Device(
            name=name,
            ip_address=ip_address,
            vendor=vendor,
            device_type=device_type,
            snmp_community=snmp_community,
            meta=meta,
            status='unknown'
        )
        
        db.session.add(device)
        db.session.commit()
        
        return jsonify({
            'id': device.id,
            'name': device.name,
            'ip_address': device.ip_address,
            'vendor': device.vendor,
            'device_type': device.device_type,
            'snmp_community': device.snmp_community,
            'status': device.status,
            'meta': device.meta
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to create device', 'error': str(e)}), 500

@devices_bp.route('/<int:device_id>', methods=['PUT'])
@operator_required
def update_device(device_id):
    try:
        device = Device.query.get_or_404(device_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'msg': 'No input data provided'}), 400
        
        device.name = data.get('name', device.name)
        device.vendor = data.get('vendor', device.vendor)
        device.device_type = data.get('device_type', device.device_type)
        device.snmp_community = data.get('snmp_community', device.snmp_community)
        device.meta = data.get('meta', device.meta)
        
        # Check IP address change
        new_ip = data.get('ip_address')
        if new_ip and new_ip != device.ip_address:
            if Device.query.filter_by(ip_address=new_ip).first():
                return jsonify({'msg': 'Device with this IP already exists'}), 409
            device.ip_address = new_ip
        
        db.session.commit()
        
        return jsonify({
            'id': device.id,
            'name': device.name,
            'ip_address': device.ip_address,
            'vendor': device.vendor,
            'device_type': device.device_type,
            'snmp_community': device.snmp_community,
            'last_seen': device.last_seen.isoformat() if device.last_seen else None,
            'status': device.status,
            'meta': device.meta
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to update device', 'error': str(e)}), 500

@devices_bp.route('/<int:device_id>', methods=['DELETE'])
@admin_required
def delete_device(device_id):
    try:
        device = Device.query.get_or_404(device_id)
        db.session.delete(device)
        db.session.commit()
        return jsonify({'msg': 'Device deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to delete device', 'error': str(e)}), 500

@devices_bp.route('/<int:device_id>/poll', methods=['POST'])
@operator_required
def poll_device(device_id):
    try:
        device = Device.query.get_or_404(device_id)
        
        # Import here to avoid circular imports
        from app.services.poller import poll_device_task, poll_device_sync
        
        # Try to queue async polling task; if Celery/broker isn't available, fall back to background thread
        try:
            task = poll_device_task.delay(device_id)
            return jsonify({
                'msg': 'Polling initiated',
                'task_id': task.id,
                'device_id': device_id
            })
        except Exception:
            # Celery/broker unavailable — run the poll in a background thread
            # so the HTTP request returns immediately instead of blocking.
            import threading
            from flask import current_app
            
            def _bg_poll(dev_id):
                try:
                    app = current_app._get_current_object()
                    with app.app_context():
                        res = poll_device_sync(dev_id)
                        # Optionally log the result
                        try:
                            import logging
                            logging.getLogger('app').info(f"Background device poll result for {dev_id}: {res}")
                        except Exception:
                            pass
                except Exception as _e:
                    try:
                        import logging
                        logging.getLogger('app').exception(f"Background device poll failed for {dev_id}: {_e}")
                    except Exception:
                        pass
            
            t = threading.Thread(target=_bg_poll, args=(device_id,), daemon=True)
            t.start()
            return jsonify({
                'msg': 'Polling initiated (background)',
                'device_id': device_id
            }), 202
    except Exception as e:
        return jsonify({'msg': 'Failed to initiate polling', 'error': str(e)}), 500

@devices_bp.route('/status', methods=['GET'])
@jwt_required()
def devices_status_summary():
    try:
        online_count = Device.query.filter_by(status='online').count()
        offline_count = Device.query.filter_by(status='offline').count()
        unknown_count = Device.query.filter_by(status='unknown').count()
        total_count = Device.query.count()
        
        return jsonify({
            'total': total_count,
            'online': online_count,
            'offline': offline_count,
            'unknown': unknown_count
        })
    except Exception as e:
        return jsonify({'msg': 'Failed to get status summary', 'error': str(e)}), 500
