from flask import Blueprint, jsonify, request, Response
from app.models import Camera, Alert
from app import db
from flask_jwt_extended import jwt_required
from app.routes.auth import admin_required, operator_required
from datetime import datetime

cameras_bp = Blueprint('cameras', __name__)

@cameras_bp.route('/', methods=['GET'])
@jwt_required()
def list_cameras():
    try:
        cameras = Camera.query.all()
        result = []
        for c in cameras:
            result.append({
                'id': c.id,
                'name': c.name,
                'ip_address': c.ip_address,
                'rtsp_url': c.rtsp_url,
                'username': c.username,
                'location': c.location,
                'status': c.status,
                'last_snapshot': c.last_snapshot
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({'msg': 'Failed to list cameras', 'error': str(e)}), 500

@cameras_bp.route('/<int:camera_id>', methods=['GET'])
@jwt_required()
def get_camera(camera_id):
    try:
        camera = Camera.query.get_or_404(camera_id)
        return jsonify({
            'id': camera.id,
            'name': camera.name,
            'ip_address': camera.ip_address,
            'rtsp_url': camera.rtsp_url,
            'username': camera.username,
            'location': camera.location,
            'status': camera.status,
            'last_snapshot': camera.last_snapshot
        })
    except Exception as e:
        return jsonify({'msg': 'Camera not found', 'error': str(e)}), 404

@cameras_bp.route('/', methods=['POST'])
@operator_required
def create_camera():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'msg': 'No input data provided'}), 400
        
        name = data.get('name')
        ip_address = data.get('ip_address')
        rtsp_url = data.get('rtsp_url')
        username = data.get('username', '')
        password = data.get('password', '')
        location = data.get('location', '')
        
        if not all([name, ip_address, rtsp_url]):
            return jsonify({'msg': 'Name, IP address and RTSP URL required'}), 400
        
        # Check if camera with same IP exists
        if Camera.query.filter_by(ip_address=ip_address).first():
            return jsonify({'msg': 'Camera with this IP already exists'}), 409
        
        camera = Camera(
            name=name,
            ip_address=ip_address,
            rtsp_url=rtsp_url,
            username=username,
            password=password,
            location=location,
            status='unknown'
        )
        
        db.session.add(camera)
        db.session.commit()
        
        return jsonify({
            'id': camera.id,
            'name': camera.name,
            'ip_address': camera.ip_address,
            'rtsp_url': camera.rtsp_url,
            'username': camera.username,
            'location': camera.location,
            'status': camera.status
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to create camera', 'error': str(e)}), 500

@cameras_bp.route('/<int:camera_id>', methods=['PUT'])
@operator_required
def update_camera(camera_id):
    try:
        camera = Camera.query.get_or_404(camera_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'msg': 'No input data provided'}), 400
        
        camera.name = data.get('name', camera.name)
        camera.rtsp_url = data.get('rtsp_url', camera.rtsp_url)
        camera.username = data.get('username', camera.username)
        camera.location = data.get('location', camera.location)
        
        # Handle password update
        if data.get('password'):
            camera.password = data.get('password')
        
        # Check IP address change
        new_ip = data.get('ip_address')
        if new_ip and new_ip != camera.ip_address:
            if Camera.query.filter_by(ip_address=new_ip).first():
                return jsonify({'msg': 'Camera with this IP already exists'}), 409
            camera.ip_address = new_ip
        
        db.session.commit()
        
        return jsonify({
            'id': camera.id,
            'name': camera.name,
            'ip_address': camera.ip_address,
            'rtsp_url': camera.rtsp_url,
            'username': camera.username,
            'location': camera.location,
            'status': camera.status,
            'last_snapshot': camera.last_snapshot
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to update camera', 'error': str(e)}), 500

@cameras_bp.route('/<int:camera_id>', methods=['DELETE'])
@admin_required
def delete_camera(camera_id):
    try:
        camera = Camera.query.get_or_404(camera_id)
        db.session.delete(camera)
        db.session.commit()
        return jsonify({'msg': 'Camera deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to delete camera', 'error': str(e)}), 500

@cameras_bp.route('/<int:camera_id>/stream/start', methods=['POST'])
@operator_required
def start_camera_stream(camera_id):
    """Start RTSP streaming for a camera"""
    try:
        camera = Camera.query.get_or_404(camera_id)
        
        from app.camera_stream import start_camera_stream
        
        success = start_camera_stream(
            camera_id=camera.id,
            rtsp_url=camera.rtsp_url,
            username=camera.username,
            password=camera.password
        )
        
        if success:
            return jsonify({'msg': 'Camera stream started successfully'})
        else:
            return jsonify({'msg': 'Failed to start camera stream'}), 500
            
    except Exception as e:
        return jsonify({'msg': 'Failed to start camera stream', 'error': str(e)}), 500

@cameras_bp.route('/<int:camera_id>/stream/stop', methods=['POST'])
@operator_required
def stop_camera_stream(camera_id):
    """Stop RTSP streaming for a camera"""
    try:
        from app.camera_stream import stop_camera_stream
        stop_camera_stream(camera_id)
        return jsonify({'msg': 'Camera stream stopped successfully'})
            
    except Exception as e:
        return jsonify({'msg': 'Failed to stop camera stream', 'error': str(e)}), 500

@cameras_bp.route('/<int:camera_id>/stream/live')
@jwt_required()
def get_camera_live_stream(camera_id):
    """Get live MJPEG stream for a camera"""
    try:
        from app.camera_stream import generate_mjpeg_stream, get_camera_stream_info
        
        # Check if stream is active
        stream_info = get_camera_stream_info(camera_id)
        if not stream_info or stream_info.get('status') != 'streaming':
            return jsonify({'msg': 'Camera stream is not active'}), 404
        
        # Return MJPEG stream
        from app.camera_stream import generate_mjpeg_stream
        return Response(
            generate_mjpeg_stream(camera_id),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )
            
    except Exception as e:
        return jsonify({'msg': 'Failed to get camera stream', 'error': str(e)}), 500

@cameras_bp.route('/<int:camera_id>/snapshot')
@jwt_required()
def get_camera_snapshot(camera_id):
    """Get a snapshot from the camera"""
    try:
        from app.camera_stream import get_snapshot_base64
        
        snapshot_b64 = get_snapshot_base64(camera_id)
        if snapshot_b64:
            return jsonify({
                'snapshot': f'data:image/jpeg;base64,{snapshot_b64}',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'msg': 'No snapshot available'}), 404
            
    except Exception as e:
        return jsonify({'msg': 'Failed to get camera snapshot', 'error': str(e)}), 500

@cameras_bp.route('/<int:camera_id>/stream/status')
@jwt_required()
def get_camera_stream_status(camera_id):
    """Get streaming status for a camera"""
    try:
        from app.camera_stream import get_camera_stream_info
        
        stream_info = get_camera_stream_info(camera_id)
        if stream_info:
            return jsonify(stream_info)
        else:
            return jsonify({'status': 'not_streaming'})
            
    except Exception as e:
        return jsonify({'msg': 'Failed to get stream status', 'error': str(e)}), 500

@cameras_bp.route('/<int:camera_id>/test', methods=['POST'])
@operator_required
def test_camera_connection(camera_id):
    try:
        camera = Camera.query.get_or_404(camera_id)

        # Import here to avoid circular imports
        from app.services.poller import test_camera_connection_task, test_camera_sync

        # Try to queue async test task; if Celery/broker isn't available, fall back to sync test
        try:
            task = test_camera_connection_task.delay(camera_id)
            return jsonify({
                'msg': 'Camera connection test initiated',
                'task_id': task.id,
                'camera_id': camera_id
            })
        except Exception:
            # Celery/broker unavailable — run the test in a background thread
            # so the HTTP request returns immediately instead of blocking.
            import threading
            from flask import current_app

            def _bg_test(cam_id):
                try:
                    app = current_app._get_current_object()
                    with app.app_context():
                        res = test_camera_sync(cam_id)
                        # Optionally log or store the result somewhere
                        try:
                            import logging
                            logging.getLogger('app').info(f"Background camera test result for {cam_id}: {res}")
                        except Exception:
                            pass
                except Exception as _e:
                    try:
                        import logging
                        logging.getLogger('app').exception(f"Background camera test failed for {cam_id}: {_e}")
                    except Exception:
                        pass

            t = threading.Thread(target=_bg_test, args=(camera_id,), daemon=True)
            t.start()
            return jsonify({
                'msg': 'Camera connection test initiated (background)',
                'camera_id': camera_id
            }), 202
    except Exception as e:
        return jsonify({'msg': 'Failed to test camera connection', 'error': str(e)}), 500

@cameras_bp.route('/status', methods=['GET'])
@jwt_required()
def cameras_status_summary():
    try:
        online_count = Camera.query.filter_by(status='online').count()
        offline_count = Camera.query.filter_by(status='offline').count()
        unknown_count = Camera.query.filter_by(status='unknown').count()
        total_count = Camera.query.count()
        
        return jsonify({
            'total': total_count,
            'online': online_count,
            'offline': offline_count,
            'unknown': unknown_count
        })
    except Exception as e:
        return jsonify({'msg': 'Failed to get camera status summary', 'error': str(e)}), 500