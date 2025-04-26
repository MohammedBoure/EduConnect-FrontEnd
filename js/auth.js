const API_BASE_URL = 'http://127.0.0.1:5000/api'; // أو 'https://educonnect-wp9t.onrender.com/api' للإنتاج

function setToken(token) {
    if (!token) {
        console.error('setToken: Token is undefined or null');
        return;
    }
    localStorage.setItem('access_token', token);
}

function getToken() {
    return localStorage.getItem('access_token');
}

function setUserId(userId) {
    if (userId === undefined || userId === null) {
        console.error('setUserId: userId is undefined or null');
        return;
    }
    localStorage.setItem('user_id', userId);
}

function getUserId() {
    const userId = localStorage.getItem('user_id');
    return userId ? parseInt(userId) : null;
}

function removeAuthData() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
}

function isAuthenticated() {
    return !!getToken() && !!getUserId(); // التأكد من وجود كل من التوكن ومعرف المستخدم
}

function logout() {
    removeAuthData();
    window.location.href = 'login.html';
}

function redirectToLoginIfNotAuthenticated() {
    if (!isAuthenticated()) {
        alert('يجب تسجيل الدخول للوصول إلى هذه الصفحة.');
        window.location.href = 'login.html';
    }
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