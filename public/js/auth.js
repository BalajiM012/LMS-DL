// Authentication utilities for the frontend
class AuthManager {
    constructor() {
        this.baseURL = '/api/auth';
    }

    // Check if user is authenticated
    async isAuthenticated() {
        try {
            const response = await fetch(`${this.baseURL}/check-auth`, {
                method: 'GET',
                credentials: 'include'
            });
            const data = await response.json();
            return data.authenticated;
        } catch (error) {
            console.error('Auth check failed:', error);
            return false;
        }
    }

    // Get current user info
    async getCurrentUser() {
        try {
            const response = await fetch(`${this.baseURL}/me`, {
                method: 'GET',
                credentials: 'include'
            });
            if (response.ok) {
                const data = await response.json();
                return data.user;
            }
            return null;
        } catch (error) {
            console.error('Get current user failed:', error);
            return null;
        }
    }

    // Login user
    async login(username, password) {
        try {
            const response = await fetch(`${this.baseURL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();
            
            if (response.ok) {
                // Store user info in sessionStorage for quick access
                sessionStorage.setItem('user', JSON.stringify(data.user));
                return { success: true, user: data.user };
            } else {
                return { success: false, error: data.error };
            }
        } catch (error) {
            console.error('Login failed:', error);
            return { success: false, error: 'Network error occurred' };
        }
    }

    // Register user
    async register(userData) {
        try {
            const response = await fetch(`${this.baseURL}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(userData)
            });

            const data = await response.json();
            
            if (response.ok) {
                return { success: true, user: data.user };
            } else {
                return { success: false, error: data.error };
            }
        } catch (error) {
            console.error('Registration failed:', error);
            return { success: false, error: 'Network error occurred' };
        }
    }

    // Logout user
    async logout() {
        try {
            const response = await fetch(`${this.baseURL}/logout`, {
                method: 'POST',
                credentials: 'include'
            });

            if (response.ok) {
                // Clear sessionStorage
                sessionStorage.removeItem('user');
                return { success: true };
            } else {
                return { success: false, error: 'Logout failed' };
            }
        } catch (error) {
            console.error('Logout failed:', error);
            // Clear sessionStorage anyway
            sessionStorage.removeItem('user');
            return { success: false, error: 'Network error occurred' };
        }
    }

    // Redirect to login if not authenticated
    async requireAuth(requiredRole = null) {
        const isAuth = await this.isAuthenticated();
        
        if (!isAuth) {
            window.location.href = '/index.html';
            return false;
        }

        if (requiredRole) {
            const user = await this.getCurrentUser();
            if (!user || user.role !== requiredRole) {
                alert('Access denied. Insufficient permissions.');
                window.location.href = '/index.html';
                return false;
            }
        }

        return true;
    }

    // Get user from sessionStorage (quick access)
    getUserFromStorage() {
        try {
            const userStr = sessionStorage.getItem('user');
            return userStr ? JSON.parse(userStr) : null;
        } catch (error) {
            console.error('Error parsing user from storage:', error);
            return null;
        }
    }

    // Update user in sessionStorage
    updateUserInStorage(user) {
        sessionStorage.setItem('user', JSON.stringify(user));
    }

    // Show loading state
    showLoading(element, text = 'Loading...') {
        if (element) {
            element.disabled = true;
            element.textContent = text;
        }
    }

    // Hide loading state
    hideLoading(element, originalText) {
        if (element) {
            element.disabled = false;
            element.textContent = originalText;
        }
    }

    // Show error message
    showError(errorElement, message) {
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }
    }

    // Hide error message
    hideError(errorElement) {
        if (errorElement) {
            errorElement.style.display = 'none';
        }
    }
}

// Create global auth manager instance
const authManager = new AuthManager();

// Utility functions for common auth operations
async function checkAuthAndRedirect(requiredRole = null) {
    return await authManager.requireAuth(requiredRole);
}

async function handleLogout() {
    const result = await authManager.logout();
    if (result.success) {
        window.location.href = '/index.html';
    } else {
        alert('Logout failed: ' + result.error);
    }
}

// Auto-redirect based on user role
async function redirectBasedOnRole() {
    const user = await authManager.getCurrentUser();
    if (user) {
        if (user.role === 'admin') {
            window.location.href = '/admin-dashboard-enhanced.html';
        } else if (user.role === 'student') {
            window.location.href = '/student-dashboard-enhanced.html';
        }
    }
}
