/**
 * Course Detail Page Component
 */
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { courseAPI, quizAPI } from '../services/api';
import QuizCard from '../components/QuizCard';
import './CourseDetail.css';

const CourseDetail = () => {
    const { id } = useParams();
    const [course, setCourse] = useState(null);
    const [quizzes, setQuizzes] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadCourseData();
    }, [id]);

    const loadCourseData = async () => {
        try {
            const [courseData, quizzesData] = await Promise.all([
                courseAPI.getById(id),
                quizAPI.getAll()
            ]);

            setCourse(courseData.course);
            // Filter quizzes for this course
            const courseQuizzes = quizzesData.quizzes.filter(
                q => q.course_id === parseInt(id)
            );
            setQuizzes(courseQuizzes);
        } catch (error) {
            console.error('Error loading course:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <div className="loading">Loading course...</div>;
    }

    if (!course) {
        return <div className="error">Course not found.</div>;
    }

    return (
        <div className="course-detail">
            <div className="course-header">
                <Link to="/courses" className="back-link">← Back to Courses</Link>
                <div className="category-badge">{course.category}</div>
                <h1>{course.title}</h1>
                <p className="course-author">By: {course.author_name}</p>
            </div>

            <div className="course-content">
                <section className="course-description">
                    <h2>About This Course</h2>
                    <p>{course.description}</p>
                </section>

                <section className="course-material">
                    <h2>Course Content</h2>
                    <div className="content-body" dangerouslySetInnerHTML={{ __html: course.content.replace(/\n/g, '<br />') }} />
                </section>

                <section className="course-quizzes">
                    <h2>Practice Quizzes</h2>
                    {quizzes.length > 0 ? (
                        <div className="quizzes-grid">
                            {quizzes.map(quiz => (
                                <QuizCard key={quiz.id} quiz={quiz} />
                            ))}
                        </div>
                    ) : (
                        <p className="empty-message">No quizzes available for this course yet.</p>
                    )}
                </section>
            </div>
        </div>
    );
};

export default CourseDetail;

