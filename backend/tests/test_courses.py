"""
Unit tests for course functionality
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
def admin_user(client):
    """Create an admin user and return their ID"""
    response = client.post('/api/auth/register',
                          data=json.dumps({
                              'email': 'admin@test.com',
                              'password': 'admin123',
                              'name': 'Admin User'
                          }),
                          content_type='application/json')
    
    data = json.loads(response.data)
    user_id = data['user']['id']
    
    # Make user admin (direct database modification for testing)
    with app.app_context():
        from app.utils import get_db_connection
        conn = get_db_connection()
        conn.execute('UPDATE users SET role = ? WHERE id = ?', ('admin', user_id))
        conn.commit()
        conn.close()
    
    return user_id


def test_get_courses_empty(client):
    """Test getting courses when none exist"""
    response = client.get('/api/courses/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'courses' in data
    assert len(data['courses']) == 0


def test_create_course_success(client, admin_user):
    """Test creating a course as admin"""
    response = client.post('/api/courses/',
                          data=json.dumps({
                              'title': 'Test Course',
                              'description': 'Test Description',
                              'category': 'Test Category',
                              'content': 'Test Content'
                          }),
                          content_type='application/json',
                          headers={'X-User-Id': str(admin_user)})
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'course' in data
    assert data['course']['title'] == 'Test Course'


def test_create_course_unauthorized(client):
    """Test creating a course without admin privileges"""
    response = client.post('/api/courses/',
                          data=json.dumps({
                              'title': 'Test Course',
                              'description': 'Test Description',
                              'category': 'Test Category',
                              'content': 'Test Content'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 401


def test_get_course_by_id(client, admin_user):
    """Test getting a specific course"""
    # Create a course
    create_response = client.post('/api/courses/',
                                 data=json.dumps({
                                     'title': 'Test Course',
                                     'description': 'Test Description',
                                     'category': 'Test Category',
                                     'content': 'Test Content'
                                 }),
                                 content_type='application/json',
                                 headers={'X-User-Id': str(admin_user)})
    
    course_id = json.loads(create_response.data)['course']['id']
    
    # Get the course
    response = client.get(f'/api/courses/{course_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['course']['title'] == 'Test Course'


def test_get_nonexistent_course(client):
    """Test getting a course that doesn't exist"""
    response = client.get('/api/courses/999')
    assert response.status_code == 404


def test_update_course(client, admin_user):
    """Test updating a course"""
    # Create a course
    create_response = client.post('/api/courses/',
                                 data=json.dumps({
                                     'title': 'Original Title',
                                     'description': 'Original Description',
                                     'category': 'Original Category',
                                     'content': 'Original Content'
                                 }),
                                 content_type='application/json',
                                 headers={'X-User-Id': str(admin_user)})
    
    course_id = json.loads(create_response.data)['course']['id']
    
    # Update the course
    response = client.put(f'/api/courses/{course_id}',
                         data=json.dumps({
                             'title': 'Updated Title'
                         }),
                         content_type='application/json',
                         headers={'X-User-Id': str(admin_user)})
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['course']['title'] == 'Updated Title'


def test_delete_course(client, admin_user):
    """Test deleting a course"""
    # Create a course
    create_response = client.post('/api/courses/',
                                 data=json.dumps({
                                     'title': 'Test Course',
                                     'description': 'Test Description',
                                     'category': 'Test Category',
                                     'content': 'Test Content'
                                 }),
                                 content_type='application/json',
                                 headers={'X-User-Id': str(admin_user)})
    
    course_id = json.loads(create_response.data)['course']['id']
    
    # Delete the course
    response = client.delete(f'/api/courses/{course_id}',
                            headers={'X-User-Id': str(admin_user)})
    
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f'/api/courses/{course_id}')
    assert get_response.status_code == 404

