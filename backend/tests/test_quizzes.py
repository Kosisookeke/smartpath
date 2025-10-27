"""
Unit tests for quiz functionality
"""
import pytest
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app


@pytest.fixture
def app():
    """Create and configure a test app instance"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['DATABASE'] = 'database/test_smartpath.db'
    yield app
    
    if os.path.exists('database/test_smartpath.db'):
        os.remove('database/test_smartpath.db')


@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()


@pytest.fixture
def setup_data(client, app):
    """Create test data"""
    # Create admin user
    response = client.post('/api/auth/register',
                          data=json.dumps({
                              'email': 'admin@test.com',
                              'password': 'admin123',
                              'name': 'Admin User'
                          }),
                          content_type='application/json')
    
    admin_id = json.loads(response.data)['user']['id']
    
    # Make user admin
    with app.app_context():
        from app.utils import get_db_connection
        conn = get_db_connection()
        conn.execute('UPDATE users SET role = ? WHERE id = ?', ('admin', admin_id))
        conn.commit()
        conn.close()
    
    # Create a course
    course_response = client.post('/api/courses/',
                                 data=json.dumps({
                                     'title': 'Test Course',
                                     'description': 'Test Description',
                                     'category': 'Test',
                                     'content': 'Content'
                                 }),
                                 content_type='application/json',
                                 headers={'X-User-Id': str(admin_id)})
    
    course_id = json.loads(course_response.data)['course']['id']
    
    # Create student user
    student_response = client.post('/api/auth/register',
                                  data=json.dumps({
                                      'email': 'student@test.com',
                                      'password': 'student123',
                                      'name': 'Student User'
                                  }),
                                  content_type='application/json')
    
    student_id = json.loads(student_response.data)['user']['id']
    
    return {
        'admin_id': admin_id,
        'student_id': student_id,
        'course_id': course_id
    }


def test_create_quiz(client, setup_data):
    """Test creating a quiz"""
    response = client.post('/api/quizzes/',
                          data=json.dumps({
                              'title': 'Test Quiz',
                              'description': 'Test Description',
                              'course_id': setup_data['course_id'],
                              'questions': [
                                  {
                                      'question_text': 'What is 2+2?',
                                      'option_a': '3',
                                      'option_b': '4',
                                      'option_c': '5',
                                      'option_d': '6',
                                      'correct_answer': 'B'
                                  }
                              ]
                          }),
                          content_type='application/json',
                          headers={'X-User-Id': str(setup_data['admin_id'])})
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'quiz' in data
    assert data['quiz']['title'] == 'Test Quiz'
    assert len(data['quiz']['questions']) == 1


def test_get_quiz(client, setup_data):
    """Test getting a quiz"""
    # Create quiz
    create_response = client.post('/api/quizzes/',
                                 data=json.dumps({
                                     'title': 'Test Quiz',
                                     'description': 'Test Description',
                                     'course_id': setup_data['course_id'],
                                     'questions': []
                                 }),
                                 content_type='application/json',
                                 headers={'X-User-Id': str(setup_data['admin_id'])})
    
    quiz_id = json.loads(create_response.data)['quiz']['id']
    
    # Get quiz
    response = client.get(f'/api/quizzes/{quiz_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['quiz']['title'] == 'Test Quiz'


def test_submit_quiz(client, setup_data):
    """Test submitting quiz answers"""
    # Create quiz with questions
    create_response = client.post('/api/quizzes/',
                                 data=json.dumps({
                                     'title': 'Test Quiz',
                                     'description': 'Test Description',
                                     'course_id': setup_data['course_id'],
                                     'questions': [
                                         {
                                             'question_text': 'What is 2+2?',
                                             'option_a': '3',
                                             'option_b': '4',
                                             'option_c': '5',
                                             'option_d': '6',
                                             'correct_answer': 'B'
                                         },
                                         {
                                             'question_text': 'What is 3+3?',
                                             'option_a': '5',
                                             'option_b': '6',
                                             'option_c': '7',
                                             'option_d': '8',
                                             'correct_answer': 'B'
                                         }
                                     ]
                                 }),
                                 content_type='application/json',
                                 headers={'X-User-Id': str(setup_data['admin_id'])})
    
    quiz_data = json.loads(create_response.data)['quiz']
    quiz_id = quiz_data['id']
    question_ids = [str(q['id']) for q in quiz_data['questions']]
    
    # Submit answers (1 correct, 1 incorrect)
    response = client.post(f'/api/quizzes/{quiz_id}/submit',
                          data=json.dumps({
                              'answers': {
                                  question_ids[0]: 'B',  # correct
                                  question_ids[1]: 'A'   # incorrect
                              }
                          }),
                          content_type='application/json',
                          headers={'X-User-Id': str(setup_data['student_id'])})
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'result' in data
    assert data['result']['correct'] == 1
    assert data['result']['total'] == 2
    assert data['result']['score'] == 50.0


def test_get_quiz_results(client, setup_data):
    """Test getting quiz results"""
    # Create and submit quiz
    create_response = client.post('/api/quizzes/',
                                 data=json.dumps({
                                     'title': 'Test Quiz',
                                     'description': 'Test Description',
                                     'course_id': setup_data['course_id'],
                                     'questions': [
                                         {
                                             'question_text': 'What is 2+2?',
                                             'option_a': '3',
                                             'option_b': '4',
                                             'option_c': '5',
                                             'option_d': '6',
                                             'correct_answer': 'B'
                                         }
                                     ]
                                 }),
                                 content_type='application/json',
                                 headers={'X-User-Id': str(setup_data['admin_id'])})
    
    quiz_data = json.loads(create_response.data)['quiz']
    quiz_id = quiz_data['id']
    question_id = str(quiz_data['questions'][0]['id'])
    
    # Submit quiz
    client.post(f'/api/quizzes/{quiz_id}/submit',
               data=json.dumps({
                   'answers': {question_id: 'B'}
               }),
               content_type='application/json',
               headers={'X-User-Id': str(setup_data['student_id'])})
    
    # Get results
    response = client.get(f'/api/quizzes/{quiz_id}/results',
                         headers={'X-User-Id': str(setup_data['student_id'])})
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'attempts' in data
    assert len(data['attempts']) > 0

