const API_BASE_URL = 'https://educonnect-wp9t.onrender.com/api'; // http://127.0.0.1:5000     https://educonnect-wp9t.onrender.com

function setToken(token) {
    localStorage.setItem('access_token', token);
}

function getToken() {
    return localStorage.getItem('access_token');
}

function setUserId(userId) {
    localStorage.setItem('user_id', userId);
}

function getUserId() {
    return localStorage.getItem('user_id');
}

function removeAuthData() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
}

function isAuthenticated() {
    return !!getToken(); // يرجع true إذا كان هناك توكن، وإلا false
}

function logout() {
    removeAuthData();
    // إعادة التوجيه إلى صفحة تسجيل الدخول
    window.location.href = 'login.html';
}

// دالة للتحقق من المصادقة في بداية تحميل الصفحات المحمية
function redirectToLoginIfNotAuthenticated() {
    if (!isAuthenticated()) {
        alert('يجب تسجيل الدخول للوصول إلى هذه الصفحة.');
        window.location.href = 'login.html';
    }
}

// دالة لعرض رسائل للمستخدم
function showMessage(elementId, message, type = 'error') {
    const messageDiv = document.getElementById(elementId);
    if (messageDiv) {
        messageDiv.textContent = message;
        messageDiv.className = `message ${type}`; // error or success
        messageDiv.style.display = 'block';
    }
}

function hideMessage(elementId) {
    const messageDiv = document.getElementById(elementId);
    if (messageDiv) {
        messageDiv.style.display = 'none';
    }
}