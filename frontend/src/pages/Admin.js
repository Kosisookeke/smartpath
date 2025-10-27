/**
 * Admin Panel Page Component
 */
import React, { useState, useEffect } from 'react';
import { adminAPI, courseAPI, quizAPI } from '../services/api';
import './Admin.css';

const Admin = () => {
    const [stats, setStats] = useState(null);
    const [users, setUsers] = useState([]);
    const [activeTab, setActiveTab] = useState('overview');
    const [loading, setLoading] = useState(true);

    // Course form state
    const [courseForm, setCourseForm] = useState({
        title: '',
        description: '',
        category: '',
        content: ''
    });

    // Quiz form state
    const [quizForm, setQuizForm] = useState({
        title: '',
        description: '',
        course_id: '',
        questions: []
    });

    useEffect(() => {
        loadAdminData();
    }, []);

    const loadAdminData = async () => {
        try {
            const [statsData, usersData] = await Promise.all([
                adminAPI.getStats(),
                adminAPI.getUsers()
            ]);

            setStats(statsData.stats);
            setUsers(usersData.users);
        } catch (error) {
            console.error('Error loading admin data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleCreateCourse = async (e) => {
        e.preventDefault();
        try {
            await courseAPI.create(courseForm);
            alert('Course created successfully!');
            setCourseForm({ title: '', description: '', category: '', content: '' });
        } catch (error) {
            alert('Error creating course: ' + error.message);
        }
    };

    const handleQuizFormChange = (e) => {
        setQuizForm({ ...quizForm, [e.target.name]: e.target.value });
    };

    const addQuestion = () => {
        setQuizForm({
            ...quizForm,
            questions: [
                ...quizForm.questions,
                {
                    question_text: '',
                    option_a: '',
                    option_b: '',
                    option_c: '',
                    option_d: '',
                    correct_answer: 'A'
                }
            ]
        });
    };

    const updateQuestion = (index, field, value) => {
        const newQuestions = [...quizForm.questions];
        newQuestions[index][field] = value;
        setQuizForm({ ...quizForm, questions: newQuestions });
    };

    const removeQuestion = (index) => {
        const newQuestions = quizForm.questions.filter((_, i) => i !== index);
        setQuizForm({ ...quizForm, questions: newQuestions });
    };

    const handleCreateQuiz = async (e) => {
        e.preventDefault();
        if (quizForm.questions.length === 0) {
            alert('Please add at least one question');
            return;
        }
        try {
            await quizAPI.create(quizForm);
            alert('Quiz created successfully!');
            setQuizForm({ title: '', description: '', course_id: '', questions: [] });
        } catch (error) {
            alert('Error creating quiz: ' + error.message);
        }
    };

    if (loading) {
        return <div className="loading">Loading admin panel...</div>;
    }

    return (
        <div className="admin-page">
            <h1>Admin Panel</h1>

            <div className="admin-tabs">
                <button
                    className={activeTab === 'overview' ? 'active' : ''}
                    onClick={() => setActiveTab('overview')}
                >
                    Overview
                </button>
                <button
                    className={activeTab === 'courses' ? 'active' : ''}
                    onClick={() => setActiveTab('courses')}
                >
                    Create Course
                </button>
                <button
                    className={activeTab === 'quizzes' ? 'active' : ''}
                    onClick={() => setActiveTab('quizzes')}
                >
                    Create Quiz
                </button>
                <button
                    className={activeTab === 'users' ? 'active' : ''}
                    onClick={() => setActiveTab('users')}
                >
                    Users
                </button>
            </div>

            {activeTab === 'overview' && stats && (
                <div className="admin-content">
                    <div className="stats-grid">
                        <div className="stat-box">
                            <h3>{stats.total_users}</h3>
                            <p>Total Users</p>
                        </div>
                        <div className="stat-box">
                            <h3>{stats.total_courses}</h3>
                            <p>Total Courses</p>
                        </div>
                        <div className="stat-box">
                            <h3>{stats.total_quizzes}</h3>
                            <p>Total Quizzes</p>
                        </div>
                        <div className="stat-box">
                            <h3>{stats.total_quiz_attempts}</h3>
                            <p>Quiz Attempts</p>
                        </div>
                        <div className="stat-box">
                            <h3>{stats.average_quiz_score}%</h3>
                            <p>Avg Quiz Score</p>
                        </div>
                    </div>
                </div>
            )}

            {activeTab === 'courses' && (
                <div className="admin-content">
                    <h2>Create New Course</h2>
                    <form onSubmit={handleCreateCourse} className="admin-form">
                        <div className="form-group">
                            <label>Course Title</label>
                            <input
                                type="text"
                                value={courseForm.title}
                                onChange={(e) => setCourseForm({ ...courseForm, title: e.target.value })}
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>Category</label>
                            <input
                                type="text"
                                value={courseForm.category}
                                onChange={(e) => setCourseForm({ ...courseForm, category: e.target.value })}
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>Description</label>
                            <textarea
                                value={courseForm.description}
                                onChange={(e) => setCourseForm({ ...courseForm, description: e.target.value })}
                                required
                                rows="3"
                            />
                        </div>

                        <div className="form-group">
                            <label>Course Content</label>
                            <textarea
                                value={courseForm.content}
                                onChange={(e) => setCourseForm({ ...courseForm, content: e.target.value })}
                                required
                                rows="10"
                            />
                        </div>

                        <button type="submit" className="btn btn-primary">Create Course</button>
                    </form>
                </div>
            )}

            {activeTab === 'quizzes' && (
                <div className="admin-content">
                    <h2>Create New Quiz</h2>
                    <form onSubmit={handleCreateQuiz} className="admin-form">
                        <div className="form-group">
                            <label>Quiz Title</label>
                            <input
                                type="text"
                                name="title"
                                value={quizForm.title}
                                onChange={handleQuizFormChange}
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>Description</label>
                            <textarea
                                name="description"
                                value={quizForm.description}
                                onChange={handleQuizFormChange}
                                required
                                rows="2"
                            />
                        </div>

                        <div className="form-group">
                            <label>Course ID</label>
                            <input
                                type="number"
                                name="course_id"
                                value={quizForm.course_id}
                                onChange={handleQuizFormChange}
                                required
                            />
                        </div>

                        <div className="questions-section">
                            <h3>Questions</h3>
                            {quizForm.questions.map((q, index) => (
                                <div key={index} className="question-form">
                                    <h4>Question {index + 1}</h4>
                                    <input
                                        type="text"
                                        placeholder="Question text"
                                        value={q.question_text}
                                        onChange={(e) => updateQuestion(index, 'question_text', e.target.value)}
                                        required
                                    />
                                    <input
                                        type="text"
                                        placeholder="Option A"
                                        value={q.option_a}
                                        onChange={(e) => updateQuestion(index, 'option_a', e.target.value)}
                                        required
                                    />
                                    <input
                                        type="text"
                                        placeholder="Option B"
                                        value={q.option_b}
                                        onChange={(e) => updateQuestion(index, 'option_b', e.target.value)}
                                        required
                                    />
                                    <input
                                        type="text"
                                        placeholder="Option C"
                                        value={q.option_c}
                                        onChange={(e) => updateQuestion(index, 'option_c', e.target.value)}
                                        required
                                    />
                                    <input
                                        type="text"
                                        placeholder="Option D"
                                        value={q.option_d}
                                        onChange={(e) => updateQuestion(index, 'option_d', e.target.value)}
                                        required
                                    />
                                    <select
                                        value={q.correct_answer}
                                        onChange={(e) => updateQuestion(index, 'correct_answer', e.target.value)}
                                        required
                                    >
                                        <option value="A">A</option>
                                        <option value="B">B</option>
                                        <option value="C">C</option>
                                        <option value="D">D</option>
                                    </select>
                                    <button type="button" onClick={() => removeQuestion(index)} className="btn-remove">
                                        Remove
                                    </button>
                                </div>
                            ))}
                            <button type="button" onClick={addQuestion} className="btn btn-secondary">
                                Add Question
                            </button>
                        </div>

                        <button type="submit" className="btn btn-primary">Create Quiz</button>
                    </form>
                </div>
            )}

            {activeTab === 'users' && (
                <div className="admin-content">
                    <h2>User Management</h2>
                    <div className="users-table">
                        <table>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Role</th>
                                    <th>Joined</th>
                                </tr>
                            </thead>
                            <tbody>
                                {users.map(user => (
                                    <tr key={user.id}>
                                        <td>{user.id}</td>
                                        <td>{user.name}</td>
                                        <td>{user.email}</td>
                                        <td>
                                            <span className={`role-badge ${user.role}`}>{user.role}</span>
                                        </td>
                                        <td>{new Date(user.created_at).toLocaleDateString()}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Admin;

