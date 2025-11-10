"""
Network scanning route for discovering devices on the network
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import subprocess
import re
import socket
from typing import List, Dict

network_bp = Blueprint('network', __name__)

def get_vendor_from_mac(mac: str) -> str:
    """Identify vendor from MAC address OUI"""
    oui_database = {
        '00:0C:29': 'VMware',
        '00:50:56': 'VMware',
        '00:1C:0E': 'Cisco',
        '00:24:C3': 'Cisco',
        'F4:CF:E2': 'Cisco',
        '00:1B:D5': 'Cisco',
        '00:04:96': 'Cisco',
        '00:0A:42': 'Cisco',
        '00:D0:D3': 'HP/3Com',
        '00:0F:E2': 'HP/3Com',
        '00:1A:4B': 'HP',
        '00:23:7D': 'HP',
        '00:19:BB': 'HP',
        '00:0E:7F': 'D-Link',
        '00:17:9A': 'D-Link',
        '00:05:5D': 'D-Link',
        '28:10:7B': 'TP-Link',
        'C4:E9:84': 'TP-Link',
        '50:C7:BF': 'TP-Link',
        'EC:08:6B': 'TP-Link',
        '00:13:3B': 'Netgear',
        '00:24:B2': 'Netgear',
        'A0:63:91': 'Netgear',
        '00:03:7F': 'Atheros/Ubiquiti',
        '00:15:6D': 'Ubiquiti',
        '68:D7:9A': 'Ubiquiti',
        'F0:9F:C2': 'Ubiquiti',
        '00:12:34': 'Dahua',
        '00:11:32': 'Hikvision',
        '00:40:8C': 'Axis',
    }
    
    oui = mac[:8].upper()
    return oui_database.get(oui, 'Unknown')

def identify_device_type(ip: str, mac: str, vendor: str, ports: List[int]) -> str:
    """Determine device type based on vendor and open ports"""
    vendor_lower = vendor.lower()
    
    # Check for cameras
    if any(cam in vendor_lower for cam in ['dahua', 'hikvision', 'axis', 'camera']):
        return 'camera'
    
    # Check for network equipment
    if any(net in vendor_lower for net in ['cisco', 'hp', 'd-link', 'tp-link', 'netgear', 'ubiquiti']):
        if 161 in ports:  # SNMP
            return 'switch'
        return 'switch'
    
    # Check by ports
    if 554 in ports:  # RTSP
        return 'camera'
    elif 161 in ports:  # SNMP
        return 'switch'
    elif 3389 in ports:  # RDP
        return 'computer'
    elif 22 in ports or 23 in ports:  # SSH/Telnet
        return 'server'
    
    return 'unknown'

def scan_port(ip: str, port: int, timeout: float = 0.3) -> bool:
    """Check if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

def scan_device_ports(ip: str) -> Dict:
    """Scan common ports on a device"""
    common_ports = {
        80: 'HTTP',
        443: 'HTTPS',
        22: 'SSH',
        23: 'Telnet',
        161: 'SNMP',
        554: 'RTSP',
        8080: 'HTTP-Alt',
        3389: 'RDP',
        21: 'FTP',
    }
    
    open_ports = []
    services = []
    
    for port, service in common_ports.items():
        if scan_port(ip, port, timeout=0.3):
            open_ports.append(port)
            services.append(service)
    
    return {
        'ports': open_ports,
        'services': services
    }

def get_arp_table() -> List[Dict]:
    """Get devices from ARP table"""
    devices = []
    
    try:
        # Windows ARP command
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True, timeout=5)
        output = result.stdout
        
        # Parse ARP output
        for line in output.split('\n'):
            # Look for IP and MAC pattern
            match = re.search(r'(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F-]{17})', line)
            if match:
                ip = match.group(1)
                mac = match.group(2).replace('-', ':').upper()
                
                # Skip broadcast, multicast, and loopback
                if ip.startswith('224.') or ip.startswith('239.') or ip.startswith('255.') or ip.startswith('169.254.'):
                    continue
                
                vendor = get_vendor_from_mac(mac)
                
                devices.append({
                    'ip': ip,
                    'mac': mac,
                    'vendor': vendor
                })
    
    except Exception as e:
        print(f"Error getting ARP table: {e}")
    
    return devices

@network_bp.route('/scan', methods=['POST'])
@jwt_required()
def scan_network():
    """
    Scan the local network for devices
    
    Returns:
        JSON with list of discovered devices
    """
    try:
        # Get devices from ARP table
        arp_devices = get_arp_table()
        
        discovered_devices = []
        
        # Scan each device
        for device in arp_devices:
            # Scan ports
            port_info = scan_device_ports(device['ip'])
            
            # Identify device type
            device_type = identify_device_type(
                device['ip'],
                device['mac'],
                device['vendor'],
                port_info['ports']
            )
            
            # Create device info
            discovered_device = {
                'ip': device['ip'],
                'mac': device['mac'],
                'vendor': device['vendor'],
                'type': device_type,
                'name': f"{device['vendor']} {device_type.title()}" if device['vendor'] != 'Unknown' else f"Device {device['ip']}",
                'ports': port_info['ports'],
                'services': port_info['services']
            }
            
            discovered_devices.append(discovered_device)
        
        return jsonify({
            'success': True,
            'devices': discovered_devices,
            'count': len(discovered_devices)
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'devices': []
        }), 500
