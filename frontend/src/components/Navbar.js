/**
 * Navigation Bar Component
 */
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

const Navbar = () => {
    const { user, logout, isAdmin } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <Link to="/" className="navbar-logo">
                    📚 SmartPath
                </Link>

                <ul className="navbar-menu">
                    <li><Link to="/">Home</Link></li>
                    <li><Link to="/courses">Courses</Link></li>

                    {user ? (
                        <>
                            <li><Link to="/dashboard">Dashboard</Link></li>
                            {isAdmin() && <li><Link to="/admin">Admin</Link></li>}
                            <li><Link to="/profile">Profile</Link></li>
                            <li>
                                <button onClick={handleLogout} className="btn-logout">
                                    Logout
                                </button>
                            </li>
                            <li className="user-greeting">
                                Hello, {user.name}
                            </li>
                        </>
                    ) : (
                        <>
                            <li><Link to="/login" className="btn-login">Login</Link></li>
                            <li><Link to="/register" className="btn-register">Register</Link></li>
                        </>
                    )}
                </ul>
            </div>
        </nav>
    );
};

export default Navbar;

