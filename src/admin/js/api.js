//const API_BASE_URL = 'https://127.0.0.1:5000/api'; // Update to production URL, e.g., 'https://educonnect-wp9t.onrender.com/api'

async function fetchApi(endpoint, options = {}, expectedResponseType = 'json') {
    const headers = {
        ...options.headers,
    };

    if (!(options.body instanceof FormData) && options.body) {
        headers['Content-Type'] = 'application/json';
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: headers,
            body: options.body && !(options.body instanceof FormData) ? JSON.stringify(options.body) : options.body,
            credentials: 'include', // Send session cookie
        });

        if (response.status === 204) {
            return { ok: true, data: { message: "Operation completed successfully (no content)" } };
        }

        const rawResponse = await response.text();

        if (expectedResponseType === 'json') {
            const contentType = response.headers.get('Content-Type');
            if (contentType && !contentType.includes('application/json')) {
                if (!response.ok) {
                    console.warn(`API Error (Not JSON): Status ${response.status}, Response: ${rawResponse}`);
                    return { ok: false, error: `Error ${response.status}: ${rawResponse || response.statusText}` };
                } else {
                    console.warn(`API Warning: Expected JSON but received ${contentType}. Response: ${rawResponse}`);
                    return { ok: true, data: rawResponse };
                }
            }

            let data;
            try {
                data = JSON.parse(rawResponse);
            } catch (jsonError) {
                console.error('JSON Parsing Error:', jsonError, 'Raw Response:', rawResponse);
                if (!response.ok) {
                    return { ok: false, error: `Error ${response.status}: ${rawResponse || response.statusText} (JSON parsing failed)` };
                } else {
                    return { ok: false, error: `Failed to parse successful JSON response: ${rawResponse}` };
                }
            }

            if (!response.ok) {
                console.error('API Error Response (JSON Parsed):', data);
                if (response.status === 401) {
                    removeAuthData();
                    window.location.href = 'login.html';
                } else if (response.status === 403) {
                    return { ok: false, error: data.error || 'Forbidden: You do not have sufficient permissions' };
                }
                return { ok: false, error: data.error || data.message || `HTTP Error! Status: ${response.status}` };
            }

            return { ok: true, data };
        } else {
            if (!response.ok) {
                return { ok: false, error: `Error ${response.status}: ${rawResponse || response.statusText}` };
            }
            return { ok: response.ok, data: rawResponse };
        }
    } catch (error) {
        console.error(`API call failed for ${endpoint}: ${error.message}`, error);
        let errorMessage = error.message || 'Network error or server unavailable';
        if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
            errorMessage = 'Failed to connect to the server. Please check your network connection and server address.';
        }
        return { ok: false, error: errorMessage };
    }
}

// --- Authentication APIs ---
async function apiRegister(userData) {
    const result = await fetchApi('/register', {
        method: 'POST',
        body: userData,
    }, 'json');
    if (result.ok) {
        setAuthData(result.data.user.id, result.data.user.role);
    }
    return result;
}

async function apiLogin(credentials) {
    const result = await fetchApi('/login', {
        method: 'POST',
        body: credentials,
    }, 'json');
    if (result.ok) {
        setAuthData(result.data.user.id, result.data.user.role);
    }
    console.log('apiLogin result:', result);
    return result;
}

// --- User Management APIs ---
async function apiGetUsers(page = 1, perPage = 10, searchQuery = '') {
    if (!isAdmin()) {
        return { ok: false, error: 'Forbidden: Admin privileges required' };
    }
    let endpoint = `/admin/users?page=${page}&per_page=${perPage}`;
    if (searchQuery) {
        endpoint += `&search=${encodeURIComponent(searchQuery)}`;
    }
    return fetchApi(endpoint, { method: 'GET' });
}

async function apiGetUserDetails(userId) {
    return fetchApi(`/profile/${userId}`, { method: 'GET' });
}

async function apiUpdateUser(userId, userData) {
    const result = await fetchApi(`/admin/users/${userId}`, {
        method: 'PUT',
        body: userData,
    });
    return result;
}

async function apiDeleteUser(userId) {
    const result = await fetchApi(`/admin/users/${userId}`, {
        method: 'DELETE',
    });
    return result;
}

// --- Profile Search API ---
async function apiSearchProfiles({ nom = '', filiere = '', competence = '', page = 1, perPage = 10 }) {
    if (!isAuthenticated()) {
        return { ok: false, error: 'You must be logged in to search profiles' };
    }
    const params = new URLSearchParams({
        nom,
        filiere,
        competence,
        page,
        per_page: perPage,
    });
    return fetchApi(`/search?${params.toString()}`, { method: 'GET' });
}

// --- Post Management APIs ---
async function apiCreatePost(postData) {
    if (!isAuthenticated()) {
        return { ok: false, error: 'You must be logged in to create a post' };
    }
    const payload = { ...postData };
    if (!payload.user_id) {
        const userId = getUserId();
        if (userId) payload.user_id = parseInt(userId);
    }
    if (payload.image === '') {
        delete payload.image;
    }
    const endpoint = isAdmin() ? '/admin/posts/create' : '/posts';
    return fetchApi(endpoint, {
        method: 'POST',
        body: payload,
    });
}

async function apiGetPosts(page = 1, perPage = 10) {
    const endpoint = isAdmin() ? `/admin/posts?page=${page}&per_page=${perPage}` : `/posts?page=${page}&per_page=${perPage}`;
    return fetchApi(endpoint, { method: 'GET' });
}

async function apiGetPostDetails(postId, isAdmin = false) {
    const endpoint = isAdmin ? `/admin/posts/${postId}` : `/posts/${postId}`;
    return fetchApi(endpoint, { method: 'GET' });
}

async function apiUpdatePost(postId, postData) {
    if (!isAdmin()) {
        return { ok: false, error: 'Forbidden: Admin privileges required' };
    }
    const validData = { ...postData };
    delete validData.id;
    delete validData.user_id;
    delete validData.author;
    delete validData.created_at;
    if (validData.image === '') {
        delete validData.image;
    }
    return fetchApi(`/admin/posts/${postId}`, {
        method: 'PUT',
        body: validData,
    });
}

async function apiDeletePost(postId) {
    if (!isAdmin()) {
        return { ok: false, error: 'Forbidden: Admin privileges required' };
    }
    return fetchApi(`/admin/posts/${postId}`, { method: 'DELETE' });
}

// --- Comment Management APIs (Public) ---
async function apiGetPostComments(postId, page = 1, perPage = 10) {
    return fetchApi(`/posts/${postId}/comments?page=${page}&per_page=${perPage}`, { method: 'GET' });
}

async function apiCreateComment(postId, commentData) {
    if (!isAuthenticated()) {
        return { ok: false, error: 'You must be logged in to add a comment' };
    }
    const payload = { ...commentData };
    if (!payload.user_id) {
        const userId = getUserId();
        if (userId) payload.user_id = parseInt(userId);
    }
    if (payload.created_at && !(payload.created_at instanceof Date)) {
        try {
            payload.created_at = new Date(payload.created_at).toISOString();
        } catch (e) {
            console.error('Invalid date format for created_at', payload.created_at);
            delete payload.created_at;
        }
    } else if (payload.created_at instanceof Date) {
        payload.created_at = payload.created_at.toISOString();
    }
    return fetchApi(`/posts/${postId}/comments`, {
        method: 'POST',
        body: payload,
    });
}

async function apiUpdateComment(postId, commentId, commentData) {
    if (!isAuthenticated()) {
        return { ok: false, error: 'You must be logged in to update a comment' };
    }
    return fetchApi(`/posts/${postId}/comments/${commentId}`, {
        method: 'PUT',
        body: commentData,
    });
}

async function apiDeleteComment(postId, commentId) {
    if (!isAuthenticated()) {
        return { ok: false, error: 'You must be logged in to delete a comment' };
    }
    return fetchApi(`/posts/${postId}/comments/${commentId}`, { method: 'DELETE' });
}

// --- Like Management APIs (Public) ---
async function apiGetPostLikes(postId) {
    return fetchApi(`/posts/${postId}/likes`, { method: 'GET' });
}

async function apiLikePost(postId) {
    if (!isAuthenticated()) {
        return { ok: false, error: 'You must be logged in to like a post' };
    }
    return fetchApi(`/posts/${postId}/likes`, { method: 'POST' });
}

async function apiUnlikePost(postId) {
    if (!isAuthenticated()) {
        return { ok: false, error: 'You must be logged in to unlike a post' };
    }
    return fetchApi(`/posts/${postId}/likes`, { method: 'DELETE' });
}

// --- Admin Comment Management APIs ---
async function apiAdminGetComments(page = 1, perPage = 10) {
    if (!isAdmin()) {
        return { ok: false, error: 'Forbidden: Admin privileges required' };
    }
    return fetchApi(`/admin/comments?page=${page}&per_page=${perPage}`, { method: 'GET' });
}

async function apiAdminAddComment(postId, commentData) {
    if (!isAdmin()) {
        return { ok: false, error: 'Forbidden: Admin privileges required' };
    }
    const payload = { ...commentData };
    if (!payload.created_at) {
        payload.created_at = new Date().toISOString();
    } else if (!(payload.created_at instanceof Date)) {
        try {
            payload.created_at = new Date(payload.created_at).toISOString();
        } catch (e) {
            console.error('Invalid date format for created_at', payload.created_at);
            return { ok: false, error: 'Invalid creation date format.' };
        }
    } else {
        payload.created_at = payload.created_at.toISOString();
    }
    if (payload.user_id) {
        payload.user_id = parseInt(payload.user_id);
    }
    return fetchApi(`/admin/posts/${postId}/comments`, {
        method: 'POST',
        body: payload,
    });
}

async function apiAdminUpdateComment(commentId, commentData) {
    if (!isAdmin()) {
        return { ok: false, error: 'Forbidden: Admin privileges required' };
    }
    const updatePayload = { content: commentData.content };
    return fetchApi(`/admin/comments/${commentId}`, {
        method: 'PUT',
        body: updatePayload,
    });
}

async function apiAdminDeleteComment(commentId) {
    if (!isAdmin()) {
        return { ok: false, error: 'Forbidden: Admin privileges required' };
    }
    return fetchApi(`/admin/comments/${commentId}`, { method: 'DELETE' });
}

async function apiAdminGetPostComments(postId, page = 1, perPage = 5) {
    if (!isAdmin()) {
        return { ok: false, error: 'Forbidden: Admin privileges required' };
    }
    return fetchApi(`/posts/${postId}/comments?page=${page}&per_page=${perPage}`, { method: 'GET' });
}

async function apiAdminCreateComment(postId, commentData) {
    if (!isAdmin()) {
        return { ok: false, error: 'Forbidden: Admin privileges required' };
    }
    const payload = { ...commentData };
    if (!payload.created_at) {
        payload.created_at = new Date().toISOString();
    } else if (!(payload.created_at instanceof Date)) {
        try {
            payload.created_at = new Date(payload.created_at).toISOString();
        } catch (e) {
            console.error('Invalid date format for created_at', payload.created_at);
            return { ok: false, error: 'Invalid creation date format.' };
        }
    } else {
        payload.created_at = payload.created_at.toISOString();
    }
    if (payload.user_id) {
        payload.user_id = parseInt(payload.user_id);
    }
    return fetchApi(`/admin/posts/${postId}/comments`, {
        method: 'POST',
        body: payload,
    });
}

// --- Message Management APIs ---
async function getAllMessages(page = 1, perPage = 30) {
    if (!isAdmin()) {
        return { ok: false, error: 'Forbidden: Admin privileges required' };
    }
    return fetchApi(`/admin/messages?page=${page}&per_page=${perPage}`, { method: 'GET' });
}

async function getMessagesBetweenUsers(currentUserId, otherUserId, page = 1, perPage = 30) {
    if (!isAdmin()) {
        return { ok: false, error: 'Forbidden: Admin privileges required' };
    }
    return fetchApi(`/admin/messages/${currentUserId}/${otherUserId}?page=${page}&per_page=${perPage}`, { method: 'GET' });
}

async function sendMessage(senderId, receiverId, content) {
    if (!isAuthenticated()) {
        return { ok: false, error: 'You must be logged in to send a message' };
    }
    return fetchApi(`/admin/messages`, {
        method: 'POST',
        body: {
            sender_id: senderId,
            receiver_id: receiverId,
            content: content,
        },
    });
}

async function deleteMessage(messageId) {
    if (!isAdmin()) {
        return { ok: false, error: 'Forbidden: Admin privileges required' };
    }
    return fetchApi(`/admin/messages/${messageId}`, { method: 'DELETE' });
}

// --- CSRF Token Helper ---
async function getCsrfToken() {
    const result = await fetchApi('/csrf-token', { method: 'GET' });
    return result.ok ? result.data.csrf_token : null;
}