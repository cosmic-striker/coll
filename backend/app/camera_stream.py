# camera_stream.py - RTSP Camera Streaming Module

import cv2
import threading
import time
import logging
from flask import Response, jsonify
import numpy as np
from datetime import datetime
import base64
import io

logger = logging.getLogger(__name__)

class CameraStreamer:
    """Manages RTSP camera streams"""

    def __init__(self):
        self.streams = {}  # camera_id -> stream_info
        self.frames = {}   # camera_id -> latest_frame
        self.threads = {}  # camera_id -> thread
        self.stop_flags = {}  # camera_id -> stop_flag

    def start_stream(self, camera_id, rtsp_url, username=None, password=None):
        """Start streaming from RTSP URL"""
        if camera_id in self.streams:
            self.stop_stream(camera_id)

        # Build RTSP URL with credentials if provided
        stream_url = rtsp_url
        if username and password:
            # Insert credentials into RTSP URL
            if 'rtsp://' in rtsp_url:
                stream_url = rtsp_url.replace('rtsp://', f'rtsp://{username}:{password}@')

        stop_flag = threading.Event()
        self.stop_flags[camera_id] = stop_flag

        thread = threading.Thread(
            target=self._stream_worker,
            args=(camera_id, stream_url, stop_flag),
            daemon=True
        )

        self.streams[camera_id] = {
            'url': stream_url,
            'status': 'starting',
            'start_time': datetime.now(),
            'frame_count': 0,
            'last_frame_time': None
        }

        self.threads[camera_id] = thread
        thread.start()

        return True

    def stop_stream(self, camera_id):
        """Stop streaming for a camera"""
        if camera_id in self.stop_flags:
            self.stop_flags[camera_id].set()

        if camera_id in self.threads:
            self.threads[camera_id].join(timeout=2)

        # Clean up
        self.streams.pop(camera_id, None)
        self.frames.pop(camera_id, None)
        self.threads.pop(camera_id, None)
        self.stop_flags.pop(camera_id, None)

    def get_frame(self, camera_id):
        """Get the latest frame for a camera"""
        return self.frames.get(camera_id)

    def get_stream_info(self, camera_id):
        """Get information about a stream"""
        return self.streams.get(camera_id, {})

    def list_active_streams(self):
        """List all active streams"""
        return list(self.streams.keys())

    def _stream_worker(self, camera_id, rtsp_url, stop_flag):
        """Worker thread for streaming RTSP"""
        logger.info(f"Starting RTSP stream for camera {camera_id}: {rtsp_url}")

        cap = None
        try:
            # Open RTSP stream
            cap = cv2.VideoCapture(rtsp_url)

            if not cap.isOpened():
                logger.error(f"Failed to open RTSP stream for camera {camera_id}")
                self.streams[camera_id]['status'] = 'failed'
                return

            self.streams[camera_id]['status'] = 'streaming'
            logger.info(f"RTSP stream started successfully for camera {camera_id}")

            frame_count = 0
            while not stop_flag.is_set():
                ret, frame = cap.read()

                if not ret:
                    logger.warning(f"Failed to read frame from camera {camera_id}")
                    time.sleep(1)
                    continue

                # Store the frame
                self.frames[camera_id] = frame
                frame_count += 1

                # Update stream info
                self.streams[camera_id]['frame_count'] = frame_count
                self.streams[camera_id]['last_frame_time'] = datetime.now()

                # Small delay to prevent excessive CPU usage
                time.sleep(0.1)

        except Exception as e:
            logger.error(f"Error in stream worker for camera {camera_id}: {str(e)}")
            self.streams[camera_id]['status'] = 'error'
        finally:
            if cap:
                cap.release()
            logger.info(f"RTSP stream stopped for camera {camera_id}")

# Global streamer instance
streamer = CameraStreamer()

def start_camera_stream(camera_id, rtsp_url, username=None, password=None):
    """Start streaming for a camera"""
    return streamer.start_stream(camera_id, rtsp_url, username, password)

def stop_camera_stream(camera_id):
    """Stop streaming for a camera"""
    streamer.stop_stream(camera_id)

def get_camera_frame(camera_id):
    """Get the latest frame from a camera stream"""
    return streamer.get_frame(camera_id)

def get_camera_stream_info(camera_id):
    """Get stream information for a camera"""
    return streamer.get_stream_info(camera_id)

def test_rtsp_connection(rtsp_url, username=None, password=None, timeout=10):
    """Test RTSP connection without starting a full stream"""
    test_url = rtsp_url
    if username and password:
        if 'rtsp://' in rtsp_url:
            test_url = rtsp_url.replace('rtsp://', f'rtsp://{username}:{password}@')

    try:
        cap = cv2.VideoCapture(test_url)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer

        if cap.isOpened():
            # Try to read a frame
            ret, frame = cap.read()
            cap.release()

            if ret and frame is not None:
                return True, "RTSP stream is accessible"
            else:
                return False, "Can connect but cannot read frames"
        else:
            return False, "Cannot open RTSP stream"

    except Exception as e:
        return False, f"RTSP test failed: {str(e)}"

def generate_mjpeg_stream(camera_id):
    """Generate MJPEG stream for a camera"""
    while True:
        frame = get_camera_frame(camera_id)
        if frame is not None:
            # Encode frame as JPEG
            ret, jpeg = cv2.imencode('.jpg', frame)
            if ret:
                # Yield the frame in MJPEG format
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            # No frame available, wait
            time.sleep(0.1)

def get_snapshot_base64(camera_id):
    """Get a snapshot from camera as base64 string"""
    frame = get_camera_frame(camera_id)
    if frame is not None:
        ret, jpeg = cv2.imencode('.jpg', frame)
        if ret:
            return base64.b64encode(jpeg.tobytes()).decode('utf-8')
    return None

def list_active_streams():
    """List all active camera streams"""
    return streamer.list_active_streams()
