// http://127.0.0.1:5000/api
// https://educonnect-wp9t.onrender.com/api
const API_BASE_URL = 'https://educonnect-wp9t.onrender.com/api';
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

async function logout() {
    const result = await fetchApi('/logout', {
        method: 'POST',
    }, 'json');

    if (result.ok) {
        removeAuthData();
        window.location.href = 'login.html';
    } else {
        console.error('Logout failed:', result.error);
        alert(result.error || 'فشل تسجيل الخروج. حاول مرة أخرى.');
    }
}

function redirectToLoginIfNotAuthenticated(requireAdmin = false) {
    if (!isAuthenticated()) {
        alert('يجب تسجيل الدخول للوصول إلى هذه الصفحة.');
        window.location.href = 'login.html';
        return true;
    }
    if (requireAdmin && !isAdmin()) {
        alert('يجب أن تكون مديرًا للوصول إلى هذه الصفحة.');
        window.location.href = 'index.html';
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