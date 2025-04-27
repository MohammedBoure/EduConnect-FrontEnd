
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
            return { ok: true, data: { message: "تمت العملية بنجاح (لا يوجد محتوى)" } };
        }

        const rawResponse = await response.text();

        if (expectedResponseType === 'json') {
            const contentType = response.headers.get('Content-Type');
            if (contentType && !contentType.includes('application/json')) {
                if (!response.ok) {
                    console.warn(`API Error (Not JSON): Status ${response.status}, Response: ${rawResponse}`);
                    return { ok: false, error: `خطأ ${response.status}: ${rawResponse || response.statusText}` };
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
                    return { ok: false, error: `خطأ ${response.status}: ${rawResponse || response.statusText} (فشل تحليل JSON)` };
                } else {
                    return { ok: false, error: `فشل تحليل استجابة JSON ناجحة: ${rawResponse}` };
                }
            }

            if (!response.ok) {
                console.error('API Error Response (JSON Parsed):', data);
                if (response.status === 401) {
                    removeAuthData();
                    window.location.href = 'login.html';
                } else if (response.status === 403) {
                    return { ok: false, error: data.error || 'ممنوع: ليس لديك الصلاحيات الكافية' };
                }
                return { ok: false, error: data.error || data.message || `خطأ HTTP! الحالة: ${response.status}` };
            }

            return { ok: true, data };
        } else {
            if (!response.ok) {
                return { ok: false, error: `خطأ ${response.status}: ${rawResponse || response.statusText}` };
            }
            return { ok: response.ok, data: rawResponse };
        }
    } catch (error) {
        console.error(`API call failed for ${endpoint}: ${error.message}`, error);
        let errorMessage = error.message || 'خطأ في الشبكة أو الخادم غير متاح';
        if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
            errorMessage = 'فشل الاتصال بالخادم. يرجى التحقق من اتصال الشبكة وعنوان الخادم.';
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
    const query = `nom=${encodeURIComponent(name)}&filiere=${encodeURIComponent(department)}&competence=${encodeURIComponent(skill)}&page=${page}&per_page=${per_page}`;
    return await fetchApi(`/search?${query}`, {
        method: 'GET',
    }, 'json');
}

// Post APIs
async function apiGetAdminPosts() {
    return await fetchApi('/posts?admin=true', {
        method: 'GET',
    }, 'json');
}

async function apiGetPublicPosts() {
    return await fetchApi('/posts', {
        method: 'GET',
    }, 'json');
}

async function apiGetUserPosts(userId) {
    return await fetchApi(`/posts?user_id=${userId}`, {
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

async function apiCreateComment(postId, commentData) {
    return await fetchApi(`/posts/${postId}/comments`, {
        method: 'POST',
        body: commentData,
    }, 'json');
}

// Message APIs
async function apiGetContacts() {
    return await fetchApi('/messages/contacts', {
        method: 'GET',
    }, 'json');
}

async function apiGetMessages(recipientId) {
    return await fetchApi(`/messages/${recipientId}`, {
        method: 'GET',
    }, 'json');
}

async function apiSendMessage(recipientId, messageData) {
    return await fetchApi(`/messages/${recipientId}`, {
        method: 'POST',
        body: messageData,
    }, 'json');
}