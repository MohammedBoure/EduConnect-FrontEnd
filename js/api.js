// تأكد من وجود API_BASE_URL (يمكن استيراده أو تعريفه هنا إذا لزم الأمر)
// const API_BASE_URL = 'http://127.0.0.1:5000'; // أو /api إذا كنت تستخدم proxy

async function fetchApi(endpoint, options = {}, authRequired = true, expectedResponseType = 'json') {
    const token = getToken(); // افترض وجود دالة getToken() في auth.js
    const headers = {
        // لا تضع Content-Type هنا بشكل افتراضي إذا كنت قد تستخدم FormData
        ...options.headers, // اسمح بتمرير ترويسات مخصصة
    };

    // أضف Content-Type فقط إذا لم يكن الجسم FormData وكان الجسم موجودًا
    if (!(options.body instanceof FormData) && options.body) {
        headers['Content-Type'] = 'application/json';
    }

    if (authRequired && token && !endpoint.startsWith('/login') && !endpoint.startsWith('/register')) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: headers,
            // تحويل الجسم إلى JSON فقط إذا لم يكن FormData وكان الجسم موجودًا
            body: (options.body && !(options.body instanceof FormData)) ? JSON.stringify(options.body) : options.body,
        });

        // حالة No Content (مثل الحذف الناجح)
        if (response.status === 204) {
            return { ok: true, data: { message: "تمت العملية بنجاح (لا يوجد محتوى)" } };
        }

        const rawResponse = await response.text(); // اقرأ الرد كنص أولاً

        // تحقق من نوع المحتوى المتوقع
        if (expectedResponseType === 'json') {
             const contentType = response.headers.get('Content-Type');
             if (contentType && !contentType.includes('application/json')) {
                // إذا لم تكن الاستجابة JSON، أرجع النص الخام مع حالة الخطأ
                 if (!response.ok) {
                    console.warn(`API Error (Not JSON): Status ${response.status}, Response: ${rawResponse}`);
                     return { ok: false, error: `خطأ ${response.status}: ${rawResponse || response.statusText}` };
                 } else {
                    // حتى لو كانت الاستجابة ناجحة ولكن ليست JSON كما هو متوقع
                    console.warn(`API Warning: Expected JSON but received ${contentType}. Response: ${rawResponse}`);
                     return { ok: true, data: rawResponse }; // أو يمكنك اعتبارها خطأ
                 }
            }

            // محاولة تحليل النص كـ JSON
            let data;
            try {
                data = JSON.parse(rawResponse);
            } catch (jsonError) {
                 console.error('JSON Parsing Error:', jsonError, 'Raw Response:', rawResponse);
                 // إذا فشل تحليل JSON، وكان الرد غير ناجح، أظهر الخطأ
                 if (!response.ok) {
                    return { ok: false, error: `خطأ ${response.status}: ${rawResponse || response.statusText} (فشل تحليل JSON)` };
                 } else {
                    // إذا كان الرد ناجحًا ولكن فشل التحليل (غير متوقع)
                    return { ok: false, error: `فشل تحليل استجابة JSON ناجحة: ${rawResponse}` };
                 }
            }

            // إذا كان التحليل ناجحًا ولكن الاستجابة غير ناجحة (مثل 4xx, 5xx)
            if (!response.ok) {
                 console.error('API Error Response (JSON Parsed):', data);
                return { ok: false, error: data.error || data.message || `خطأ HTTP! الحالة: ${response.status}` };
            }

            // كل شيء جيد (الاستجابة ناجحة وتم تحليل JSON)
            return { ok: true, data };

        } else { // إذا كان نوع الاستجابة المتوقع غير JSON (مثل text)
            if (!response.ok) {
                return { ok: false, error: `خطأ ${response.status}: ${rawResponse || response.statusText}` };
            }
            return { ok: response.ok, data: rawResponse };
        }

    } catch (error) { // أخطاء الشبكة أو أخطاء أخرى
        console.error(`API call failed for ${endpoint}: ${error.message}`, error);
        // حاول تقديم رسالة خطأ أكثر تحديدًا إذا أمكن
        let errorMessage = error.message || 'خطأ في الشبكة أو الخادم غير متاح';
        if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
             errorMessage = 'فشل الاتصال بالخادم. يرجى التحقق من اتصال الشبكة وعنوان الخادم.';
        }
        return { ok: false, error: errorMessage };
    }
}


// --- واجهات المصادقة (موجودة بالفعل) ---
async function apiRegister(userData) {
    return fetchApi('/register', {
        method: 'POST',
        body: userData, // الجسم ككائن JS
    }, false);
}

async function apiLogin(credentials) {
    return fetchApi('/login', {
        method: 'POST',
        body: credentials, // الجسم ككائن JS
    }, false);
}

// --- واجهات إدارة المستخدمين (موجودة بالفعل) ---
async function apiGetUsers(page = 1, perPage = 10, searchQuery = '') {
    let endpoint = `/admin/users?page=${page}&per_page=${perPage}`;
    if (searchQuery) {
        endpoint += `&search=${encodeURIComponent(searchQuery)}`;
    }
    return fetchApi(endpoint, { method: 'GET' });
}

async function apiGetUserDetails(userId) {
    // قد تحتاج هذه إلى مصادقة حسب تصميم API الخاص بك
    return fetchApi(`/admin/users/${userId}`, { method: 'GET' });
}

async function apiUpdateUser(userId, userData) {
    // إزالة الحقول غير القابلة للتعديل مباشرة
    const validData = { ...userData };
    delete validData.id; // عادة لا يتم إرسال المعرف في الجسم للتحديث
    delete validData.email; // قد لا تسمح بتغيير البريد الإلكتروني
    // تأكد من إرسال كلمة المرور فقط إذا تم تغييرها
    if (validData.password === '') {
        delete validData.password;
    }
    return fetchApi(`/admin/users/${userId}`, {
        method: 'PUT',
        body: validData, // الجسم ككائن JS
    });
}

async function apiDeleteUser(userId) {
    return fetchApi(`/admin/users/${userId}`, { method: 'DELETE' });
}


// --- واجهات إدارة المنشورات (موجودة بالفعل) ---
async function apiCreatePost(postData) {
    // قم بتعيين user_id تلقائيًا إذا لم يكن موجودًا وكان المستخدم مسجلاً
    if (!postData.user_id) {
        const userId = getUserId(); // افترض وجود هذه الدالة في auth.js
        if (userId) postData.user_id = parseInt(userId);
    }
    // إزالة الصورة إذا كانت فارغة
    if (postData.image === '') {
        delete postData.image;
    }
    return fetchApi('/admin/posts/create', {
        method: 'POST',
        body: postData, // الجسم ككائن JS
    });
}

async function apiGetPosts(page = 1, perPage = 10) {
    return fetchApi(`/admin/posts?page=${page}&per_page=${perPage}`, { method: 'GET' });
}


// دمج دالتي apiGetPostDetails في واحدة صحيحة
async function apiGetPostDetails(postId, isAdmin = false) {
    const endpoint = isAdmin ? `/admin/posts/${postId}` : `/posts/${postId}`;
    return fetchApi(endpoint, { method: 'GET' });
}


async function apiUpdatePost(postId, postData) {
    const validData = { ...postData };
    // إزالة الحقول التي لا يجب تحديثها عبر هذه الواجهة
    delete validData.id;
    delete validData.user_id;
    delete validData.author;
    delete validData.created_at;
    // إزالة الصورة إذا كانت فارغة
    if (validData.image === '') {
        delete validData.image;
    }
    return fetchApi(`/admin/posts/${postId}`, {
        method: 'PUT',
        body: validData, // الجسم ككائن JS
    });
}

async function apiDeletePost(postId) {
    return fetchApi(`/admin/posts/${postId}`, { method: 'DELETE' });
}


// --- واجهات التعليقات (العامة) ---
async function apiGetPostComments(postId, page = 1, perPage = 10) {
    return fetchApi(`/posts/${postId}/comments?page=${page}&per_page=${perPage}`, { method: 'GET' });
}

async function apiCreateComment(postId, commentData) {
    // تأكد من إضافة user_id إذا لزم الأمر وكان المستخدم مسجلاً
    if (!commentData.user_id) {
        const userId = getUserId();
        if (userId) commentData.user_id = parseInt(userId);
    }
     // تأكد من أن created_at بالتنسيق الصحيح إذا أرسلته
     if (commentData.created_at && !(commentData.created_at instanceof Date)) {
         try {
             commentData.created_at = new Date(commentData.created_at).toISOString();
         } catch (e) {
             console.error("Invalid date format for created_at", commentData.created_at);
             // قد ترغب في إزالة التاريخ أو إرجاع خطأ هنا
             delete commentData.created_at;
         }
     } else if (commentData.created_at instanceof Date) {
         commentData.created_at = commentData.created_at.toISOString();
     }

    return fetchApi(`/posts/${postId}/comments`, {
        method: 'POST',
        body: commentData, // الجسم ككائن JS
    });
}

// ملاحظة: الواجهات العامة لتحديث وحذف التعليق قد تتطلب منطق أذونات إضافي
async function apiUpdateComment(postId, commentId, commentData) {
    return fetchApi(`/posts/${postId}/comments/${commentId}`, {
        method: 'PUT',
        body: commentData, // الجسم ككائن JS
    });
}

async function apiDeleteComment(postId, commentId) {
    return fetchApi(`/posts/${postId}/comments/${commentId}`, { method: 'DELETE' });
}


// --- واجهات الإعجابات (العامة) ---
async function apiGetPostLikes(postId) {
    return fetchApi(`/posts/${postId}/likes`, { method: 'GET' });
}

async function apiLikePost(postId) {
    // الجسم قد يكون فارغًا أو يحتوي على user_id حسب تصميم API
    return fetchApi(`/posts/${postId}/likes`, { method: 'POST' });
}

async function apiUnlikePost(postId) {
    return fetchApi(`/posts/${postId}/likes`, { method: 'DELETE' });
}

// --- <<< الدوال الجديدة لإدارة التعليقات الإدارية >>> ---
/**
 * جلب قائمة التعليقات الإدارية مع ترقيم الصفحات.
 * @param {number} page رقم الصفحة
 * @param {number} perPage عدد العناصر في كل صفحة
 * @returns {Promise<object>} كائن يحتوي على ok, data أو error
 */
async function apiAdminGetComments(page = 1, perPage = 10) {
    return fetchApi(`/admin/comments?page=${page}&per_page=${perPage}`, { method: 'GET' });
}

/**
 * إضافة تعليق جديد من لوحة الإدارة.
 * @param {number} postId معرف المنشور
 * @param {object} commentData بيانات التعليق { content, user_id, created_at }
 * @returns {Promise<object>} كائن يحتوي على ok, data أو error
 */
async function apiAdminAddComment(postId, commentData) {
     // تأكد من أن created_at بالتنسيق الصحيح ISO 8601
     if (commentData.created_at && !(commentData.created_at instanceof Date)) {
         try {
             commentData.created_at = new Date(commentData.created_at).toISOString();
         } catch (e) {
             console.error("Invalid date format for created_at", commentData.created_at);
             // API يتوقع تاريخًا، قد تحتاج لمعالجة هذا الخطأ بشكل أفضل
             return { ok: false, error: "تنسيق تاريخ الإنشاء غير صالح." };
         }
     } else if (commentData.created_at instanceof Date) {
         commentData.created_at = commentData.created_at.toISOString();
     } else {
        // إذا لم يتم توفير التاريخ، لا ترسله (قد يقوم الخادم بتعيينه) أو قم بتعيينه الآن
        commentData.created_at = new Date().toISOString();
     }

     // تأكد من أن user_id هو رقم
     if (commentData.user_id) {
        commentData.user_id = parseInt(commentData.user_id);
     }

    return fetchApi(`/admin/posts/${postId}/comments`, {
        method: 'POST',
        body: commentData, // الجسم ككائن JS
    });
}

/**
 * تحديث محتوى تعليق موجود من لوحة الإدارة.
 * @param {number} commentId معرف التعليق
 * @param {object} commentData بيانات التعليق { content }
 * @returns {Promise<object>} كائن يحتوي على ok, data أو error
 */
async function apiAdminUpdateComment(commentId, commentData) {
    // تأكد من إرسال المحتوى فقط أو أي حقول أخرى يسمح الـ API بتحديثها
    const updatePayload = { content: commentData.content };
    return fetchApi(`/admin/comments/${commentId}`, {
        method: 'PUT',
        body: updatePayload, // الجسم ككائن JS
    });
}

/**
 * حذف تعليق من لوحة الإدارة.
 * @param {number} commentId معرف التعليق
 * @returns {Promise<object>} كائن يحتوي على ok, data أو error
 */
async function apiAdminDeleteComment(commentId) {
    // طريقة DELETE عادة لا تحتوي على جسم للطلب
    return fetchApi(`/admin/comments/${commentId}`, { method: 'DELETE' });
}


// --- دالة جديدة لجلب تعليقات منشور معين (إداري) ---
/**
 * جلب تعليقات منشور معين للوحة الإدارة مع ترقيم الصفحات.
 * @param {number} postId معرف المنشور
 * @param {number} page رقم الصفحة
 * @param {number} perPage عدد العناصر في كل صفحة
 * @returns {Promise<object>} كائن يحتوي على ok, data أو error
 */
async function apiAdminGetPostComments(postId, page = 1, perPage = 5) {
    // تأكد من أن نقطة النهاية هذه موجودة في الـ Backend الخاص بك
    return fetchApi(`/posts/${postId}/comments?page=${page}&per_page=${perPage}`, { method: 'GET' });
}



async function apiAdminCreateComment(postId, commentData) {
    const payload = { ...commentData };

    if (!payload.created_at) {
        payload.created_at = new Date().toISOString();
    } else if (!(payload.created_at instanceof Date)) {
        try {
            payload.created_at = new Date(payload.created_at).toISOString();
        } catch (e) {
            console.error("Invalid date format for created_at", payload.created_at);
            return { ok: false, error: "تنسيق تاريخ الإنشاء غير صالح." };
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
    }, true);
}