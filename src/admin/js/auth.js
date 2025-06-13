// http://127.0.0.1:5000/api
// https://educonnect-wp9t.onrender.com/api
const API_BASE_URL = 'http://127.0.0.1:5000/api';

function setAuthData(userId, role) {
    if (userId === undefined || userId === null || !role) {
        console.error('setAuthData: userId or role is undefined or null');
        return;
    }
    localStorage.setItem('user_id', userId);
    localStorage.setItem('role', role);
}

function getUserId() {
    const userId = localStorage.getItem('user_id');
    return userId ? parseInt(userId) : null;
}

function getRole() {
    return localStorage.getItem('role'); // Returns 'user', 'admin', or null
}

function removeAuthData() {
    localStorage.removeItem('user_id');
    localStorage.removeItem('role');
}

function isAuthenticated() {
    return !!getUserId() && !!getRole(); // Check if user_id and role exist
}

function isAdmin() {
    return isAuthenticated() && getRole() === 'admin'; // Check if user is admin
}

async function logout() {
    try {
        const response = await fetch(`${API_BASE_URL}/logout`, {
            method: 'POST',
            credentials: 'include', // Send session cookie
        });
        if (response.ok) {
            removeAuthData();
            window.location.href = 'login.html';
        } else {
            console.error('Logout failed:', await response.json());
            alert('Logout failed. Please try again.');
        }
    } catch (error) {
        console.error('Logout error:', error);
        alert('An error occurred during logout.');
    }
}

function redirectToLoginIfNotAuthenticated(requireAdmin = false) {
    const userId = getUserId();
    const role = getRole();

    if (!userId || !role) {
        alert('You must be logged in to access this page.');
        window.location.href = 'login.html';
        return true;
    }

    if (role === 'user') {
        window.location.href = 'login.html';
        return true;
    }

    if (requireAdmin && role !== 'admin') {
        alert('You must be an admin to access this page.');
        window.location.href = 'login.html';
        return true;
    }

    return false;
}

function showMessage(elementId, message, type = 'error') {
    const messageDiv = document.getElementById(elementId);
    if (messageDiv) {
        messageDiv.textContent = message;
        messageDiv.className = `message ${type}`;
        messageDiv.style.display = 'block';
    }
}

function hideMessage(elementId) {
    const messageDiv = document.getElementById(elementId);
    if (messageDiv) {
        messageDiv.style.display = 'none';
    }
}