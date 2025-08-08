import re
import ipaddress
from cryptography.fernet import Fernet
from flask import current_app
import base64
import hashlib
import secrets
from datetime import datetime, timedelta
import json

def validate_ip_address(ip):
    """Validate IP address format"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_url(url):
    """Validate URL format"""
    pattern = r'^https?://.+|^rtsp://.+'
    return re.match(pattern, url) is not None

def generate_encryption_key():
    """Generate a new encryption key"""
    return Fernet.generate_key()

def encrypt_password(password, key=None):
    """Encrypt password using Fernet symmetric encryption"""
    try:
        if key is None:
            # Use app secret key to derive encryption key
            secret = current_app.config['SECRET_KEY'].encode()
            key = base64.urlsafe_b64encode(hashlib.sha256(secret).digest())
        
        f = Fernet(key)
        encrypted = f.encrypt(password.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    except Exception:
        # Fallback to base64 encoding if encryption fails
        return base64.b64encode(password.encode()).decode()

def decrypt_password(encrypted_password, key=None):
    """Decrypt password using Fernet symmetric encryption"""
    try:
        if key is None:
            # Use app secret key to derive encryption key
            secret = current_app.config['SECRET_KEY'].encode()
            key = base64.urlsafe_b64encode(hashlib.sha256(secret).digest())
        
        f = Fernet(key)
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_password.encode())
        decrypted = f.decrypt(encrypted_bytes)
        return decrypted.decode()
    except Exception:
        # Fallback to base64 decoding if decryption fails
        try:
            return base64.b64decode(encrypted_password.encode()).decode()
        except Exception:
            return encrypted_password  # Return as-is if all else fails

def generate_secure_token(length=32):
    """Generate a cryptographically secure random token"""
    return secrets.token_urlsafe(length)

def sanitize_filename(filename):
    """Sanitize filename for safe storage"""
    # Remove dangerous characters
    filename = re.sub(r'[^\w\s-.]', '', filename)
    # Replace spaces with underscores
    filename = re.sub(r'\s+', '_', filename)
    # Remove multiple dots
    filename = re.sub(r'\.+', '.', filename)
    return filename.strip('._')

def parse_snmp_response(response):
    """Parse SNMP response data"""
    try:
        if isinstance(response, dict):
            return response
        elif isinstance(response, str):
            return json.loads(response)
        else:
            return {'raw_response': str(response)}
    except (json.JSONDecodeError, Exception):
        return {'raw_response': str(response)}

def format_uptime(seconds):
    """Format uptime seconds into human-readable string"""
    if not seconds or seconds < 0:
        return "Unknown"
    
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    
    return " ".join(parts)

def format_bytes(bytes_value):
    """Format bytes into human-readable string"""
    if not bytes_value or bytes_value < 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(bytes_value)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.2f} {units[unit_index]}"

def calculate_availability(total_checks, successful_checks):
    """Calculate availability percentage"""
    if total_checks == 0:
        return 0.0
    return round((successful_checks / total_checks) * 100, 2)

def is_port_open(host, port, timeout=5):
    """Check if a specific port is open on a host"""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def get_network_info(ip_address):
    """Get network information for an IP address"""
    try:
        ip = ipaddress.ip_address(ip_address)
        return {
            'version': ip.version,
            'is_private': ip.is_private,
            'is_loopback': ip.is_loopback,
            'is_multicast': ip.is_multicast,
            'compressed': ip.compressed,
            'exploded': ip.exploded
        }
    except ValueError:
        return None

def create_pagination_info(page, per_page, total):
    """Create pagination information object"""
    total_pages = (total + per_page - 1) // per_page
    
    return {
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_num': page - 1 if page > 1 else None,
        'next_num': page + 1 if page < total_pages else None
    }

def validate_json_schema(data, required_fields):
    """Validate JSON data against required fields"""
    if not isinstance(data, dict):
        return False, "Data must be a JSON object"
    
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None:
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    return True, "Valid"

def clean_metadata(metadata):
    """Clean and validate metadata object"""
    if not metadata:
        return {}
    
    if isinstance(metadata, str):
        try:
            metadata = json.loads(metadata)
        except json.JSONDecodeError:
            return {}
    
    if not isinstance(metadata, dict):
        return {}
    
    # Remove null values and clean strings
    cleaned = {}
    for key, value in metadata.items():
        if value is not None:
            if isinstance(value, str):
                value = value.strip()
                if value:
                    cleaned[key] = value
            else:
                cleaned[key] = value
    
    return cleaned

def log_activity(user_id, action, resource_type, resource_id, details=None):
    """Log user activity for audit purposes"""
    try:
        from app.models import ActivityLog
        from app import db
        
        log_entry = ActivityLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            timestamp=datetime.utcnow()
        )
        
        db.session.add(log_entry)
        db.session.commit()
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to log activity: {str(e)}")
        return False

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, key, max_requests=100, window_seconds=3600):
        """Check if request is allowed based on rate limit"""
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window_seconds)
        
        # Clean old entries
        if key in self.requests:
            self.requests[key] = [req_time for req_time in self.requests[key] if req_time > window_start]
        else:
            self.requests[key] = []
        
        # Check if under limit
        if len(self.requests[key]) >= max_requests:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True

# Global rate limiter instance
rate_limiter = RateLimiter()
