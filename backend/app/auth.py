"""
Authentication routes for SmartPath
"""
from flask import Blueprint, request, jsonify, g
from app.models import User
from app.utils import validate_email, require_auth

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate input
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email', '').strip()
    password = data.get('password', '')
    name = data.get('name', '').strip()
    
    # Validation
    if not email or not password or not name:
        return jsonify({'error': 'Email, password, and name are required'}), 400
    
    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Create user
    user_id, error = User.create(email, password, name)
    
    if error:
        return jsonify({'error': error}), 400
    
    # Get user details
    user = User.get_by_id(user_id)
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Authenticate user
    user = User.authenticate(email, password)
    
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    return jsonify({
        'message': 'Login successful',
        'user': user
    }), 200


@auth_bp.route('/user', methods=['GET'])
@require_auth
def get_user():
    """Get current user information"""
    user = User.get_by_id(g.user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user}), 200


@auth_bp.route('/user', methods=['PUT'])
@require_auth
def update_user():
    """Update user information"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    name = data.get('name')
    email = data.get('email')
    
    if email and not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    User.update(g.user_id, name=name, email=email)
    user = User.get_by_id(g.user_id)
    
    return jsonify({
        'message': 'User updated successfully',
        'user': user
    }), 200

