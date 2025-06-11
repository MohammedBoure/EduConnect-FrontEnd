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
            credentials: 'include',
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

// Authentication APIs
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
    return result;
}

// Profile APIs
async function apiGetProfile(userId) {
    return await fetchApi(`/profile/${userId}`, {
        method: 'GET',
    }, 'json');
}

async function apiUpdateProfile(userId, profileData) {
    return await fetchApi(`/profile/${userId}`, {
        method: 'PUT',
        body: profileData,
    }, 'json');
}

async function apiDeleteProfile(userId) {
    return await fetchApi(`/profile/${userId}`, {
        method: 'DELETE',
    }, 'json');
}

async function apiSearchUsers({ name = '', department = '', skill = '', page = 1, per_page = 10 }) {
    const query = `name=${encodeURIComponent(name)}&department=${encodeURIComponent(department)}&skill=${encodeURIComponent(skill)}&page=${page}&per_page=${per_page}`;
    return await fetchApi(`/search?${query}`, {
        method: 'GET',
    }, 'json');
}

async function apiGetUsers(page = 1, perPage = 10) {
    return await fetchApi(`/admin/users?page=${page}&per_page=${perPage}`, {
        method: 'GET',
    }, 'json');
}

// Post APIs
async function apiGetUserPosts(userId, page = 1, perPage = 10) {
    return await fetchApi(`/posts/user/${userId}?page=${page}&per_page=${perPage}`, {
        method: 'GET',
    }, 'json');
}

async function apiGetAdminUserPosts(page = 1, perPage = 10) {
    return await fetchApi(`/posts/admin_user_posts?page=${page}&per_page=${perPage}`, {
        method: 'GET',
    }, 'json');
}

async function apiGetPost(postId) {
    return await fetchApi(`/posts/${postId}`, {
        method: 'GET',
    }, 'json');
}

async function apiCreatePost(postData) {
    return await fetchApi('/posts', {
        method: 'POST',
        body: postData,
    }, 'json');
}

async function apiGetPosts(page = 1, perPage = 10) {
    return await fetchApi(`/posts/users_posts?page=${page}&per_page=${perPage}`, {
        method: 'GET',
    }, 'json');
}

async function apiUpdatePost(postId, postData) {
    return await fetchApi(`/posts/${postId}`, {
        method: 'PUT',
        body: postData,
    }, 'json');
}

async function apiDeletePost(postId) {
    return await fetchApi(`/posts/${postId}`, {
        method: 'DELETE',
    }, 'json');
}

// Comment APIs
async function apiGetComments(postId) {
    return await fetchApi(`/posts/${postId}/comments`, {
        method: 'GET',
    }, 'json');
}

async function postComment(postId, content) {
    const createdAt = new Date().toISOString(); // Generate ISO format timestamp
    const payload = {
        content: content,
        created_at: createdAt
    };

    const response = await fetchApi(`/posts/${postId}/comments`, {
        method: 'POST',
        body: payload,
    });

    return response;
}

// Message APIs
async function apiSendMessage(recipientId, content) {
    return await fetchApi(`/messages`, {
        method: 'POST',
        body: {
            receiver_id: recipientId,
            content: content
        }
    }, 'json');
}

async function apiGetMessages(recipientId) {
    return await fetchApi(`/messages/${recipientId}`, {
        method: 'GET',
    }, 'json');
}