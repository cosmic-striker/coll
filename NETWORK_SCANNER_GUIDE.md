# 🔍 Network Scanner Feature Guide

## Overview
A powerful network scanning tool that discovers all devices on your local network and allows you to selectively add them to your monitoring system.

## Features

### ✨ Core Functionality
- **Automatic Network Discovery**: Scans your entire network subnet
- **Device Identification**: Identifies cameras, switches, routers, computers
- **Vendor Detection**: Recognizes device manufacturers from MAC addresses
- **Service Detection**: Scans common ports to identify device capabilities
- **Selective Import**: Accept or reject each discovered device
- **Bulk Actions**: Accept/reject multiple devices at once

### 🎯 Access the Scanner

**Navigation**: The "🔍 Scan Network" button is positioned on the **right side** of the navigation bar, before the "Logout" button.

**Direct URL**: `frontend/public/network_scan.html`

---

## How It Works

### 1. Network Discovery Process

```
Start Scan
    ↓
Get Network Info (10%)
    ↓
Scan ARP Table (30%)
    ↓
Discover Devices (50%)
    ↓
Identify Types (80%)
    ↓
Complete (100%)
```

### 2. Device Detection Methods

| Method | Purpose |
|--------|---------|
| **ARP Table** | Find all devices with IP addresses on network |
| **MAC Address OUI** | Identify device manufacturer/vendor |
| **Port Scanning** | Detect services (HTTP, RTSP, SNMP, etc.) |
| **Service Analysis** | Determine device type (camera, switch, etc.) |

### 3. Device Types Detected

- 🌐 **Routers/Gateways** - Network routing devices
- 🔌 **Switches** - Managed/unmanaged network switches
- 📹 **IP Cameras** - RTSP-enabled surveillance cameras
- 🖥️ **Computers** - Desktops, laptops, workstations
- 🖧 **Servers** - File servers, web servers
- 📱 **IoT Devices** - Smart devices and appliances
- ❓ **Unknown** - Unidentified network devices

---

## Using the Scanner

### Step 1: Start Scan

1. Navigate to **"🔍 Scan Network"** in the top navigation
2. Click **"Start Network Scan"** button
3. Wait for scan to complete (1-2 minutes)

### Step 2: Review Discovered Devices

Each device card shows:
- **Device Icon** - Visual representation of device type
- **Device Name** - Auto-generated or vendor-based name
- **Type Badge** - Camera, Switch, Router, etc.
- **IP Address** - Network IP address
- **MAC Address** - Physical hardware address
- **Vendor** - Manufacturer (Cisco, Dahua, etc.)
- **Services** - Detected services (HTTP, RTSP, SNMP)

### Step 3: Accept or Reject Devices

**Individual Actions**:
- ✅ **Accept** - Adds device to monitoring system
- ❌ **Reject** - Ignores device (won't be added)

**Bulk Actions**:
- **Accept All** - Add all pending devices
- **Reject All** - Reject all pending devices
- **Accept All Cameras** - Add only cameras
- **Accept All Switches** - Add only switches

### Step 4: Device Added Confirmation

Once accepted:
- ✅ Card turns green with "Added to System" badge
- Device appears in "Devices" or "Cameras" page
- Automatic monitoring begins

---

## Device Type Rules

### Cameras (📹)
**Auto-detected if**:
- Vendor: Dahua, Hikvision, Axis
- Port 554 open (RTSP)

**Added as**: Camera with RTSP URL `rtsp://[IP]:554/live`

### Switches (🔌)
**Auto-detected if**:
- Vendor: Cisco, HP, D-Link, TP-Link, Netgear, Ubiquiti
- Port 161 open (SNMP)

**Added as**: Device with SNMP monitoring enabled

### Routers (🌐)
**Auto-detected if**:
- Ports 80, 443, 8080 open (Web interface)
- Typically the gateway device

**Added as**: Network device with ping monitoring

---

## API Endpoint

### POST `/api/network/scan`

**Request**:
```json
Headers:
  Authorization: Bearer [token]
```

**Response**:
```json
{
  "success": true,
  "devices": [
    {
      "ip": "192.168.31.100",
      "mac": "00:1C:0E:12:34:56",
      "vendor": "Cisco",
      "type": "switch",
      "name": "Cisco Switch",
      "ports": [161, 80],
      "services": ["SNMP", "HTTP"]
    }
  ],
  "count": 5
}
```

---

## Supported Vendors

### Network Equipment
- **Cisco** - MAC: `00:1C:0E`, `00:24:C3`, `F4:CF:E2`
- **HP/3Com** - MAC: `00:D0:D3`, `00:0F:E2`, `00:1A:4B`
- **D-Link** - MAC: `00:0E:7F`, `00:17:9A`
- **TP-Link** - MAC: `28:10:7B`, `C4:E9:84`, `50:C7:BF`
- **Netgear** - MAC: `00:13:3B`, `00:24:B2`, `A0:63:91`
- **Ubiquiti** - MAC: `00:03:7F`, `00:15:6D`, `68:D7:9A`

### Cameras
- **Dahua** - MAC: `00:12:34`
- **Hikvision** - MAC: `00:11:32`
- **Axis** - MAC: `00:40:8C`

---

## Port Scanning

### Common Ports Scanned

| Port | Service | Indicates |
|------|---------|-----------|
| 80 | HTTP | Web interface |
| 443 | HTTPS | Secure web interface |
| 22 | SSH | Remote administration |
| 23 | Telnet | Remote terminal |
| 161 | SNMP | Network monitoring |
| 554 | RTSP | Video streaming |
| 8080 | HTTP-Alt | Alternative web port |
| 3389 | RDP | Windows remote desktop |
| 21 | FTP | File transfer |

---

## UI Components

### Navigation
```css
margin-left: auto;  /* Pushes "Scan Network" to the right */
```

The scan button appears on the **right side** of the navigation, separated from other menu items.

### Device Cards

**States**:
1. **Pending** - White/default background, shows Accept/Reject buttons
2. **Accepted** - Green background, shows "✅ Added to System"
3. **Rejected** - Red background (faded), shows "❌ Rejected"

### Progress Bar
- Animated progress indicator
- Shows percentage completion
- Displays current scan stage

---

## Examples

### Example 1: Adding a Camera

```
Device Discovered:
  IP: 192.168.31.150
  MAC: 00:12:34:56:78:90
  Vendor: Dahua
  Type: Camera
  Services: RTSP, HTTP

Action: Click "✅ Accept"

Result: 
  Added to Cameras page
  RTSP URL: rtsp://192.168.31.150:554/live
  Ready for live streaming
```

### Example 2: Adding a Switch

```
Device Discovered:
  IP: 192.168.31.100
  MAC: 00:1C:0E:12:34:56
  Vendor: Cisco
  Type: Switch
  Services: SNMP, HTTP

Action: Click "✅ Accept"

Result:
  Added to Devices page
  SNMP community: public
  Monitoring enabled
```

### Example 3: Bulk Accept Cameras

```
Devices Found: 5 cameras
Action: Click "📹 Accept All Cameras"

Result:
  All 5 cameras added to system
  Available in Live Feeds page
  Monitoring started automatically
```

---

## Troubleshooting

### No Devices Found

**Possible Causes**:
- No other devices on network
- Firewall blocking scans
- Network isolation/VLANs

**Solutions**:
- Check physical network connections
- Verify devices are powered on
- Try disabling firewall temporarily
- Ensure on same subnet

### Wrong Device Type

**Issue**: Camera detected as "Unknown"

**Cause**: Vendor not in database or no RTSP port

**Solution**: 
- Accept as-is, then edit in Devices/Cameras page
- Or reject and add manually

### Scan Takes Too Long

**Normal Duration**: 1-2 minutes for 10-20 devices

**If Longer**:
- Large network (50+ devices)
- Slow network response
- Many unreachable IPs being scanned

**Optimization**: Reduce port scan timeout (requires backend edit)

---

## Security Considerations

### Best Practices

1. **Authentication Required** - Only logged-in users can scan
2. **Local Network Only** - Scans only local subnet
3. **Non-Intrusive** - Uses ARP table + light port scanning
4. **Review Before Adding** - Manual accept/reject prevents auto-import
5. **Audit Trail** - Devices marked as "auto-discovered" in metadata

### Permissions

- Requires **authenticated user** (JWT token)
- No special admin permissions needed
- All users can discover and add devices

---

## Future Enhancements

### Planned Features

1. **VLAN Support** - Scan multiple VLANs
2. **Scheduled Scans** - Auto-discover new devices daily
3. **Custom Port Lists** - User-defined ports to scan
4. **SNMP Walking** - Get device details via SNMP
5. **LLDP/CDP** - Use discovery protocols
6. **Export Results** - Save scan results to CSV/JSON
7. **Comparison Mode** - Compare current vs previous scans
8. **Auto-Classification** - ML-based device type detection

---

## Files Modified

### Frontend
- ✅ `dashboard.html` - Added nav link
- ✅ `device_details.html` - Added nav link
- ✅ `cameras.html` - Added nav link  
- ✅ `live_feeds.html` - Added nav link
- ✅ `alerts.html` - Added nav link
- ✅ `settings.html` - Added nav link
- ✅ `users.html` - Added nav link
- ✅ `network_scan.html` - **NEW** Main scanner page

### Backend
- ✅ `app/routes/network.py` - **NEW** Network scan API
- ✅ `app/routes/__init__.py` - Registered network blueprint

---

## Testing

### Quick Test

1. Login to your application
2. Click "🔍 Scan Network" (top-right navigation)
3. Click "Start Network Scan"
4. Wait for results
5. Accept test device
6. Verify in Devices/Cameras page

### Expected Results

- Should find your router/gateway
- May find your own laptop
- Will find any IP cameras on network
- Will find managed switches if present

---

## Keyboard Shortcuts (Future)

- `Ctrl+N` - Start new scan
- `Ctrl+A` - Accept all
- `Ctrl+R` - Reject all
- `Esc` - Cancel scan

---

**Feature Status**: ✅ Production Ready  
**Last Updated**: November 9, 2025  
**Version**: 1.0.0
