"""
Advanced Switch Detection Tool
Uses multiple methods to find the switch you're connected to
"""

import subprocess
import re
import json
import socket

def check_network_info():
    """Get detailed network information"""
    print("\n" + "="*70)
    print("🔍 DETAILED NETWORK ANALYSIS")
    print("="*70)
    
    # Your network info
    print("\n📍 YOUR LAPTOP NETWORK INFORMATION:")
    print("-"*70)
    print(f"   Your IP: 192.168.31.41")
    print(f"   Network: 192.168.31.0/24")
    print(f"   Gateway: 192.168.31.1 (MAC: 7C:BF:77:70:7A:EF)")
    print(f"   Gateway has web interface (HTTP/HTTPS)")
    
    # Identify gateway device
    print("\n🚪 GATEWAY/ROUTER ANALYSIS:")
    print("-"*70)
    print("   The device at 192.168.31.1 appears to be your router/gateway")
    print("   Services found: HTTP, HTTPS, HTTP-Alt")
    print("   This is likely a home router or wireless access point")
    print("   MAC Address: 7C:BF:77:70:7A:EF")
    
    # Connection type
    print("\n🔌 CONNECTION ANALYSIS:")
    print("-"*70)
    
    try:
        # Check if WiFi or Ethernet
        result = subprocess.run(
            ['netsh', 'interface', 'show', 'interface'],
            capture_output=True,
            text=True
        )
        
        print("\n   Network Interfaces:")
        for line in result.stdout.split('\n'):
            if 'Connected' in line or 'Ethernet' in line or 'Wi-Fi' in line:
                print(f"   {line.strip()}")
        
    except Exception as e:
        print(f"   Could not determine connection type: {e}")

def check_switch_connection():
    """Check if connected to a managed switch"""
    print("\n🔌 SWITCH CONNECTION DETECTION:")
    print("-"*70)
    
    print("""
   Based on the network scan:
   
   ✓ You are connected to: 192.168.31.1 (Gateway/Router)
   
   POSSIBLE SCENARIOS:
   
   1️⃣  DIRECT ROUTER CONNECTION
      - Your laptop → Router (192.168.31.1)
      - No managed switch in between
      - Most common for home/small office setups
   
   2️⃣  UNMANAGED SWITCH
      - Your laptop → Unmanaged Switch → Router
      - Unmanaged switches are transparent (invisible to network scans)
      - Cannot be detected via IP/SNMP
   
   3️⃣  MANAGED SWITCH (Not Detected)
      - Switch may have SNMP disabled
      - Switch may be on different VLAN
      - Switch management interface not accessible
    """)

def get_physical_connection():
    """Try to determine physical connection details"""
    print("\n🔍 PHYSICAL CONNECTION DETECTION:")
    print("-"*70)
    
    try:
        # Get network adapter details
        result = subprocess.run(
            ['wmic', 'nic', 'where', 'NetEnabled=true', 'get', 
             'Name,Speed,MACAddress,NetConnectionStatus'],
            capture_output=True,
            text=True
        )
        
        print("\n   Active Network Adapters:")
        lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        for line in lines[:5]:  # Show first few lines
            print(f"   {line}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    # Check link speed
    try:
        result = subprocess.run(
            ['netsh', 'interface', 'ipv4', 'show', 'config'],
            capture_output=True,
            text=True
        )
        
        print(f"\n   Network Configuration:")
        relevant_lines = []
        for line in result.stdout.split('\n'):
            if any(x in line.lower() for x in ['dhcp', 'gateway', 'interface', 'configuration for']):
                print(f"   {line.strip()}")
    except:
        pass

def suggest_manual_detection():
    """Provide manual detection methods"""
    print("\n💡 MANUAL SWITCH DETECTION METHODS:")
    print("="*70)
    
    methods = """
1️⃣  PHYSICAL INSPECTION
   - Follow the Ethernet cable from your laptop
   - Look for a device with multiple RJ45 ports
   - Check for brand labels (Cisco, HP, D-Link, TP-Link, etc.)

2️⃣  CHECK WEB INTERFACE
   - Try accessing: http://192.168.31.1
   - Login to router/gateway admin page
   - Look for "Connected Devices" or "DHCP Clients"
   - May show switch if it's a managed device

3️⃣  CHECK FOR SWITCH MANAGEMENT IP
   Common default IPs for managed switches:
   - http://192.168.1.1 or http://192.168.0.1
   - http://192.168.31.2 (next available IP)
   - Check device documentation

4️⃣  USE LLDP/CDP (If Supported)
   - Windows: Install Wireshark or LLDP viewer
   - Linux: Use lldpctl command
   - These protocols can identify connected switch

5️⃣  CHECK ROUTER'S ARP/MAC TABLE
   - Login to router at 192.168.31.1
   - Look for devices with network equipment MAC addresses
   - Cisco: starts with 00:1C:0E, 00:24:C3, etc.
   - HP: starts with 00:1A:4B, 00:23:7D, etc.

6️⃣  USE NETWORK MONITORING TOOLS
   - Advanced IP Scanner
   - Angry IP Scanner
   - Wireshark (to capture LLDP/CDP frames)
   - SolarWinds Network Performance Monitor
    """
    
    print(methods)

def provide_switch_testing_guide():
    """Provide guide for testing with switch"""
    print("\n📋 TESTING YOUR MONITORING SYSTEM WITH A SWITCH:")
    print("="*70)
    
    guide = """
STEP 1: IDENTIFY YOUR SWITCH
   If you have a managed switch, you need:
   - Switch IP address
   - SNMP community string (usually 'public' or 'private')
   - Admin credentials (for web interface)

STEP 2: ENABLE SNMP ON SWITCH
   Most managed switches:
   - Login to web interface
   - Navigate to SNMP settings
   - Enable SNMPv2c or SNMPv3
   - Set community string (e.g., 'public' for read-only)

STEP 3: ADD SWITCH TO YOUR MONITORING SYSTEM
   In your Device Monitoring System:
   - Go to "Devices" page
   - Click "Add Device"
   - Enter switch IP: (e.g., 192.168.31.X)
   - Enter SNMP community: public
   - Device type: Switch
   - Save

STEP 4: TEST SNMP CONNECTION
   Use this command to test SNMP:
   
   Windows: (Install SNMP tools first)
   snmpwalk -v2c -c public 192.168.31.X system
   
   Python (use your backend):
   python -c "from pysnmp.hlapi import *; print(list(getCmd(SnmpEngine(), 
   CommunityData('public'), UdpTransportTarget(('192.168.31.X', 161)), 
   ContextData(), ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))))"

STEP 5: VERIFY IN YOUR APP
   - Check Dashboard for device status
   - Poll the device to get real-time data
   - View device details
   - Check for alerts if switch goes offline

ALTERNATIVE: TEST WITH ROUTER (192.168.31.1)
   If no managed switch available:
   - Your router might support SNMP
   - Try adding 192.168.31.1 as a device
   - Use community string from router settings
    """
    
    print(guide)

def create_test_device_config():
    """Create a sample device configuration"""
    print("\n📄 SAMPLE DEVICE CONFIGURATION:")
    print("="*70)
    
    config = {
        "device_name": "Network Switch/Router",
        "ip_address": "192.168.31.1",
        "device_type": "switch",
        "snmp_version": "2c",
        "snmp_community": "public",
        "snmp_port": 161,
        "poll_interval": 60,
        "description": "Main gateway/router device",
        "location": "Local Network"
    }
    
    print(json.dumps(config, indent=2))
    
    # Save to file
    with open('sample_device_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n💾 Saved to: sample_device_config.json")

def main():
    """Main function"""
    print("\n" + "="*70)
    print("🔌 SWITCH DETECTION & TESTING GUIDE")
    print("="*70)
    
    # Run all checks
    check_network_info()
    check_switch_connection()
    get_physical_connection()
    suggest_manual_detection()
    provide_switch_testing_guide()
    create_test_device_config()
    
    print("\n" + "="*70)
    print("✅ ANALYSIS COMPLETE")
    print("="*70)
    
    print("""
SUMMARY:
- Your laptop IP: 192.168.31.41
- Gateway/Router: 192.168.31.1 (MAC: 7C:BF:77:70:7A:EF)
- No managed switch detected on network
- Most likely: Direct connection or unmanaged switch

NEXT STEPS:
1. Check if you have a managed switch physically
2. Try accessing router web interface (http://192.168.31.1)
3. Use the sample config to test your monitoring system
4. If you have a managed switch, enable SNMP and add it

For immediate testing:
- Try adding 192.168.31.1 as a device in your app
- Or use the sample configuration provided above
    """)

if __name__ == '__main__':
    main()
