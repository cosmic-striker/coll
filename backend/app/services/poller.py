from celery import shared_task
from app import db
from app.models import Device, Camera, Alert
from datetime import datetime
import subprocess
import socket
import requests
from urllib.parse import urlparse
import logging

import asyncio

# SNMP imports
try:
    from pysnmp.hlapi.v3arch.asyncio import *
    SNMP_AVAILABLE = True
except ImportError:
    try:
        from pysnmp.hlapi.v1arch.asyncio import *
        SNMP_AVAILABLE = True
    except ImportError:
        SNMP_AVAILABLE = False
        logging.warning("PySNMP not available, SNMP features will be limited")

# Use shared_task decorator instead of getting celery instance
# This avoids circular import issues

@shared_task(bind=True)
def poll_all_devices(self):
    """Poll all devices for status updates"""
    try:
        devices = Device.query.all()
        results = []
        
        for device in devices:
            result = poll_device_sync(device.id)
            results.append(result)
            
        return {
            'total_polled': len(results),
            'online': len([r for r in results if r.get('status') == 'online']),
            'offline': len([r for r in results if r.get('status') == 'offline'])
        }
    except Exception as e:
        logging.error(f"Error in poll_all_devices: {str(e)}")
        return {'error': str(e)}

@shared_task(bind=True)
def poll_device_task(self, device_id):
    """Async task to poll a specific device"""
    return poll_device_sync(device_id)

async def poll_device_snmp(ip_address, community, port=161, timeout=5):
    """Poll device using SNMP to get system information"""
    if not SNMP_AVAILABLE:
        return False, {}

    try:
        device_info = {}

        # SNMP OIDs for basic system information
        oids = [
            ('sysDescr', '1.3.6.1.2.1.1.1.0'),      # System description
            ('sysName', '1.3.6.1.2.1.1.5.0'),       # System name
            ('sysUpTime', '1.3.6.1.2.1.1.3.0'),     # System uptime
            ('sysLocation', '1.3.6.1.2.1.1.6.0'),   # System location
            ('sysContact', '1.3.6.1.2.1.1.4.0'),    # System contact
            ('ifNumber', '1.3.6.1.2.1.2.1.0'),      # Number of interfaces
        ]

        # Create transport target
        transport = await UdpTransportTarget.create((ip_address, port), timeout)

        # Query each OID using hlapi
        for name, oid in oids:
            try:
                errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
                    SnmpEngine(),
                    CommunityData(community),
                    transport,
                    ContextData(),
                    ObjectType(ObjectIdentity(oid))
                )

                if errorIndication:
                    logging.warning(f"SNMP error for {ip_address} OID {oid}: {errorIndication}")
                    continue
                elif errorStatus:
                    logging.warning(f"SNMP error for {ip_address} OID {oid}: {errorStatus.prettyPrint()}")
                    continue
                else:
                    for varBind in varBinds:
                        value = varBind[1].prettyPrint()
                        device_info[name] = value

                        # Special handling for interface count
                        if name == 'ifNumber':
                            device_info['interface_count'] = int(value) if value.isdigit() else 0

            except Exception as e:
                logging.warning(f"Failed to query OID {oid} on {ip_address}: {str(e)}")
                continue

        # If we got at least system description, consider SNMP successful
        if 'sysDescr' in device_info:
            return True, device_info
        else:
            return False, {}

    except Exception as e:
        logging.error(f"SNMP polling failed for {ip_address}: {str(e)}")
        return False, {}

def poll_device_sync(device_id):
    """Synchronous device polling function with SNMP support"""
    try:
        device = Device.query.get(device_id)
        if not device:
            return {'error': 'Device not found'}
        
        # Try SNMP polling first, fall back to ping if SNMP fails
        snmp_success = False
        snmp_data = {}
        
        if SNMP_AVAILABLE and device.snmp_community:
            # Run async SNMP polling in event loop
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                snmp_success, snmp_data = loop.run_until_complete(
                    poll_device_snmp(device.ip_address, device.snmp_community)
                )
                loop.close()
            except Exception as e:
                logging.warning(f"SNMP polling failed for device {device_id}: {str(e)}")
                snmp_success = False
                snmp_data = {}
        
        # If SNMP succeeded, device is online
        if snmp_success:
            is_online = True
            device_info = snmp_data
        else:
            # Fall back to ping
            is_online = ping_host(device.ip_address)
            device_info = {}
        
        old_status = device.status
        device.status = 'online' if is_online else 'offline'
        device.last_seen = datetime.utcnow() if is_online else device.last_seen
        
        # Update device metadata with SNMP information
        if snmp_data:
            if not device.meta:
                device.meta = {}
            device.meta.update({
                'snmp_available': True,
                'system_description': snmp_data.get('sysDescr', ''),
                'system_name': snmp_data.get('sysName', ''),
                'system_uptime': snmp_data.get('sysUpTime', ''),
                'interface_count': snmp_data.get('interface_count', 0),
                'last_snmp_poll': datetime.utcnow().isoformat()
            })
        else:
            if device.meta:
                device.meta['snmp_available'] = False
        
        # Create alert if status changed to offline
        if old_status == 'online' and device.status == 'offline':
            alert = Alert(
                device_id=device.id,
                severity='high',
                message=f'Device {device.name} ({device.ip_address}) went offline',
                created_at=datetime.utcnow(),
                acknowledged=False
            )
            db.session.add(alert)
            
            # Send notification for high severity alert
            from app.services.alerting import send_alert_notification
            send_alert_notification.delay(alert.id)
        
        # Create alert if device comes back online
        elif old_status == 'offline' and device.status == 'online':
            alert = Alert(
                device_id=device.id,
                severity='info',
                message=f'Device {device.name} ({device.ip_address}) is back online',
                created_at=datetime.utcnow(),
                acknowledged=False
            )
            db.session.add(alert)
        
        db.session.commit()
        
        return {
            'device_id': device.id,
            'device_name': device.name,
            'ip_address': device.ip_address,
            'status': device.status,
            'snmp_success': snmp_success,
            'snmp_data': snmp_data,
            'last_seen': device.last_seen.isoformat() if device.last_seen else None,
            'status_changed': old_status != device.status
        }
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error polling device {device_id}: {str(e)}")
        return {'error': str(e), 'device_id': device_id}

@shared_task(bind=True)
def poll_all_cameras(self):
    """Poll all cameras for status updates"""
    try:
        cameras = Camera.query.all()
        results = []
        
        for camera in cameras:
            result = test_camera_sync(camera.id)
            results.append(result)
            
        return {
            'total_polled': len(results),
            'online': len([r for r in results if r.get('status') == 'online']),
            'offline': len([r for r in results if r.get('status') == 'offline'])
        }
    except Exception as e:
        logging.error(f"Error in poll_all_cameras: {str(e)}")
        return {'error': str(e)}

@shared_task(bind=True)
def test_camera_connection_task(self, camera_id):
    """Async task to test camera connection"""
    return test_camera_sync(camera_id)

def test_camera_sync(camera_id):
    """Synchronous camera connection test"""
    try:
        camera = Camera.query.get(camera_id)
        if not camera:
            return {'error': 'Camera not found'}
        
        old_status = camera.status
        
        # Test basic connectivity first
        is_reachable = ping_host(camera.ip_address)
        
        if is_reachable:
            # Test RTSP stream using OpenCV
            from app.camera_stream import test_rtsp_connection
            rtsp_success, rtsp_message = test_rtsp_connection(
                camera.rtsp_url, camera.username, camera.password
            )
            is_stream_available = rtsp_success
            camera.status = 'online' if is_stream_available else 'offline'
        else:
            camera.status = 'offline'
        
        # Create alert if camera status changed to offline
        if old_status == 'online' and camera.status == 'offline':
            alert = Alert(
                device_id=None,  # Cameras don't have device_id in our current model
                severity='medium',
                message=f'Camera {camera.name} ({camera.ip_address}) went offline',
                created_at=datetime.utcnow(),
                acknowledged=False
            )
            db.session.add(alert)
        
        # Create alert if camera comes back online
        elif old_status == 'offline' and camera.status == 'online':
            alert = Alert(
                device_id=None,
                severity='info',
                message=f'Camera {camera.name} ({camera.ip_address}) is back online',
                created_at=datetime.utcnow(),
                acknowledged=False
            )
            db.session.add(alert)
        
        db.session.commit()
        
        return {
            'camera_id': camera.id,
            'camera_name': camera.name,
            'ip_address': camera.ip_address,
            'status': camera.status,
            'status_changed': old_status != camera.status
        }
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error testing camera {camera_id}: {str(e)}")
        return {'error': str(e), 'camera_id': camera_id}

def ping_host(ip_address, timeout=5):
    """Ping a host to check connectivity"""
    try:
        # Use platform-specific ping command
        import platform
        system = platform.system().lower()
        
        if system == "windows":
            cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), ip_address]
        else:
            cmd = ["ping", "-c", "1", "-W", str(timeout), ip_address]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 2)
        return result.returncode == 0
        
    except (subprocess.TimeoutExpired, Exception) as e:
        logging.warning(f"Ping failed for {ip_address}: {str(e)}")
        return False

def test_rtsp_stream(rtsp_url, timeout=10):
    """Test RTSP stream availability"""
    try:
        # Parse RTSP URL to get host and port
        parsed = urlparse(rtsp_url)
        host = parsed.hostname
        port = parsed.port or 554  # Default RTSP port
        
        # Test TCP connection to RTSP port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        return result == 0
        
    except Exception as e:
        logging.warning(f"RTSP test failed for {rtsp_url}: {str(e)}")
        return False

# Periodic task setup needs to be configured through Celery beat
# Configuration moved to celery_worker.py or app config