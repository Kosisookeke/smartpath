"""
SmartPath Learning Platform - Main Application
"""
from flask import Flask, jsonify
from flask_cors import CORS
from app import create_app

# Create Flask app
app = create_app()

# Health check endpoint
@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "ok", 
        "message": "SmartPath API is running",
        "version": "1.0.0"
    })

# Root endpoint
@app.route('/')
def index():
    return jsonify({
        "name": "SmartPath Learning Platform API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "auth": "/api/auth",
            "courses": "/api/courses",
            "quizzes": "/api/quizzes",
            "admin": "/api/admin"
        }
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Starting SmartPath Learning Platform API")
    print("Server running on: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, port=5000, host='0.0.0.0')
