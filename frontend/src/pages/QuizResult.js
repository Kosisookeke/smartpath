/**
 * Quiz Result Page Component
 */
import React from 'react';
import { useLocation, Link, useParams } from 'react-router-dom';
import './QuizResult.css';

const QuizResult = () => {
    const location = useLocation();
    const { id } = useParams();
    const result = location.state?.result;

    if (!result) {
        return (
            <div className="quiz-result">
                <div className="error">No result data available.</div>
                <Link to="/dashboard" className="btn btn-primary">Go to Dashboard</Link>
            </div>
        );
    }

    const percentage = result.score;
    const passed = percentage >= 70;

    return (
        <div className="quiz-result">
            <div className="result-card">
                <div className={`result-icon ${passed ? 'pass' : 'fail'}`}>
                    {passed ? '🎉' : '📚'}
                </div>

                <h1>{passed ? 'Congratulations!' : 'Keep Learning!'}</h1>

                <div className="score-circle">
                    <div className="score-value">{percentage.toFixed(0)}%</div>
                    <div className="score-label">Your Score</div>
                </div>

                <div className="result-details">
                    <div className="detail-item">
                        <span className="detail-label">Correct Answers:</span>
                        <span className="detail-value">{result.correct} / {result.total}</span>
                    </div>
                    <div className="detail-item">
                        <span className="detail-label">Status:</span>
                        <span className={`detail-value ${passed ? 'pass-text' : 'fail-text'}`}>
                            {passed ? 'Passed ✓' : 'Need More Practice'}
                        </span>
                    </div>
                </div>

                <div className="result-message">
                    {passed ? (
                        <p>Great job! You've demonstrated a solid understanding of the material.</p>
                    ) : (
                        <p>Don't give up! Review the course material and try again.</p>
                    )}
                </div>

                <div className="result-actions">
                    <Link to={`/quiz/${id}`} className="btn btn-secondary">
                        Retake Quiz
                    </Link>
                    <Link to="/dashboard" className="btn btn-primary">
                        Back to Dashboard
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default QuizResult;

