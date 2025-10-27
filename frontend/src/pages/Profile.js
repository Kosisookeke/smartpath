/**
 * User Profile Page Component
 */
import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import './Profile.css';

const Profile = () => {
    const { user, updateProfile } = useAuth();
    const [editing, setEditing] = useState(false);
    const [formData, setFormData] = useState({
        name: user.name,
        email: user.email
    });
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage('');
        setError('');

        const result = await updateProfile(formData);

        if (result.success) {
            setMessage('Profile updated successfully!');
            setEditing(false);
        } else {
            setError(result.error);
        }
    };

    const handleCancel = () => {
        setFormData({
            name: user.name,
            email: user.email
        });
        setEditing(false);
        setError('');
    };

    return (
        <div className="profile-page">
            <div className="profile-container">
                <h1>My Profile</h1>

                {message && <div className="success-message">{message}</div>}
                {error && <div className="error-message">{error}</div>}

                <div className="profile-card">
                    <div className="profile-avatar">
                        <div className="avatar-circle">
                            {user.name.charAt(0).toUpperCase()}
                        </div>
                    </div>

                    {editing ? (
                        <form onSubmit={handleSubmit} className="profile-form">
                            <div className="form-group">
                                <label htmlFor="name">Full Name</label>
                                <input
                                    type="text"
                                    id="name"
                                    name="name"
                                    value={formData.name}
                                    onChange={handleChange}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="email">Email</label>
                                <input
                                    type="email"
                                    id="email"
                                    name="email"
                                    value={formData.email}
                                    onChange={handleChange}
                                    required
                                />
                            </div>

                            <div className="form-actions">
                                <button type="submit" className="btn btn-primary">
                                    Save Changes
                                </button>
                                <button type="button" className="btn btn-secondary" onClick={handleCancel}>
                                    Cancel
                                </button>
                            </div>
                        </form>
                    ) : (
                        <div className="profile-info">
                            <div className="info-item">
                                <span className="info-label">Name:</span>
                                <span className="info-value">{user.name}</span>
                            </div>

                            <div className="info-item">
                                <span className="info-label">Email:</span>
                                <span className="info-value">{user.email}</span>
                            </div>

                            <div className="info-item">
                                <span className="info-label">Role:</span>
                                <span className="info-value role-badge">{user.role}</span>
                            </div>

                            <div className="info-item">
                                <span className="info-label">Member Since:</span>
                                <span className="info-value">
                                    {new Date(user.created_at).toLocaleDateString()}
                                </span>
                            </div>

                            <button className="btn btn-primary" onClick={() => setEditing(true)}>
                                Edit Profile
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Profile;

