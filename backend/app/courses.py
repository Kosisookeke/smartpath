"""
Course management routes for SmartPath
"""
from flask import Blueprint, request, jsonify, g
from app.models import Course
from app.utils import require_auth, require_admin

courses_bp = Blueprint('courses', __name__)


@courses_bp.route('/', methods=['GET'])
def get_courses():
    """Get all courses"""
    courses = Course.get_all()
    return jsonify({'courses': courses}), 200


@courses_bp.route('/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """Get a specific course"""
    course = Course.get_by_id(course_id)
    
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    return jsonify({'course': course}), 200


@courses_bp.route('/', methods=['POST'])
@require_admin
def create_course():
    """Create a new course (admin only)"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    category = data.get('category', '').strip()
    content = data.get('content', '').strip()
    
    # Validation
    if not title or not description or not category or not content:
        return jsonify({'error': 'Title, description, category, and content are required'}), 400
    
    # Create course
    course_id, error = Course.create(title, description, category, content, g.user_id)
    
    if error:
        return jsonify({'error': error}), 400
    
    course = Course.get_by_id(course_id)
    
    return jsonify({
        'message': 'Course created successfully',
        'course': course
    }), 201


@courses_bp.route('/<int:course_id>', methods=['PUT'])
@require_admin
def update_course(course_id):
    """Update a course (admin only)"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Check if course exists
    course = Course.get_by_id(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    title = data.get('title')
    description = data.get('description')
    category = data.get('category')
    content = data.get('content')
    
    Course.update(course_id, title=title, description=description, 
                  category=category, content=content)
    
    course = Course.get_by_id(course_id)
    
    return jsonify({
        'message': 'Course updated successfully',
        'course': course
    }), 200


@courses_bp.route('/<int:course_id>', methods=['DELETE'])
@require_admin
def delete_course(course_id):
    """Delete a course (admin only)"""
    # Check if course exists
    course = Course.get_by_id(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    Course.delete(course_id)
    
    return jsonify({'message': 'Course deleted successfully'}), 200

