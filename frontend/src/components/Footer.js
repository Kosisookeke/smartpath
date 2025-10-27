/**
 * Footer Component
 */
import React from 'react';
import './Footer.css';

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-container">
                <div className="footer-section">
                    <h3>SmartPath</h3>
                    <p>Empowering learners across Africa and beyond</p>
                </div>

                <div className="footer-section">
                    <h4>Quick Links</h4>
                    <ul>
                        <li><a href="/">Home</a></li>
                        <li><a href="/courses">Courses</a></li>
                        <li><a href="/about">About</a></li>
                        <li><a href="/contact">Contact</a></li>
                    </ul>
                </div>

                <div className="footer-section">
                    <h4>Resources</h4>
                    <ul>
                        <li><a href="/help">Help Center</a></li>
                        <li><a href="/terms">Terms of Service</a></li>
                        <li><a href="/privacy">Privacy Policy</a></li>
                    </ul>
                </div>

                <div className="footer-section">
                    <h4>Connect</h4>
                    <ul>
                        <li><a href="https://github.com">GitHub</a></li>
                        <li><a href="https://twitter.com">Twitter</a></li>
                        <li><a href="mailto:support@smartpath.com">Email</a></li>
                    </ul>
                </div>
            </div>

            <div className="footer-bottom">
                <p>&copy; 2025 SmartPath. All rights reserved. Made with ❤️ by the SmartPath Team</p>
            </div>
        </footer>
    );
};

export default Footer;

