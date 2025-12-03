/**
 * Home Page Component
 */
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Home.css';

const Home = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="home">
      <section className="hero">
        <div className="hero-content">
          <h1>Welcome to SmartPath </h1>
          <p className="hero-subtitle">
            Empowering learners across Africa and beyond with accessible,
            high-quality education resources
          </p>
          <div className="hero-buttons">
            {isAuthenticated() ? (
              <>
                <Link to="/dashboard" className="btn btn-primary btn-large">
                  Go to Dashboard
                </Link>
                <Link to="/courses" className="btn btn-secondary btn-large">
                  Browse Courses
                </Link>
              </>
            ) : (
              <>
                <Link to="/register" className="btn btn-primary btn-large">
                  Get Started Free
                </Link>
                <Link to="/login" className="btn btn-secondary btn-large">
                  Login
                </Link>
              </>
            )}
          </div>
        </div>
      </section>

      <section className="features-section">
        <h2>Why Choose SmartPath?</h2>
        <div className="features-grid">
          <div className="feature-item">
            <div className="feature-icon">📚</div>
            <h3>Quality Content</h3>
            <p>Access curated learning materials created by experienced educators</p>
          </div>
          <div className="feature-item">
            <div className="feature-icon">✅</div>
            <h3>Interactive Quizzes</h3>
            <p>Test your knowledge with engaging quizzes and get instant feedback</p>
          </div>
          <div className="feature-item">
            <div className="feature-icon">📊</div>
            <h3>Track Progress</h3>
            <p>Monitor your learning journey and celebrate your achievements</p>
          </div>
          <div className="feature-item">
            <div className="feature-icon">🌍</div>
            <h3>Learn Anywhere</h3>
            <p>Access your courses anytime, anywhere, on any device</p>
          </div>
        </div>
      </section>

      <section className="stats-section">
        <div className="stats-grid">
          <div className="stat-item">
            <h3>1000+</h3>
            <p>Students</p>
          </div>
          <div className="stat-item">
            <h3>50+</h3>
            <p>Courses</p>
          </div>
          <div className="stat-item">
            <h3>95%</h3>
            <p>Success Rate</p>
          </div>
          <div className="stat-item">
            <h3>24/7</h3>
            <p>Support</p>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <h2>Ready to Start Learning?</h2>
        <p>Join thousands of students already learning on SmartPath</p>
        {!isAuthenticated() && (
          <Link to="/register" className="btn btn-primary btn-large">
            Create Free Account
          </Link>
        )}
      </section>
    </div>
  );
};

export default Home;
