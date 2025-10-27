/**
 * Course Card Component
 */
import React from 'react';
import { Link } from 'react-router-dom';
import './Card.css';

const CourseCard = ({ course }) => {
    return (
        <div className="card course-card">
            <div className="card-header">
                <div className="category-badge">{course.category}</div>
            </div>

            <div className="card-body">
                <h3 className="card-title">{course.title}</h3>
                <p className="card-description">{course.description}</p>

                {course.author_name && (
                    <p className="card-meta">By: {course.author_name}</p>
                )}
            </div>

            <div className="card-footer">
                <Link to={`/courses/${course.id}`} className="btn btn-primary">
                    View Course
                </Link>
            </div>
        </div>
    );
};

export default CourseCard;

