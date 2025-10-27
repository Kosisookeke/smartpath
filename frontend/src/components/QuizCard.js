/**
 * Quiz Card Component
 */
import React from 'react';
import { Link } from 'react-router-dom';
import './Card.css';

const QuizCard = ({ quiz }) => {
    return (
        <div className="card quiz-card">
            <div className="card-header">
                <span className="quiz-icon">📝</span>
            </div>

            <div className="card-body">
                <h3 className="card-title">{quiz.title}</h3>
                <p className="card-description">{quiz.description}</p>

                {quiz.course_title && (
                    <p className="card-meta">Course: {quiz.course_title}</p>
                )}
            </div>

            <div className="card-footer">
                <Link to={`/quiz/${quiz.id}`} className="btn btn-secondary">
                    Take Quiz
                </Link>
            </div>
        </div>
    );
};

export default QuizCard;

