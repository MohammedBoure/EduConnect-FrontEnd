// http://127.0.0.1:5000/api
// https://educonnect-wp9t.onrender.com/api
// --- DYNAMIC API URL CONFIGURATION ---

// ====================================================================
//                 *** DYNAMIC API URL CONFIGURATION ***
//
// This is the core of the dynamic server selection feature.
// It defines a global constant 'API_BASE_URL' that all other scripts
// can use without modification.
// ====================================================================

// 1. Define your default (fallback) API URL. This is used if the user hasn't set a custom one.
const DEFAULT_API_BASE_URL = 'https://educonnect-wp9t.onrender.com/api';

// 2. <<< التعديل الأساسي هنا >>>
// Create the global constant that all other files (like api.js) depend on.
// It intelligently checks localStorage for a custom URL and uses it if it exists.
// Otherwise, it falls back to the default URL.
const API_BASE_URL = localStorage.getItem('customApiBaseUrl') || DEFAULT_API_BASE_URL;

/**
 * A helper function primarily for the API settings modal.
 * It allows the modal to retrieve the currently active URL to display it in the input field.
 * @returns {string} The currently active API Base URL.
 */
function getApiBaseUrl() {
    // This function now simply returns the value of the globally defined constant.
    return API_BASE_URL;
}


// ====================================================================
//               *** AUTHENTICATION & USER FUNCTIONS ***
//          (No changes needed in the functions below)
// ====================================================================

/**
 * Saves user ID and role to localStorage.
 * @param {number|string} userId The user's ID.
 * @param {string} role The user's role (e.g., 'user', 'admin').
 */
function setAuthData(userId, role) {
    if (userId === undefined || userId === null || !role) {
        console.error('setAuthData Error: userId or role is missing.');
        return;
    }
    localStorage.setItem('user_id', userId);
    localStorage.setItem('role', role);
}

function getUserId() {
    const userId = localStorage.getItem('user_id');
    return userId ? parseInt(userId, 10) : null;
}

function getRole() {
    return localStorage.getItem('role');
}

function removeAuthData() {
    localStorage.removeItem('user_id');
    localStorage.removeItem('role');
}

function isAuthenticated() {
    return !!getUserId() && !!getRole();
}

function isAdmin() {
    return isAuthenticated() && getRole() === 'admin';
}

/**
 * Handles user logout by calling the API and clearing local data.
 * It will automatically use the correct API_BASE_URL.
 */
async function logout() {
    try {
        const response = await fetch(`${API_BASE_URL}/logout`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            const errorResult = await response.json().catch(() => ({}));
            console.warn('Logout API call failed:', errorResult.message || response.statusText);
        }

    } catch (error) {
        console.error('Network error during logout:', error);
    } finally {
        removeAuthData();
        alert('You have been logged out.');
        window.location.href = 'login.html';
    }
}

/**
 * Redirects user if they are not authenticated or don't have the required role.
 * @param {boolean} requireAdmin - If true, checks for admin role.
 * @returns {boolean} - True if a redirect occurred, false otherwise.
 */
function redirectToLoginIfNotAuthenticated(requireAdmin = false) {
    if (!isAuthenticated()) {
        alert('You must be logged in to access this page.');
        window.location.href = 'login.html';
        return true;
    }
    if (requireAdmin && !isAdmin()) {
        alert('You do not have permission to access this page.');
        window.location.href = 'index.html';
        return true;
    }
    return false;
}

// ====================================================================
//                       *** UI HELPER FUNCTIONS ***
// ====================================================================

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