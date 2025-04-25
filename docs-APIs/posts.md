# وثائق واجهات برمجة التطبيقات للمنشورات (Posts APIs)

## رابط الخادم
`https://educonnect-wp9t.onrender.com`  
استبدل هذا المسار بـ `http://127.0.0.1:5000` إذا كنت تعمل في بيئة الاختبار.

## نظرة عامة
تتيح واجهات المنشورات إنشاء، استرجاع، تحديث، وحذف المنشورات.

## المتطلبات الأساسية
- **الخادم**: يعمل على `https://educonnect-wp9t.onrender.com` في الإنتاج.
- **المصادقة**: مطلوبة (JWT) لإنشاء، تحديث، وحذف المنشورات.
- **نوع المحتوى**: `application/json` للطلبات التي تحتوي على جسم.
- **HTTPS**: يُوصى به في الإنتاج لحماية البيانات الحساسة.

## نقاط النهاية (Endpoints)

### 1. إنشاء منشور
- **الطريقة**: `POST`
- **الرابط**: `/api/posts`
- **الوصف**: إنشاء منشور جديد.
- **المصادقة**: مطلوبة (JWT).

#### جسم الطلب
| الحقل       | النوع   | الوصف                  | ملاحظات          |
|-------------|---------|------------------------|--------------------|
| `title` *   | String  | عنوان المنشور         | لا يمكن أن يكون فارغًا |
| `content` * | String  | محتوى المنشور         | لا يمكن أن يكون فارغًا |
| `image`     | String  | رابط صورة             | اختياري          |

**مثال**:
```json
{
  "title": "عنوان منشوري الأول",
  "content": "هذا هو محتوى منشوري الأول!",
  "image": "https://example.com/image.jpg"
}
```

#### الاستجابات
- **201 Created**:
  ```json
  {
    "message": "Post created successfully",
    "post": {
      "id": 1,
      "title": "عنوان منشوري الأول",
      "content": "هذا هو محتوى منشوري الأول!",
      "image": "https://example.com/image.jpg",
      "created_at": "2025-04-21T10:00:00Z",
      "user_id": 123,
      "author": {
        "first_name": "أحمد",
        "last_name": "بن علي",
        "photo": "https://example.com/photos/ahmed.jpg"
      }
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "Title and content cannot be empty"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to create post"}
  ```

#### مثال JavaScript (Frontend):
```javascript
async function createPost(postData, token) {
  try {
    const response = await fetch('https://educonnect-wp9t.onrender.com/api/posts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(postData),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to create post');
    }
    console.log('Post created:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// استخدام الدالة
const postData = {
  title: 'عنوان منشوري الأول',
  content: 'هذا هو محتوى منشوري الأول!',
  image: 'https://example.com/image.jpg',
};
const jwtToken = 'your_jwt_token_here';

createPost(postData, jwtToken)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 2. استرجاع منشورات المستخدم
- **الطريقة**: `GET`
- **الرابط**: `/api/posts/user/<user_id>` (مصادقة مطلوبة) أو `/api/posts/public/user/<user_id>` (عام)
- **الوصف**: استرجاع منشورات مستخدم معين.
- **المصادقة**: مطلوبة لـ `/api/posts/user/<user_id>`، غير مطلوبة لـ `/api/posts/public/user/<user_id>`.

#### معلمات المسار
| المعلم      | النوع   | الوصف                  | ملاحظات          |
|-------------|---------|------------------------|--------------------|
| `user_id` * | Integer | معرف المستخدم         | رقم صحيح         |

#### معلمات الاستعلام
| المعلمة    | النوع   | الوصف                    | الافتراضي |
|-------------|---------|--------------------------|-----------|
| `page`      | Integer | رقم الصفحة              | 1         |
| `per_page`  | Integer | عدد المنشورات لكل صفحة | 10        |

#### الاستجابات
- **200 OK**:
  ```json
  {
    "posts": [
      {
        "id": 1,
        "title": "عنوان منشوري الأول",
        "content": "هذا هو محتوى منشوري الأول!",
        "image": "https://example.com/image.jpg",
        "created_at": "2025-04-21T10:00:00Z",
        "user_id": 123,
        "author": {
          "first_name": "أحمد",
          "last_name": "بن علي",
          "photo": "https://example.com/photos/ahmed.jpg"
        }
      }
    ],
    "total": 1,
    "page": 1,
    "pages": 1,
    "per_page": 10
  }
  ```
- **404 Not Found**:
  ```json
  {"error": "User not found"}
  ```

#### مثال JavaScript (Frontend):
```javascript
async function getUserPosts(userId, page = 1, perPage = 10, token = null) {
  try {
    const endpoint = token ? `/api/posts/user/${userId}` : `/api/posts/public/user/${userId}`;
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

    const response = await fetch(
      `https://educonnect-wp9t.onrender.com${endpoint}?page=${page}&per_page=${perPage}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...headers,
        },
      }
    );

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to retrieve posts');
    }
    console.log('Posts retrieved:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// استخدام الدالة - منشورات عامة
getUserPosts(123)
  .then(data => console.log(data))
  .catch(error => console.error(error));

// استخدام الدالة - مع مصادقة
const jwtToken = 'your_jwt_token_here';
getUserPosts(123, 1, 20, jwtToken)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 3. تحديث منشور
- **الطريقة**: `PUT`
- **الرابط**: `/api/posts/<post_id>`
- **الوصف**: تحديث محتوى منشور.
- **المصادقة**: مطلوبة (JWT).

#### معلمات المسار
| المعلم      | النوع   | الوصف                  | ملاحظات          |
|-------------|---------|------------------------|--------------------|
| `post_id` * | Integer | معرف المنشور          | رقم صحيح         |

#### جسم الطلب
| الحقل       | النوع   | الوصف                  | ملاحظات          |
|-------------|---------|------------------------|--------------------|
| `title`     | String  | عنوان المنشور المحدث  | لا يمكن أن يكون فارغًا |
| `content`   | String  | محتوى المنشور المحدث  | لا يمكن أن يكون فارغًا |
| `image`     | String  | رابط صورة             | اختياري          |

**مثال**:
```json
{
  "title": "عنوان المنشور المحدث",
  "content": "هذا هو محتوى المنشور المحدث!",
  "image": "https://example.com/updated-image.jpg"
}
```

#### الاستجابات
- **200 OK**:
  ```json
  {
    "message": "Post updated successfully",
    "post": {
      "id": 1,
      "title": "عنوان المنشور المحدث",
      "content": "هذا هو محتوى المنشور المحدث!",
      "image": "https://example.com/updated-image.jpg",
      "created_at": "2025-04-21T10:00:00Z",
      "user_id": 123,
      "author": {
        "first_name": "أحمد",
        "last_name": "بن علي",
        "photo": "https://example.com/photos/ahmed.jpg"
      }
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "Title and content cannot be empty"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Post not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to update post"}
  ```

#### مثال JavaScript (Frontend):
```javascript
async function updatePost(postId, postData, token) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/api/posts/${postId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(postData),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to update post');
    }
    console.log('Post updated:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// استخدام الدالة
const postId = 1;
const postData = {
  title: 'عنوان المنشور المحدث',
  content: 'هذا هو محتوى المنشور المحدث!',
  image: 'https://example.com/updated-image.jpg',
};
const jwtToken = 'your_jwt_token_here';

updatePost(postId, postData, jwtToken)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 4. حذف منشور
- **الطريقة**: `DELETE`
- **الرابط**: `/api/posts/<post_id>`
- **الوصف**: حذف منشور.
- **المصادقة**: مطلوبة (JWT).

#### معلمات المسار
| المعلم      | النوع   | الوصف                  | ملاحظات          |
|-------------|---------|------------------------|--------------------|
| `post_id` * | Integer | معرف المنشور          | رقم صحيح         |

#### الاستجابات
- **200 OK**:
  ```json
  {"message": "Post deleted successfully"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Post not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to delete post"}
  ```

#### مثال JavaScript (Frontend):
```javascript
async function deletePost(postId, token) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/api/posts/${postId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to delete post');
    }
    console.log('Post deleted:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// استخدام الدالة
const postId = 1;
const jwtToken = 'your_jwt_token_here';

deletePost(postId, jwtToken)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```
### 5. استرجاع منشور
- **الطريقة**: `GET`
- **الرابط**: `/api/posts/<post_id>`
- **الوصف**: استرجاع تفاصيل منشور بناءً على معرفه.
- **المصادقة**: غير مطلوبة.

#### معلمات المسار
| المعلم      | النوع   | الوصف                  | ملاحظات          |
|-------------|---------|------------------------|--------------------|
| `post_id` * | Integer | معرف المنشور          | رقم صحيح         |

#### جسم الطلب
- لا يتطلب جسم طلب.

#### الاستجابات
- **200 OK**:
  ```json
  {
    "post": {
      "id": 1,
      "title": "عنوان المنشور",
      "content": "هذا هو محتوى المنشور!",
      "image": "https://example.com/image.jpg",
      "created_at": "2025-04-21T10:00:00Z",
      "user_id": 123,
      "author": {
        "first_name": "أحمد",
        "last_name": "بن علي",
        "photo": "https://example.com/photos/ahmed.jpg"
      }
    }
  }
  ```
- **404 Not Found**:
  ```json
  {"error": "Post not found"}
  ```

#### مثال JavaScript (Frontend):
```javascript
async function getPost(postId) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/api/posts/${postId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch post');
    }
    console.log('Post fetched:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// استخدام الدالة
const postId = 1;

getPost(postId)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```
## ملاحظات عامة
- يُوصى باستخدام HTTPS في الإنتاج لحماية البيانات الحساسة.
- اختبر الواجهات باستخدام أدوات مثل Postman أو cURL.
- رمز الوصول (JWT) يجب تضمينه في رأس الطلب كـ `Authorization: Bearer <token>` للواجهات التي تتطلب المصادقة.
- يتم تسجيل الإجراءات الإدارية (مثل تحديث أو حذف المنشورات) باستخدام `AuditLogManager` لأغراض التدقيق.
- النقطة النهائية العامة (`/api/posts/public/user/<user_id>`) تتيح استرجاع المنشورات بدون مصادقة، مما يناسب العرض العام للمنشورات.