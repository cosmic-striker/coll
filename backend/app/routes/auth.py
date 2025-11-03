from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
from datetime import timedelta
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or user.role != 'admin':
            return jsonify({'msg': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def operator_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or user.role not in ['admin', 'operator']:
            return jsonify({'msg': 'Operator or admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'msg': 'No input data provided'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'msg': 'Username and password required'}), 400
        
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return jsonify({'msg': 'Bad username or password'}), 401

        access_token = create_access_token(
            identity=user.id, 
            expires_delta=timedelta(hours=8),
            additional_claims={'role': user.role}
        )
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        })
    except Exception as e:
        return jsonify({'msg': 'Login failed', 'error': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'msg': 'User not found'}), 404
        
        new_token = create_access_token(
            identity=current_user_id,
            expires_delta=timedelta(hours=8),
            additional_claims={'role': user.role}
        )
        return jsonify({'access_token': new_token})
    except Exception as e:
        return jsonify({'msg': 'Token refresh failed', 'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'msg': 'User not found'}), 404
        
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        })
    except Exception as e:
        return jsonify({'msg': 'Failed to get profile', 'error': str(e)}), 500

@auth_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    try:
        users = User.query.all()
        return jsonify([{
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'role': u.role
        } for u in users])
    except Exception as e:
        return jsonify({'msg': 'Failed to list users', 'error': str(e)}), 500

@auth_bp.route('/users', methods=['POST'])
@admin_required
def create_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'msg': 'No input data provided'}), 400
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'viewer')
        if not all([username, email, password]):
            return jsonify({'msg': 'Username, email and password required'}), 400
        if role not in ['admin', 'operator', 'viewer']:
            return jsonify({'msg': 'Invalid role'}), 400
        # Check if user exists
        if User.query.filter_by(username=username).first():
            return jsonify({'msg': 'Username already exists'}), 409
        if User.query.filter_by(email=email).first():
            return jsonify({'msg': 'Email already exists'}), 409
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to create user', 'error': str(e)}), 500

# Update user
@auth_bp.route('/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'msg': 'User not found'}), 404
        data = request.get_json()
        if not data:
            return jsonify({'msg': 'No input data provided'}), 400
        username = data.get('username')
        email = data.get('email')
        role = data.get('role')
        password = data.get('password')
        # Check for username/email uniqueness if changed
        if username and username != user.username:
            if User.query.filter_by(username=username).first():
                return jsonify({'msg': 'Username already exists'}), 409
            user.username = username
        if email and email != user.email:
            if User.query.filter_by(email=email).first():
                return jsonify({'msg': 'Email already exists'}), 409
            user.email = email
        if role:
            if role not in ['admin', 'operator', 'viewer']:
                return jsonify({'msg': 'Invalid role'}), 400
            user.role = role
        if password:
            user.set_password(password)
        db.session.commit()
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to update user', 'error': str(e)}), 500

# Delete user
@auth_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'msg': 'User not found'}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({'msg': 'User deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to delete user', 'error': str(e)}), 500
