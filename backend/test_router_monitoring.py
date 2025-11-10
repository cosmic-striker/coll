"""
Quick Test - Add Router/Switch to Monitoring System
Tests if your router at 192.168.31.1 supports SNMP
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Device

try:
    from pysnmp.hlapi import *
except ImportError:
    print("Warning: pysnmp not available, SNMP features will be limited")

def test_snmp_connection(ip, community='public', port=161):
    """Test SNMP connection to device"""
    print(f"\n🔍 Testing SNMP connection to {ip}...")
    print("-" * 60)
    
    try:
        # Try to get system description
        iterator = getCmd(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((ip, port), timeout=2, retries=1),
            ContextData(),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))
        )
        
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        
        if errorIndication:
            print(f"❌ SNMP Error: {errorIndication}")
            return False, None
        elif errorStatus:
            print(f"❌ SNMP Error: {errorStatus.prettyPrint()}")
            return False, None
        else:
            for varBind in varBinds:
                desc = varBind[1].prettyPrint()
                print(f"✅ SNMP Connection Successful!")
                print(f"   System Description: {desc}")
                return True, desc
    
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False, None

def add_device_to_system(ip, name, device_type='switch'):
    """Add device to monitoring system"""
    print(f"\n📝 Adding device to monitoring system...")
    print("-" * 60)
    
    try:
        app = create_app()
        
        with app.app_context():
            # Check if device already exists
            existing = Device.query.filter_by(ip_address=ip).first()
            
            if existing:
                print(f"⚠️  Device already exists: {existing.name}")
                print(f"   Device ID: {existing.id}")
                print(f"   Status: {existing.status}")
                return existing
            
            # Create new device
            device = Device(
                name=name,
                ip_address=ip,
                device_type=device_type,
                vendor='Unknown',
                snmp_community='public',
                status='unknown',
                meta={
                    'description': 'Network gateway/router device',
                    'location': 'Local Network',
                    'snmp_version': '2c',
                    'snmp_port': 161,
                    'poll_interval': 60
                }
            )
            
            db.session.add(device)
            db.session.commit()
            
            print(f"✅ Device added successfully!")
            print(f"   Device ID: {device.id}")
            print(f"   Name: {device.name}")
            print(f"   IP: {device.ip_address}")
            print(f"   Type: {device.device_type}")
            
            return device
    
    except Exception as e:
        print(f"❌ Error adding device: {e}")
        import traceback
        traceback.print_exc()
        return None

def poll_device(device_id):
    """Poll a device to get current data"""
    print(f"\n🔄 Polling device {device_id}...")
    print("-" * 60)
    
    try:
        app = create_app()
        
        with app.app_context():
            from app.device_scanner import DeviceScanner
            
            device = Device.query.get(device_id)
            if not device:
                print(f"❌ Device not found")
                return
            
            scanner = DeviceScanner()
            result = scanner.poll_device(device)
            
            print(f"✅ Poll completed!")
            print(f"   Status: {device.status}")
            print(f"   Response Time: {device.response_time}ms" if device.response_time else "   Response Time: N/A")
            
            if result:
                print(f"\n📊 Device Information:")
                for key, value in result.items():
                    print(f"   {key}: {value}")
            
            return result
    
    except Exception as e:
        print(f"❌ Error polling device: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main testing function"""
    print("\n" + "="*70)
    print("🧪 ROUTER/SWITCH MONITORING TEST")
    print("="*70)
    
    # Your network details
    router_ip = "192.168.31.1"
    router_name = "Main Gateway/Router"
    
    print(f"\nTarget Device:")
    print(f"   IP: {router_ip}")
    print(f"   Name: {router_name}")
    
    # Step 1: Test SNMP
    print("\n" + "="*70)
    print("STEP 1: Test SNMP Connection")
    print("="*70)
    
    snmp_works, sys_desc = test_snmp_connection(router_ip)
    
    if not snmp_works:
        print("\n⚠️  SNMP is not available on this device")
        print("\nPossible reasons:")
        print("   - Router doesn't support SNMP")
        print("   - SNMP is disabled (check router settings)")
        print("   - Firewall blocking SNMP port 161")
        print("\nAlternative: Try ping-only monitoring")
        
        # Try ping test
        print("\n" + "="*70)
        print("Testing PING connectivity...")
        print("="*70)
        
        import subprocess
        result = subprocess.run(
            ['ping', '-n', '1', router_ip],
            capture_output=True,
            timeout=2
        )
        
        if result.returncode == 0:
            print(f"✅ Device responds to PING")
            print("   You can monitor this device with ping-only mode")
        else:
            print(f"❌ Device doesn't respond to PING")
    
    # Step 2: Add to monitoring system
    print("\n" + "="*70)
    print("STEP 2: Add Device to Monitoring System")
    print("="*70)
    
    device = add_device_to_system(router_ip, router_name, 'switch')
    
    if not device:
        print("\n❌ Failed to add device to system")
        return
    
    # Step 3: Poll device
    print("\n" + "="*70)
    print("STEP 3: Poll Device")
    print("="*70)
    
    poll_device(device.id)
    
    # Summary
    print("\n" + "="*70)
    print("✅ TEST COMPLETE")
    print("="*70)
    
    print(f"""
SUMMARY:
   Device: {router_name}
   IP: {router_ip}
   SNMP: {'✅ Available' if snmp_works else '❌ Not available'}
   
NEXT STEPS:
   1. Open your web browser
   2. Go to: http://localhost:5000 (or your frontend URL)
   3. Login to your monitoring system
   4. Navigate to "Devices" page
   5. You should see "{router_name}" in the device list
   6. Click on it to view details
   
If SNMP is not available:
   - Login to router at http://{router_ip}
   - Enable SNMP in router settings
   - Set community string to 'public'
   - Then run this test again
    """)

if __name__ == '__main__':
    main()
