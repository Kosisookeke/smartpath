"""
Utility functions for SmartPath
"""
import sqlite3
from flask import current_app, g
from functools import wraps
from flask import jsonify, request


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # For MVP, we'll use a simple session-based auth
        # In production, use JWT tokens
        user_id = request.headers.get('X-User-Id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        g.user_id = int(user_id)
        return f(*args, **kwargs)
    
    return decorated_function


def require_admin(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = request.headers.get('X-User-Id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Check if user is admin
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT role FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if not user or user['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        g.user_id = int(user_id)
        return f(*args, **kwargs)
    
    return decorated_function


def validate_email(email):
    """Simple email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

