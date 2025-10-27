"""
Database models for SmartPath Learning Platform
"""
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils import get_db_connection


class User:
    """User model for authentication and profile management"""
    
    @staticmethod
    def create(email, password, name, role='student'):
        """Create a new user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            return None, "Email already registered"
        
        # Hash password and create user
        password_hash = generate_password_hash(password)
        
        try:
            cursor.execute(
                '''INSERT INTO users (email, password_hash, name, role, created_at)
                   VALUES (?, ?, ?, ?, ?)''',
                (email, password_hash, name, role, datetime.utcnow().isoformat())
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id, None
        except Exception as e:
            conn.close()
            return None, str(e)
    
    @staticmethod
    def authenticate(email, password):
        """Authenticate user with email and password"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            return {
                'id': user['id'],
                'email': user['email'],
                'name': user['name'],
                'role': user['role']
            }
        return None
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user['id'],
                'email': user['email'],
                'name': user['name'],
                'role': user['role'],
                'created_at': user['created_at']
            }
        return None
    
    @staticmethod
    def update(user_id, name=None, email=None):
        """Update user information"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if name:
            cursor.execute('UPDATE users SET name = ? WHERE id = ?', (name, user_id))
        if email:
            cursor.execute('UPDATE users SET email = ? WHERE id = ?', (email, user_id))
        
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def get_all():
        """Get all users (admin only)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, email, name, role, created_at FROM users')
        users = cursor.fetchall()
        conn.close()
        
        return [dict(user) for user in users]


class Course:
    """Course model for learning modules"""
    
    @staticmethod
    def create(title, description, category, content, created_by):
        """Create a new course"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                '''INSERT INTO courses (title, description, category, content, created_by, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (title, description, category, content, created_by, datetime.utcnow().isoformat())
            )
            conn.commit()
            course_id = cursor.lastrowid
            conn.close()
            return course_id, None
        except Exception as e:
            conn.close()
            return None, str(e)
    
    @staticmethod
    def get_all():
        """Get all courses"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.*, u.name as author_name 
            FROM courses c
            LEFT JOIN users u ON c.created_by = u.id
            ORDER BY c.created_at DESC
        ''')
        courses = cursor.fetchall()
        conn.close()
        
        return [dict(course) for course in courses]
    
    @staticmethod
    def get_by_id(course_id):
        """Get course by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.*, u.name as author_name 
            FROM courses c
            LEFT JOIN users u ON c.created_by = u.id
            WHERE c.id = ?
        ''', (course_id,))
        course = cursor.fetchone()
        conn.close()
        
        return dict(course) if course else None
    
    @staticmethod
    def update(course_id, title=None, description=None, category=None, content=None):
        """Update a course"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if title:
            updates.append('title = ?')
            params.append(title)
        if description:
            updates.append('description = ?')
            params.append(description)
        if category:
            updates.append('category = ?')
            params.append(category)
        if content:
            updates.append('content = ?')
            params.append(content)
        
        if updates:
            params.append(course_id)
            query = f"UPDATE courses SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
        return True
    
    @staticmethod
    def delete(course_id):
        """Delete a course"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM courses WHERE id = ?', (course_id,))
        conn.commit()
        conn.close()
        return True


class Quiz:
    """Quiz model for assessments"""
    
    @staticmethod
    def create(title, description, course_id, created_by):
        """Create a new quiz"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                '''INSERT INTO quizzes (title, description, course_id, created_by, created_at)
                   VALUES (?, ?, ?, ?, ?)''',
                (title, description, course_id, created_by, datetime.utcnow().isoformat())
            )
            conn.commit()
            quiz_id = cursor.lastrowid
            conn.close()
            return quiz_id, None
        except Exception as e:
            conn.close()
            return None, str(e)
    
    @staticmethod
    def get_all():
        """Get all quizzes"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT q.*, c.title as course_title
            FROM quizzes q
            LEFT JOIN courses c ON q.course_id = c.id
            ORDER BY q.created_at DESC
        ''')
        quizzes = cursor.fetchall()
        conn.close()
        
        return [dict(quiz) for quiz in quizzes]
    
    @staticmethod
    def get_by_id(quiz_id):
        """Get quiz by ID with questions"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT q.*, c.title as course_title
            FROM quizzes q
            LEFT JOIN courses c ON q.course_id = c.id
            WHERE q.id = ?
        ''', (quiz_id,))
        quiz = cursor.fetchone()
        
        if quiz:
            quiz = dict(quiz)
            # Get questions
            cursor.execute('''
                SELECT id, question_text, option_a, option_b, option_c, option_d, correct_answer
                FROM quiz_questions
                WHERE quiz_id = ?
            ''', (quiz_id,))
            quiz['questions'] = [dict(q) for q in cursor.fetchall()]
        
        conn.close()
        return quiz
    
    @staticmethod
    def add_question(quiz_id, question_text, option_a, option_b, option_c, option_d, correct_answer):
        """Add a question to a quiz"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                '''INSERT INTO quiz_questions 
                   (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_answer)
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_answer)
            )
            conn.commit()
            question_id = cursor.lastrowid
            conn.close()
            return question_id, None
        except Exception as e:
            conn.close()
            return None, str(e)
    
    @staticmethod
    def submit_attempt(user_id, quiz_id, answers):
        """Submit a quiz attempt and calculate score"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get correct answers
        cursor.execute('SELECT id, correct_answer FROM quiz_questions WHERE quiz_id = ?', (quiz_id,))
        questions = cursor.fetchall()
        
        # Calculate score
        correct = 0
        total = len(questions)
        
        for question in questions:
            question_id = str(question['id'])
            if question_id in answers and answers[question_id] == question['correct_answer']:
                correct += 1
        
        score = (correct / total * 100) if total > 0 else 0
        
        # Save attempt
        cursor.execute(
            '''INSERT INTO quiz_attempts (user_id, quiz_id, score, answers, submitted_at)
               VALUES (?, ?, ?, ?, ?)''',
            (user_id, quiz_id, score, str(answers), datetime.utcnow().isoformat())
        )
        conn.commit()
        attempt_id = cursor.lastrowid
        conn.close()
        
        return {
            'attempt_id': attempt_id,
            'score': score,
            'correct': correct,
            'total': total
        }
    
    @staticmethod
    def get_user_attempts(user_id, quiz_id=None):
        """Get user's quiz attempts"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if quiz_id:
            cursor.execute('''
                SELECT qa.*, q.title as quiz_title
                FROM quiz_attempts qa
                LEFT JOIN quizzes q ON qa.quiz_id = q.id
                WHERE qa.user_id = ? AND qa.quiz_id = ?
                ORDER BY qa.submitted_at DESC
            ''', (user_id, quiz_id))
        else:
            cursor.execute('''
                SELECT qa.*, q.title as quiz_title
                FROM quiz_attempts qa
                LEFT JOIN quizzes q ON qa.quiz_id = q.id
                WHERE qa.user_id = ?
                ORDER BY qa.submitted_at DESC
            ''', (user_id,))
        
        attempts = cursor.fetchall()
        conn.close()
        
        return [dict(attempt) for attempt in attempts]

