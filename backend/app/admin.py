"""
Admin panel routes for SmartPath
"""
from flask import Blueprint, request, jsonify, g
from app.models import User, Course, Quiz
from app.utils import require_admin, get_db_connection

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/stats', methods=['GET'])
@require_admin
def get_stats():
    """Get platform statistics (admin only)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get counts
    cursor.execute('SELECT COUNT(*) as count FROM users')
    total_users = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM users WHERE role = "student"')
    total_students = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM courses')
    total_courses = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM quizzes')
    total_quizzes = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM quiz_attempts')
    total_attempts = cursor.fetchone()['count']
    
    cursor.execute('SELECT AVG(score) as avg_score FROM quiz_attempts')
    avg_score_row = cursor.fetchone()
    avg_score = round(avg_score_row['avg_score'], 2) if avg_score_row['avg_score'] else 0
    
    conn.close()
    
    return jsonify({
        'stats': {
            'total_users': total_users,
            'total_students': total_students,
            'total_courses': total_courses,
            'total_quizzes': total_quizzes,
            'total_quiz_attempts': total_attempts,
            'average_quiz_score': avg_score
        }
    }), 200


@admin_bp.route('/users', methods=['GET'])
@require_admin
def get_users():
    """Get all users (admin only)"""
    users = User.get_all()
    return jsonify({'users': users}), 200


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@require_admin
def update_user_role(user_id):
    """Update user role (admin only)"""
    data = request.get_json()
    
    if not data or 'role' not in data:
        return jsonify({'error': 'Role is required'}), 400
    
    role = data['role']
    
    if role not in ['student', 'admin']:
        return jsonify({'error': 'Role must be either "student" or "admin"'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET role = ? WHERE id = ?', (role, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User role updated successfully'}), 200


@admin_bp.route('/recent-activity', methods=['GET'])
@require_admin
def get_recent_activity():
    """Get recent platform activity (admin only)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get recent quiz attempts
    cursor.execute('''
        SELECT qa.*, u.name as user_name, q.title as quiz_title
        FROM quiz_attempts qa
        LEFT JOIN users u ON qa.user_id = u.id
        LEFT JOIN quizzes q ON qa.quiz_id = q.id
        ORDER BY qa.submitted_at DESC
        LIMIT 10
    ''')
    recent_attempts = [dict(row) for row in cursor.fetchall()]
    
    # Get recently created courses
    cursor.execute('''
        SELECT c.*, u.name as author_name
        FROM courses c
        LEFT JOIN users u ON c.created_by = u.id
        ORDER BY c.created_at DESC
        LIMIT 5
    ''')
    recent_courses = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'recent_attempts': recent_attempts,
        'recent_courses': recent_courses
    }), 200

