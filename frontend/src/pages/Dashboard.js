/**
 * Dashboard Page Component
 */
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { courseAPI, quizAPI } from '../services/api';
import CourseCard from '../components/CourseCard';
import './Dashboard.css';

const Dashboard = () => {
    const { user } = useAuth();
    const [courses, setCourses] = useState([]);
    const [attempts, setAttempts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadDashboardData();
    }, []);

    const loadDashboardData = async () => {
        try {
            const [coursesData, attemptsData] = await Promise.all([
                courseAPI.getAll(),
                quizAPI.getMyAttempts()
            ]);

            setCourses(coursesData.courses || []);
            setAttempts(attemptsData.attempts || []);
        } catch (error) {
            console.error('Error loading dashboard:', error);
        } finally {
            setLoading(false);
        }
    };

    const calculateAverageScore = () => {
        if (attempts.length === 0) return 0;
        const total = attempts.reduce((sum, attempt) => sum + attempt.score, 0);
        return (total / attempts.length).toFixed(1);
    };

    if (loading) {
        return <div className="loading">Loading dashboard...</div>;
    }

    return (
        <div className="dashboard">
            <div className="dashboard-header">
                <h1>Welcome back, {user.name}!</h1>
                <p>Continue your learning journey</p>
            </div>

            <div className="dashboard-stats">
                <div className="stat-card">
                    <h3>{courses.length}</h3>
                    <p>Available Courses</p>
                </div>
                <div className="stat-card">
                    <h3>{attempts.length}</h3>
                    <p>Quizzes Taken</p>
                </div>
                <div className="stat-card">
                    <h3>{calculateAverageScore()}%</h3>
                    <p>Average Score</p>
                </div>
            </div>

            <section className="dashboard-section">
                <div className="section-header">
                    <h2>Recent Courses</h2>
                    <Link to="/courses" className="view-all-link">View All →</Link>
                </div>
                <div className="courses-grid">
                    {courses.slice(0, 3).map(course => (
                        <CourseCard key={course.id} course={course} />
                    ))}
                </div>
                {courses.length === 0 && (
                    <p className="empty-message">No courses available yet.</p>
                )}
            </section>

            <section className="dashboard-section">
                <h2>Recent Quiz Attempts</h2>
                <div className="attempts-list">
                    {attempts.slice(0, 5).map(attempt => (
                        <div key={attempt.id} className="attempt-item">
                            <div className="attempt-info">
                                <h4>{attempt.quiz_title}</h4>
                                <p className="attempt-date">
                                    {new Date(attempt.submitted_at).toLocaleDateString()}
                                </p>
                            </div>
                            <div className={`attempt-score ${attempt.score >= 70 ? 'pass' : 'fail'}`}>
                                {attempt.score.toFixed(0)}%
                            </div>
                        </div>
                    ))}
                </div>
                {attempts.length === 0 && (
                    <p className="empty-message">You haven't taken any quizzes yet.</p>
                )}
            </section>
        </div>
    );
};

export default Dashboard;

