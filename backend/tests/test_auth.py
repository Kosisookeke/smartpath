"""
Unit tests for authentication functionality
"""
import pytest
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import User


@pytest.fixture
def app():
    """Create and configure a test app instance"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['DATABASE'] = 'database/test_smartpath.db'
    yield app
    
    # Cleanup
    if os.path.exists('database/test_smartpath.db'):
        os.remove('database/test_smartpath.db')


@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()


def test_register_success(client):
    """Test successful user registration"""
    response = client.post('/api/auth/register',
                          data=json.dumps({
                              'email': 'test@example.com',
                              'password': 'password123',
                              'name': 'Test User'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'user' in data
    assert data['user']['email'] == 'test@example.com'


def test_register_missing_fields(client):
    """Test registration with missing fields"""
    response = client.post('/api/auth/register',
                          data=json.dumps({
                              'email': 'test@example.com',
                              'password': 'password123'
                              # missing name
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400


def test_register_invalid_email(client):
    """Test registration with invalid email"""
    response = client.post('/api/auth/register',
                          data=json.dumps({
                              'email': 'invalid-email',
                              'password': 'password123',
                              'name': 'Test User'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400


def test_register_short_password(client):
    """Test registration with short password"""
    response = client.post('/api/auth/register',
                          data=json.dumps({
                              'email': 'test@example.com',
                              'password': '12345',
                              'name': 'Test User'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400


def test_login_success(client):
    """Test successful login"""
    # First register a user
    client.post('/api/auth/register',
               data=json.dumps({
                   'email': 'test@example.com',
                   'password': 'password123',
                   'name': 'Test User'
               }),
               content_type='application/json')
    
    # Then try to login
    response = client.post('/api/auth/login',
                          data=json.dumps({
                              'email': 'test@example.com',
                              'password': 'password123'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'user' in data
    assert data['user']['email'] == 'test@example.com'


def test_login_wrong_password(client):
    """Test login with wrong password"""
    # Register a user
    client.post('/api/auth/register',
               data=json.dumps({
                   'email': 'test@example.com',
                   'password': 'password123',
                   'name': 'Test User'
               }),
               content_type='application/json')
    
    # Try wrong password
    response = client.post('/api/auth/login',
                          data=json.dumps({
                              'email': 'test@example.com',
                              'password': 'wrongpassword'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    """Test login with nonexistent user"""
    response = client.post('/api/auth/login',
                          data=json.dumps({
                              'email': 'nonexistent@example.com',
                              'password': 'password123'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 401

