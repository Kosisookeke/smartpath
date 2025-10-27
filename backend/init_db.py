"""
Database initialization script for SmartPath
This script creates all necessary tables and seeds initial data
"""
import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime


def init_database():
    """Initialize the database with tables and sample data"""
    
    # Create database directory if it doesn't exist
    os.makedirs('database', exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect('database/smartpath.db')
    cursor = conn.cursor()
    
    print("Creating database tables...")
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'student',
            created_at TEXT NOT NULL
        )
    ''')
    
    # Create courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            content TEXT NOT NULL,
            created_by INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')
    
    # Create quizzes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            course_id INTEGER NOT NULL,
            created_by INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses (id),
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')
    
    # Create quiz_questions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            FOREIGN KEY (quiz_id) REFERENCES quizzes (id) ON DELETE CASCADE
        )
    ''')
    
    # Create quiz_attempts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            quiz_id INTEGER NOT NULL,
            score REAL NOT NULL,
            answers TEXT NOT NULL,
            submitted_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (quiz_id) REFERENCES quizzes (id)
        )
    ''')
    
    conn.commit()
    print("✓ Database tables created successfully")
    
    # Check if sample data already exists
    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]
    
    if user_count == 0:
        print("\nSeeding sample data...")
        
        # Create admin user
        admin_hash = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO users (email, password_hash, name, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin@smartpath.com', admin_hash, 'Admin User', 'admin', datetime.utcnow().isoformat()))
        admin_id = cursor.lastrowid
        
        # Create student user
        student_hash = generate_password_hash('student123')
        cursor.execute('''
            INSERT INTO users (email, password_hash, name, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', ('student@smartpath.com', student_hash, 'Student User', 'student', datetime.utcnow().isoformat()))
        
        print("✓ Created default users:")
        print("  - Admin: admin@smartpath.com / admin123")
        print("  - Student: student@smartpath.com / student123")
        
        # Create sample courses
        courses_data = [
            {
                'title': 'Introduction to Python Programming',
                'description': 'Learn the basics of Python programming language',
                'category': 'Programming',
                'content': '''
# Introduction to Python Programming

## What is Python?
Python is a high-level, interpreted programming language known for its simplicity and readability.

## Why Learn Python?
- Easy to learn and use
- Versatile and powerful
- Large community and extensive libraries
- High demand in job market

## Topics Covered:
1. Variables and Data Types
2. Control Structures (if, while, for)
3. Functions
4. Lists and Dictionaries
5. File Handling
6. Basic Object-Oriented Programming

## Getting Started:
To start programming in Python, you need to install Python from python.org and use any text editor or IDE like VS Code, PyCharm, or IDLE.
                '''
            },
            {
                'title': 'Web Development Fundamentals',
                'description': 'Master HTML, CSS, and JavaScript basics',
                'category': 'Web Development',
                'content': '''
# Web Development Fundamentals

## Overview
Learn to build modern, responsive websites from scratch.

## What You'll Learn:

### HTML (Structure)
- HTML elements and tags
- Forms and input elements
- Semantic HTML
- Accessibility basics

### CSS (Styling)
- Selectors and properties
- Box model
- Flexbox and Grid
- Responsive design
- Animations

### JavaScript (Interactivity)
- Variables and functions
- DOM manipulation
- Events
- Async programming
- Fetch API

## Project:
Build a complete responsive portfolio website.
                '''
            },
            {
                'title': 'Data Structures and Algorithms',
                'description': 'Essential computer science concepts',
                'category': 'Computer Science',
                'content': '''
# Data Structures and Algorithms

## Introduction
Understanding data structures and algorithms is crucial for writing efficient code and solving complex problems.

## Data Structures:
1. **Arrays**: Contiguous memory storage
2. **Linked Lists**: Dynamic memory allocation
3. **Stacks**: LIFO (Last In First Out)
4. **Queues**: FIFO (First In First Out)
5. **Trees**: Hierarchical structures
6. **Graphs**: Network structures
7. **Hash Tables**: Fast key-value lookups

## Algorithms:
1. **Sorting**: Bubble, Merge, Quick Sort
2. **Searching**: Linear, Binary Search
3. **Recursion**: Solving problems by breaking them down
4. **Dynamic Programming**: Optimizing recursive solutions
5. **Greedy Algorithms**: Making locally optimal choices

## Big O Notation:
Learn to analyze time and space complexity of algorithms.
                '''
            }
        ]
        
        course_ids = []
        for course in courses_data:
            cursor.execute('''
                INSERT INTO courses (title, description, category, content, created_by, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (course['title'], course['description'], course['category'], 
                  course['content'], admin_id, datetime.utcnow().isoformat()))
            course_ids.append(cursor.lastrowid)
        
        print(f"✓ Created {len(courses_data)} sample courses")
        
        # Create sample quizzes
        quizzes_data = [
            {
                'title': 'Python Basics Quiz',
                'description': 'Test your knowledge of Python fundamentals',
                'course_id': course_ids[0],
                'questions': [
                    {
                        'text': 'Which of the following is the correct way to declare a variable in Python?',
                        'a': 'int x = 5',
                        'b': 'x = 5',
                        'c': 'var x = 5',
                        'd': 'let x = 5',
                        'correct': 'B'
                    },
                    {
                        'text': 'What is the output of: print(type([]))?',
                        'a': '<class \'list\'>',
                        'b': '<class \'array\'>',
                        'c': '<class \'tuple\'>',
                        'd': '<class \'dict\'>',
                        'correct': 'A'
                    },
                    {
                        'text': 'Which keyword is used to define a function in Python?',
                        'a': 'function',
                        'b': 'def',
                        'c': 'func',
                        'd': 'define',
                        'correct': 'B'
                    },
                    {
                        'text': 'What does the len() function do?',
                        'a': 'Returns the length of an object',
                        'b': 'Converts to lowercase',
                        'c': 'Checks if object is empty',
                        'd': 'Returns type of object',
                        'correct': 'A'
                    },
                    {
                        'text': 'Which operator is used for exponentiation in Python?',
                        'a': '^',
                        'b': '**',
                        'c': 'exp',
                        'd': 'pow',
                        'correct': 'B'
                    }
                ]
            },
            {
                'title': 'HTML & CSS Quiz',
                'description': 'Test your web development knowledge',
                'course_id': course_ids[1],
                'questions': [
                    {
                        'text': 'What does HTML stand for?',
                        'a': 'Hyper Text Markup Language',
                        'b': 'High Tech Modern Language',
                        'c': 'Home Tool Markup Language',
                        'd': 'Hyperlinks and Text Markup Language',
                        'correct': 'A'
                    },
                    {
                        'text': 'Which CSS property is used to change text color?',
                        'a': 'text-color',
                        'b': 'font-color',
                        'c': 'color',
                        'd': 'text-style',
                        'correct': 'C'
                    },
                    {
                        'text': 'What is the correct HTML element for the largest heading?',
                        'a': '<heading>',
                        'b': '<h1>',
                        'c': '<head>',
                        'd': '<h6>',
                        'correct': 'B'
                    },
                    {
                        'text': 'Which property is used in CSS to change the background color?',
                        'a': 'bgcolor',
                        'b': 'background-color',
                        'c': 'bg-color',
                        'd': 'color-background',
                        'correct': 'B'
                    },
                    {
                        'text': 'What is the correct CSS syntax for making all <p> elements bold?',
                        'a': 'p {font-weight: bold;}',
                        'b': '<p style="font-weight:bold;">',
                        'c': 'p {text-size: bold;}',
                        'd': '<p font="bold">',
                        'correct': 'A'
                    }
                ]
            },
            {
                'title': 'Algorithms Quiz',
                'description': 'Test your understanding of algorithms',
                'course_id': course_ids[2],
                'questions': [
                    {
                        'text': 'What is the time complexity of binary search?',
                        'a': 'O(n)',
                        'b': 'O(log n)',
                        'c': 'O(n²)',
                        'd': 'O(1)',
                        'correct': 'B'
                    },
                    {
                        'text': 'Which data structure uses LIFO (Last In First Out)?',
                        'a': 'Queue',
                        'b': 'Array',
                        'c': 'Stack',
                        'd': 'Tree',
                        'correct': 'C'
                    },
                    {
                        'text': 'What is the worst-case time complexity of QuickSort?',
                        'a': 'O(n log n)',
                        'b': 'O(n)',
                        'c': 'O(n²)',
                        'd': 'O(log n)',
                        'correct': 'C'
                    },
                    {
                        'text': 'Which algorithm is commonly used for finding shortest path in graphs?',
                        'a': 'Binary Search',
                        'b': 'Bubble Sort',
                        'c': 'Dijkstra\'s Algorithm',
                        'd': 'Merge Sort',
                        'correct': 'C'
                    },
                    {
                        'text': 'What does BFS stand for?',
                        'a': 'Best First Search',
                        'b': 'Breadth First Search',
                        'c': 'Binary File System',
                        'd': 'Bottom First Search',
                        'correct': 'B'
                    }
                ]
            }
        ]
        
        for quiz in quizzes_data:
            # Create quiz
            cursor.execute('''
                INSERT INTO quizzes (title, description, course_id, created_by, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (quiz['title'], quiz['description'], quiz['course_id'], 
                  admin_id, datetime.utcnow().isoformat()))
            quiz_id = cursor.lastrowid
            
            # Add questions
            for q in quiz['questions']:
                cursor.execute('''
                    INSERT INTO quiz_questions 
                    (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (quiz_id, q['text'], q['a'], q['b'], q['c'], q['d'], q['correct']))
        
        print(f"✓ Created {len(quizzes_data)} sample quizzes with questions")
        
        conn.commit()
        print("\n✅ Database initialization completed successfully!")
    else:
        print("\n✓ Database already contains data. Skipping sample data creation.")
    
    conn.close()


if __name__ == '__main__':
    print("=" * 60)
    print("SmartPath Database Initialization")
    print("=" * 60)
    init_database()
    print("=" * 60)

