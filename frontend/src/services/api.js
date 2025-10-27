/**
 * API Service for SmartPath
 * Handles all API communications with the backend
 */

const API_BASE_URL = 'http://localhost:5000/api';

// Helper function to get auth headers
const getAuthHeaders = () => {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    return {
        'Content-Type': 'application/json',
        'X-User-Id': user.id || ''
    };
};

// Handle API errors
const handleResponse = async (response) => {
    if (!response.ok) {
        const error = await response.json().catch(() => ({ error: 'Network error' }));
        throw new Error(error.error || 'Something went wrong');
    }
    return response.json();
};

// Authentication APIs
export const authAPI = {
    register: async (email, password, name) => {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, name })
        });
        return handleResponse(response);
    },

    login: async (email, password) => {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        return handleResponse(response);
    },

    getUser: async () => {
        const response = await fetch(`${API_BASE_URL}/auth/user`, {
            headers: getAuthHeaders()
        });
        return handleResponse(response);
    },

    updateUser: async (data) => {
        const response = await fetch(`${API_BASE_URL}/auth/user`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(data)
        });
        return handleResponse(response);
    }
};

// Course APIs
export const courseAPI = {
    getAll: async () => {
        const response = await fetch(`${API_BASE_URL}/courses/`);
        return handleResponse(response);
    },

    getById: async (id) => {
        const response = await fetch(`${API_BASE_URL}/courses/${id}`);
        return handleResponse(response);
    },

    create: async (courseData) => {
        const response = await fetch(`${API_BASE_URL}/courses/`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(courseData)
        });
        return handleResponse(response);
    },

    update: async (id, courseData) => {
        const response = await fetch(`${API_BASE_URL}/courses/${id}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(courseData)
        });
        return handleResponse(response);
    },

    delete: async (id) => {
        const response = await fetch(`${API_BASE_URL}/courses/${id}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        return handleResponse(response);
    }
};

// Quiz APIs
export const quizAPI = {
    getAll: async () => {
        const response = await fetch(`${API_BASE_URL}/quizzes/`);
        return handleResponse(response);
    },

    getById: async (id, mode = 'view') => {
        const response = await fetch(`${API_BASE_URL}/quizzes/${id}?mode=${mode}`, {
            headers: getAuthHeaders()
        });
        return handleResponse(response);
    },

    create: async (quizData) => {
        const response = await fetch(`${API_BASE_URL}/quizzes/`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(quizData)
        });
        return handleResponse(response);
    },

    submit: async (id, answers) => {
        const response = await fetch(`${API_BASE_URL}/quizzes/${id}/submit`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ answers })
        });
        return handleResponse(response);
    },

    getResults: async (id) => {
        const response = await fetch(`${API_BASE_URL}/quizzes/${id}/results`, {
            headers: getAuthHeaders()
        });
        return handleResponse(response);
    },

    getMyAttempts: async () => {
        const response = await fetch(`${API_BASE_URL}/quizzes/my-attempts`, {
            headers: getAuthHeaders()
        });
        return handleResponse(response);
    }
};

// Admin APIs
export const adminAPI = {
    getStats: async () => {
        const response = await fetch(`${API_BASE_URL}/admin/stats`, {
            headers: getAuthHeaders()
        });
        return handleResponse(response);
    },

    getUsers: async () => {
        const response = await fetch(`${API_BASE_URL}/admin/users`, {
            headers: getAuthHeaders()
        });
        return handleResponse(response);
    },

    updateUserRole: async (userId, role) => {
        const response = await fetch(`${API_BASE_URL}/admin/users/${userId}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify({ role })
        });
        return handleResponse(response);
    },

    getRecentActivity: async () => {
        const response = await fetch(`${API_BASE_URL}/admin/recent-activity`, {
            headers: getAuthHeaders()
        });
        return handleResponse(response);
    }
};

// Health check
export const healthCheck = async () => {
    const response = await fetch(`${API_BASE_URL}/health`);
    return handleResponse(response);
};

export default {
    auth: authAPI,
    course: courseAPI,
    quiz: quizAPI,
    admin: adminAPI,
    healthCheck
};

