/**
 * Authentication Context for SmartPath
 * Manages user authentication state across the application
 */
import React, { createContext, useState, useContext, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Load user from localStorage on mount
    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            try {
                setUser(JSON.parse(storedUser));
            } catch (e) {
                localStorage.removeItem('user');
            }
        }
        setLoading(false);
    }, []);

    // Save user to localStorage whenever it changes
    useEffect(() => {
        if (user) {
            localStorage.setItem('user', JSON.stringify(user));
        } else {
            localStorage.removeItem('user');
        }
    }, [user]);

    const register = async (email, password, name) => {
        try {
            setError(null);
            const response = await authAPI.register(email, password, name);
            setUser(response.user);
            return { success: true, user: response.user };
        } catch (err) {
            setError(err.message);
            return { success: false, error: err.message };
        }
    };

    const login = async (email, password) => {
        try {
            setError(null);
            const response = await authAPI.login(email, password);
            setUser(response.user);
            return { success: true, user: response.user };
        } catch (err) {
            setError(err.message);
            return { success: false, error: err.message };
        }
    };

    const logout = () => {
        setUser(null);
        setError(null);
    };

    const updateProfile = async (data) => {
        try {
            setError(null);
            const response = await authAPI.updateUser(data);
            setUser(response.user);
            return { success: true, user: response.user };
        } catch (err) {
            setError(err.message);
            return { success: false, error: err.message };
        }
    };

    const isAdmin = () => {
        return user && user.role === 'admin';
    };

    const isAuthenticated = () => {
        return !!user;
    };

    const value = {
        user,
        loading,
        error,
        register,
        login,
        logout,
        updateProfile,
        isAdmin,
        isAuthenticated
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;

