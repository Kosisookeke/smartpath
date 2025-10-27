/**
 * Quiz Taking Page Component
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { quizAPI } from '../services/api';
import './Quiz.css';

const Quiz = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [quiz, setQuiz] = useState(null);
    const [answers, setAnswers] = useState({});
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => {
        loadQuiz();
    }, [id]);

    const loadQuiz = async () => {
        try {
            const data = await quizAPI.getById(id, 'take');
            setQuiz(data.quiz);
        } catch (error) {
            console.error('Error loading quiz:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleAnswerChange = (questionId, answer) => {
        setAnswers({
            ...answers,
            [questionId]: answer
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Check if all questions are answered
        if (Object.keys(answers).length !== quiz.questions.length) {
            alert('Please answer all questions before submitting.');
            return;
        }

        setSubmitting(true);
        try {
            const result = await quizAPI.submit(id, answers);
            navigate(`/quiz/${id}/result`, { state: { result: result.result } });
        } catch (error) {
            console.error('Error submitting quiz:', error);
            alert('Error submitting quiz. Please try again.');
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) {
        return <div className="loading">Loading quiz...</div>;
    }

    if (!quiz) {
        return <div className="error">Quiz not found.</div>;
    }

    return (
        <div className="quiz-page">
            <div className="quiz-header">
                <h1>{quiz.title}</h1>
                <p>{quiz.description}</p>
                <div className="quiz-info">
                    <span>📝 {quiz.questions.length} Questions</span>
                </div>
            </div>

            <form onSubmit={handleSubmit} className="quiz-form">
                {quiz.questions.map((question, index) => (
                    <div key={question.id} className="question-card">
                        <h3 className="question-number">Question {index + 1}</h3>
                        <p className="question-text">{question.question_text}</p>

                        <div className="options">
                            {['A', 'B', 'C', 'D'].map(option => (
                                <label key={option} className="option-label">
                                    <input
                                        type="radio"
                                        name={`question-${question.id}`}
                                        value={option}
                                        checked={answers[question.id] === option}
                                        onChange={() => handleAnswerChange(question.id, option)}
                                    />
                                    <span className="option-text">
                                        <strong>{option}.</strong> {question[`option_${option.toLowerCase()}`]}
                                    </span>
                                </label>
                            ))}
                        </div>
                    </div>
                ))}

                <div className="quiz-actions">
                    <button
                        type="submit"
                        className="btn btn-primary btn-large"
                        disabled={submitting}
                    >
                        {submitting ? 'Submitting...' : 'Submit Quiz'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default Quiz;

