"""
Network Discovery Tool - Find Switches and Network Devices
Discovers switches, routers, and network devices on the local network
"""

import socket
import subprocess
import re
import json
import platform
from typing import List, Dict, Any
import ipaddress
import netifaces
import concurrent.futures

class NetworkDiscovery:
    def __init__(self):
        self.os_type = platform.system()
        self.devices = []
        
    def get_local_ip_and_network(self) -> tuple:
        """Get the local IP address and network range"""
        try:
            # Get all network interfaces
            interfaces = netifaces.interfaces()
            
            for interface in interfaces:
                addrs = netifaces.ifaddresses(interface)
                
                # Check for IPv4 addresses
                if netifaces.AF_INET in addrs:
                    for addr_info in addrs[netifaces.AF_INET]:
                        ip = addr_info.get('addr')
                        netmask = addr_info.get('netmask')
                        
                        # Skip loopback
                        if ip and ip != '127.0.0.1' and not ip.startswith('169.254'):
                            print(f"✓ Found interface: {interface}")
                            print(f"  IP Address: {ip}")
                            print(f"  Netmask: {netmask}")
                            
                            # Calculate network
                            network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                            return ip, str(network)
            
            return None, None
            
        except Exception as e:
            print(f"Error getting local IP: {e}")
            return None, None
    
    def get_arp_table(self) -> List[Dict[str, str]]:
        """Get ARP table to find devices on local network"""
        devices = []
        
        try:
            if self.os_type == "Windows":
                result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
                output = result.stdout
                
                # Parse Windows ARP output
                for line in output.split('\n'):
                    # Look for IP and MAC address pattern
                    match = re.search(r'(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F-]{17})', line)
                    if match:
                        ip = match.group(1)
                        mac = match.group(2).replace('-', ':').upper()
                        
                        devices.append({
                            'ip': ip,
                            'mac': mac,
                            'vendor': self.get_vendor_from_mac(mac)
                        })
            
            else:  # Linux/Unix
                result = subprocess.run(['arp', '-n'], capture_output=True, text=True)
                output = result.stdout
                
                for line in output.split('\n')[1:]:  # Skip header
                    parts = line.split()
                    if len(parts) >= 3:
                        ip = parts[0]
                        mac = parts[2].upper()
                        if re.match(r'^([0-9A-F]{2}:){5}[0-9A-F]{2}$', mac):
                            devices.append({
                                'ip': ip,
                                'mac': mac,
                                'vendor': self.get_vendor_from_mac(mac)
                            })
        
        except Exception as e:
            print(f"Error getting ARP table: {e}")
        
        return devices
    
    def get_vendor_from_mac(self, mac: str) -> str:
        """Identify vendor/manufacturer from MAC address OUI"""
        # Common network equipment OUIs
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
            '00:50:C2': 'IEEE 802.1',
            '01:80:C2': 'IEEE 802.1 (STP/LLDP)',
        }
        
        # Get first 8 characters (OUI)
        oui = mac[:8].upper()
        
        return oui_database.get(oui, 'Unknown')
    
    def ping_host(self, ip: str) -> bool:
        """Ping a host to check if it's alive"""
        try:
            if self.os_type == "Windows":
                result = subprocess.run(
                    ['ping', '-n', '1', '-w', '500', ip],
                    capture_output=True,
                    timeout=2
                )
            else:
                result = subprocess.run(
                    ['ping', '-c', '1', '-W', '1', ip],
                    capture_output=True,
                    timeout=2
                )
            
            return result.returncode == 0
            
        except Exception:
            return False
    
    def scan_port(self, ip: str, port: int, timeout: float = 0.5) -> bool:
        """Check if a port is open on a host"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def identify_device_type(self, ip: str, mac: str, vendor: str) -> Dict[str, Any]:
        """Identify device type based on open ports and vendor"""
        device_info = {
            'ip': ip,
            'mac': mac,
            'vendor': vendor,
            'type': 'Unknown',
            'ports': [],
            'services': []
        }
        
        # Common ports to check
        ports_to_check = {
            80: 'HTTP',
            443: 'HTTPS',
            22: 'SSH',
            23: 'Telnet',
            161: 'SNMP',
            554: 'RTSP',
            8080: 'HTTP-Alt',
        }
        
        print(f"  Scanning {ip} ({vendor})...")
        
        # Check ports
        for port, service in ports_to_check.items():
            if self.scan_port(ip, port, timeout=0.5):
                device_info['ports'].append(port)
                device_info['services'].append(service)
        
        # Determine device type
        if vendor in ['Cisco', 'HP', 'D-Link', 'TP-Link', 'Netgear', 'Ubiquiti']:
            if 161 in device_info['ports']:  # SNMP
                device_info['type'] = 'Network Switch/Router'
            elif 80 in device_info['ports'] or 443 in device_info['ports']:
                device_info['type'] = 'Managed Switch/Router'
            else:
                device_info['type'] = 'Network Device'
        
        elif 554 in device_info['ports']:
            device_info['type'] = 'IP Camera'
        
        elif 80 in device_info['ports'] or 443 in device_info['ports']:
            device_info['type'] = 'Web Server/Device'
        
        return device_info
    
    def get_gateway(self) -> str:
        """Get default gateway"""
        try:
            gws = netifaces.gateways()
            default_gw = gws.get('default', {}).get(netifaces.AF_INET)
            if default_gw:
                return default_gw[0]
        except Exception as e:
            print(f"Error getting gateway: {e}")
        return None
    
    def discover_network(self) -> List[Dict[str, Any]]:
        """Discover all devices on the network"""
        print("\n" + "="*60)
        print("🔍 NETWORK DISCOVERY TOOL")
        print("="*60)
        
        # Get local network info
        local_ip, network = self.get_local_ip_and_network()
        
        if not local_ip:
            print("❌ Could not determine local IP address")
            return []
        
        print(f"\n📍 Your IP: {local_ip}")
        print(f"🌐 Network: {network}")
        
        # Get gateway
        gateway = self.get_gateway()
        if gateway:
            print(f"🚪 Gateway: {gateway}")
        
        # Get devices from ARP table
        print(f"\n🔍 Scanning ARP table...")
        arp_devices = self.get_arp_table()
        print(f"✓ Found {len(arp_devices)} devices in ARP table")
        
        # Identify each device
        print(f"\n🔬 Identifying devices...")
        discovered_devices = []
        
        for device in arp_devices:
            device_info = self.identify_device_type(
                device['ip'],
                device['mac'],
                device['vendor']
            )
            discovered_devices.append(device_info)
        
        return discovered_devices
    
    def find_switches(self, devices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter for network switches"""
        switches = []
        
        for device in devices:
            if 'Switch' in device['type'] or 'Router' in device['type']:
                switches.append(device)
            elif device['vendor'] in ['Cisco', 'HP', 'D-Link', 'TP-Link', 'Netgear', 'Ubiquiti']:
                if device['vendor'] != 'Unknown':
                    switches.append(device)
        
        return switches
    
    def print_results(self, devices: List[Dict[str, Any]]):
        """Print discovery results"""
        print("\n" + "="*60)
        print("📊 DISCOVERY RESULTS")
        print("="*60)
        
        # Find switches
        switches = self.find_switches(devices)
        
        if switches:
            print(f"\n🔌 FOUND {len(switches)} NETWORK SWITCH(ES):")
            print("-"*60)
            
            for idx, switch in enumerate(switches, 1):
                print(f"\n#{idx} Network Switch/Router:")
                print(f"   IP Address: {switch['ip']}")
                print(f"   MAC Address: {switch['mac']}")
                print(f"   Vendor: {switch['vendor']}")
                print(f"   Type: {switch['type']}")
                if switch['ports']:
                    print(f"   Open Ports: {', '.join(map(str, switch['ports']))}")
                if switch['services']:
                    print(f"   Services: {', '.join(switch['services'])}")
        else:
            print("\n⚠️  No network switches detected")
            print("   This could mean:")
            print("   - You're connected to an unmanaged switch")
            print("   - Switch doesn't respond to scans")
            print("   - Switch is not in ARP table yet")
        
        # Show all devices
        print(f"\n\n📱 ALL DISCOVERED DEVICES ({len(devices)}):")
        print("-"*60)
        
        for idx, device in enumerate(devices, 1):
            print(f"\n#{idx} {device['type']}")
            print(f"   IP: {device['ip']}")
            print(f"   MAC: {device['mac']}")
            print(f"   Vendor: {device['vendor']}")
            if device['services']:
                print(f"   Services: {', '.join(device['services'])}")
        
        print("\n" + "="*60)
        
        # Save to file
        self.save_results(devices, switches)
    
    def save_results(self, devices: List[Dict[str, Any]], switches: List[Dict[str, Any]]):
        """Save results to JSON file"""
        try:
            results = {
                'timestamp': str(__import__('datetime').datetime.now()),
                'total_devices': len(devices),
                'switches_found': len(switches),
                'switches': switches,
                'all_devices': devices
            }
            
            with open('network_discovery_results.json', 'w') as f:
                json.dump(results, f, indent=2)
            
            print(f"\n💾 Results saved to: network_discovery_results.json")
            
        except Exception as e:
            print(f"Error saving results: {e}")


def main():
    """Main function"""
    try:
        # Check for dependencies
        try:
            import netifaces
        except ImportError:
            print("❌ Missing required package: netifaces")
            print("📦 Install with: pip install netifaces")
            return
        
        # Create discovery instance
        discovery = NetworkDiscovery()
        
        # Discover network
        devices = discovery.discover_network()
        
        # Print results
        discovery.print_results(devices)
        
        print("\n✅ Network discovery complete!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
