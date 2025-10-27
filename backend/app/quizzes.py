"""
Quiz functionality routes for SmartPath
"""
from flask import Blueprint, request, jsonify, g
from app.models import Quiz
from app.utils import require_auth, require_admin

quizzes_bp = Blueprint('quizzes', __name__)


@quizzes_bp.route('/', methods=['GET'])
def get_quizzes():
    """Get all quizzes"""
    quizzes = Quiz.get_all()
    return jsonify({'quizzes': quizzes}), 200


@quizzes_bp.route('/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Get a specific quiz with questions"""
    quiz = Quiz.get_by_id(quiz_id)
    
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    # Remove correct_answer from questions for non-admin users
    # (Admin check would go here in production)
    user_id = request.headers.get('X-User-Id')
    is_taking_quiz = request.args.get('mode') == 'take'
    
    if is_taking_quiz and 'questions' in quiz:
        for question in quiz['questions']:
            # Don't send correct answer to students taking the quiz
            question.pop('correct_answer', None)
    
    return jsonify({'quiz': quiz}), 200


@quizzes_bp.route('/', methods=['POST'])
@require_admin
def create_quiz():
    """Create a new quiz (admin only)"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    course_id = data.get('course_id')
    questions = data.get('questions', [])
    
    # Validation
    if not title or not description or not course_id:
        return jsonify({'error': 'Title, description, and course_id are required'}), 400
    
    # Create quiz
    quiz_id, error = Quiz.create(title, description, course_id, g.user_id)
    
    if error:
        return jsonify({'error': error}), 400
    
    # Add questions
    for q in questions:
        Quiz.add_question(
            quiz_id,
            q.get('question_text'),
            q.get('option_a'),
            q.get('option_b'),
            q.get('option_c'),
            q.get('option_d'),
            q.get('correct_answer')
        )
    
    quiz = Quiz.get_by_id(quiz_id)
    
    return jsonify({
        'message': 'Quiz created successfully',
        'quiz': quiz
    }), 201


@quizzes_bp.route('/<int:quiz_id>/questions', methods=['POST'])
@require_admin
def add_question(quiz_id):
    """Add a question to a quiz (admin only)"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    question_text = data.get('question_text', '').strip()
    option_a = data.get('option_a', '').strip()
    option_b = data.get('option_b', '').strip()
    option_c = data.get('option_c', '').strip()
    option_d = data.get('option_d', '').strip()
    correct_answer = data.get('correct_answer', '').strip()
    
    # Validation
    if not all([question_text, option_a, option_b, option_c, option_d, correct_answer]):
        return jsonify({'error': 'All fields are required'}), 400
    
    if correct_answer not in ['A', 'B', 'C', 'D']:
        return jsonify({'error': 'Correct answer must be A, B, C, or D'}), 400
    
    question_id, error = Quiz.add_question(
        quiz_id, question_text, option_a, option_b, option_c, option_d, correct_answer
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': 'Question added successfully',
        'question_id': question_id
    }), 201


@quizzes_bp.route('/<int:quiz_id>/submit', methods=['POST'])
@require_auth
def submit_quiz(quiz_id):
    """Submit quiz answers and get results"""
    data = request.get_json()
    
    if not data or 'answers' not in data:
        return jsonify({'error': 'Answers are required'}), 400
    
    answers = data['answers']
    
    # Submit attempt and calculate score
    result = Quiz.submit_attempt(g.user_id, quiz_id, answers)
    
    return jsonify({
        'message': 'Quiz submitted successfully',
        'result': result
    }), 200


@quizzes_bp.route('/<int:quiz_id>/results', methods=['GET'])
@require_auth
def get_quiz_results(quiz_id):
    """Get user's quiz attempts and results"""
    attempts = Quiz.get_user_attempts(g.user_id, quiz_id)
    
    return jsonify({
        'quiz_id': quiz_id,
        'attempts': attempts
    }), 200


@quizzes_bp.route('/my-attempts', methods=['GET'])
@require_auth
def get_my_attempts():
    """Get all quiz attempts for current user"""
    attempts = Quiz.get_user_attempts(g.user_id)
    
    return jsonify({'attempts': attempts}), 200

