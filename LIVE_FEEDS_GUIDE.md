# 📹 Live Feeds Feature Guide

## Overview
A dedicated page for viewing live camera RTSP streams with external player support.

## Features

### ✨ Core Functionality
- **Real-time Camera Grid**: Display up to 8 online cameras simultaneously
- **Configurable Stream Limit**: Choose 2, 4, 6, or 8 concurrent feeds
- **RTSP URL Management**: Copy URLs to clipboard or open in external players
- **Auto-refresh**: Manual refresh button for updating camera list
- **Responsive Design**: Adapts to desktop, tablet, and mobile screens

### 🎯 Key Components

#### 1. Camera Feed Cards
Each camera displays:
- Camera name and online status
- Visual placeholder (gradient background with camera icon)
- Copy URL button (copies RTSP link to clipboard)
- Open in Player button (attempts to launch external player)
- Camera details (location, IP address, brand)

#### 2. Stream Controls
- **Max Feeds Selector**: Dropdown to limit concurrent streams (2/4/6/8)
- **Refresh Button**: Reload camera list from backend
- **Active Count Badge**: Shows number of displayed cameras

#### 3. Instructions Section
Built-in guide showing:
- Desktop player options (VLC, ffplay, PotPlayer)
- Mobile app recommendations
- Browser viewing options

## How to Use

### For Users

1. **Navigate to Live Feeds**
   - Click "Live Feeds" in the main navigation
   - Or go directly to `live_feeds.html`

2. **View Camera Streams**
   - Online cameras load automatically
   - Click "Copy URL" to copy RTSP link
   - Click "Open in Player" to launch external viewer

3. **Adjust Settings**
   - Use "Max Feeds" dropdown to change display limit
   - Click "Refresh" to update camera list

4. **Open in External Player**
   - **VLC**: Media → Open Network Stream → Paste URL
   - **ffplay**: Run `ffplay rtsp://[camera-url]`
   - **Mobile**: Use VLC or RTSP Player app

### For Developers

#### File Structure
```
frontend/public/
├── live_feeds.html          # Main page
├── assets/
│   ├── app.js              # API client
│   ├── utils.js            # Helper functions
│   ├── theme.js            # Theme management
│   └── style.css           # Styles
```

#### Key Functions

```javascript
// Load and display camera feeds
async function loadCameraFeeds()

// Copy RTSP URL to clipboard
function copyRtspUrl(rtspUrl, cameraName)

// Open stream in external player
function openStream(rtspUrl, cameraName)

// Update maximum concurrent streams
function updateMaxFeeds()
```

#### API Endpoints Used
- `GET /api/cameras/` - List all cameras
- `GET /api/cameras/status` - Get camera status summary

## Browser Compatibility

### ✅ Supported
- **Copy to Clipboard**: Modern browsers (Chrome, Firefox, Edge, Safari)
- **Protocol Handlers**: If configured (e.g., VLC protocol handler)
- **Responsive Layout**: All modern browsers

### ⚠️ Limitations
- **Native RTSP Playback**: Not supported in browsers
  - Requires external player (VLC, ffplay, etc.)
  - Or server-side transcoding to HLS/WebRTC
  
## Future Enhancements

### Potential Improvements
1. **WebRTC/HLS Support**
   - Add server-side transcoding
   - Enable in-browser playback
   - Use libraries like hls.js or video.js

2. **Grid Layout Options**
   - Fullscreen mode
   - Picture-in-picture
   - Custom grid arrangements

3. **Recording Features**
   - Snapshot capture
   - Video recording
   - Cloud storage integration

4. **Advanced Controls**
   - PTZ controls (Pan/Tilt/Zoom)
   - Quality selection
   - Audio toggle

5. **Multi-camera Features**
   - Split-screen view
   - Synchronized playback
   - Multi-camera recording

## Troubleshooting

### Cameras Not Showing
**Problem**: No feeds displayed  
**Solutions**:
- Check cameras are marked "online" in Cameras page
- Verify RTSP URLs are configured correctly
- Check backend API is running
- Look for errors in browser console

### Cannot Open Stream
**Problem**: "Open in Player" doesn't work  
**Solutions**:
- Install VLC or another RTSP player
- Manually copy URL and paste in player
- Check firewall allows RTSP connections
- Verify camera credentials are correct

### Copy URL Fails
**Problem**: Copy button doesn't work  
**Solutions**:
- Enable clipboard permissions in browser
- Use HTTPS (clipboard API requires secure context)
- Manually select and copy RTSP URL from camera details

## Security Considerations

### Best Practices
1. **RTSP URLs**: May contain credentials - handle securely
2. **HTTPS**: Use HTTPS to protect clipboard operations
3. **Authentication**: Ensure only authorized users access feeds
4. **Network**: Use VPN for remote access to cameras
5. **Credentials**: Store camera passwords securely in backend

## Technical Details

### RTSP Protocol
- **Port**: Usually 554
- **Format**: `rtsp://username:password@ip:port/stream`
- **Transport**: TCP/UDP
- **Codecs**: H.264, H.265, MJPEG (camera-dependent)

### Performance
- **Max Streams**: Limited by client network bandwidth
- **Recommended**: 4 concurrent 1080p streams on typical connection
- **Optimization**: Lower resolution or framerate if needed

### Styling
- **Theme Support**: Inherits from main theme system
- **Responsive Breakpoint**: 768px for mobile layout
- **Card Aspect Ratio**: 16:9 for video placeholder
- **Grid**: Auto-fill with min 350px cards

## Example RTSP URLs

### Common Formats
```bash
# Dahua
rtsp://admin:password@192.168.1.100:554/cam/realmonitor?channel=1&subtype=0

# Hikvision
rtsp://admin:password@192.168.1.101:554/Streaming/Channels/101

# CP Plus
rtsp://admin:password@192.168.1.102:554/live

# Generic
rtsp://username:password@ip:port/stream
```

## Navigation Integration

The "Live Feeds" link has been added to all pages:
- ✅ dashboard.html
- ✅ device_details.html
- ✅ cameras.html
- ✅ alerts.html
- ✅ settings.html
- ✅ users.html

## Testing Checklist

- [ ] Page loads without errors
- [ ] Online cameras are displayed
- [ ] Copy URL button works
- [ ] Max feeds selector changes grid
- [ ] Refresh button updates data
- [ ] Instructions section is readable
- [ ] Responsive layout works on mobile
- [ ] Navigation links work correctly
- [ ] Toast notifications appear
- [ ] Loading states display properly

## Related Documentation
- [Camera Setup Guide](SETUP.md)
- [API Documentation](backend/README.md)
- [Frontend Structure](frontend/README.md)
- [Troubleshooting](TROUBLESHOOTING.md)

---

**Last Updated**: November 9, 2025  
**Version**: 1.0.0  
**Status**: Production Ready ✅
