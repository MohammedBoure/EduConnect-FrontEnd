# وثائق واجهات برمجة التطبيقات الإدارية (Admin APIs)

## نظرة عامة

هذه الوثيقة توضح واجهات برمجة التطبيقات (APIs) الإدارية المتاحة في النظام. تم تصميم هذه الواجهات لتمكين المشرفين من إدارة المستخدمين، المنشورات، التعليقات، والرسائل.

## جدول المحتويات

- [المتطلبات الأساسية](#المتطلبات-الأساسية)
- [إدارة المستخدمين](#إدارة-المستخدمين)
- [إدارة المنشورات](#إدارة-المنشورات)
- [إدارة التعليقات](#إدارة-التعليقات)
- [إدارة الرسائل](#إدارة-الرسائل)

## المتطلبات الأساسية

- نوع المحتوى: `application/json` للطلبات التي تحتوي على جسم البيانات
- المصادقة: تتطلب معظم النقاط النهائية توثيق المستخدم كمشرف (admin)

## إدارة المستخدمين

### 1. الحصول على قائمة المستخدمين

**الطلب:**
```
GET /admin/users?page=1&per_page=10
```

**معلمات الاستعلام:**
- `page`: رقم الصفحة (افتراضياً: 1)
- `per_page`: عدد المستخدمين في الصفحة الواحدة (افتراضياً: 10)

**الاستجابة:**
```json
{
  "users": [
    {
      "id": 1,
      "last_name": "العلوي",
      "first_name": "محمد",
      "email": "mohammed@example.com",
      "department": "هندسة البرمجيات",
      "skills": ["JavaScript", "React", "Node.js"],
      "photo": "https://example.com/photos/mohammed.jpg",
      "role": "admin"
    },
    // المزيد من المستخدمين...
  ],
  "total": 25,
  "page": 1,
  "pages": 3,
  "per_page": 10
}
```

**مثال باستخدام JavaScript:**
```javascript
async function getUsers() {
  try {
    const response = await fetch('http://example.com/admin/users?page=1&per_page=10', {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer YOUR_AUTH_TOKEN'
      }
    });
    
    if (!response.ok) {
      throw new Error('فشل في الحصول على قائمة المستخدمين');
    }
    
    const data = await response.json();
    console.log('قائمة المستخدمين:', data);
    return data;
  } catch (error) {
    console.error('حدث خطأ:', error);
  }
}
```

### 2. الحصول على تفاصيل مستخدم محدد

**الطلب:**
```
GET /admin/users/{user_id}
```

**الاستجابة:**
```json
{
  "id": 1,
  "last_name": "العلوي",
  "first_name": "محمد",
  "email": "mohammed@example.com",
  "department": "هندسة البرمجيات",
  "skills": ["JavaScript", "React", "Node.js"],
  "photo": "https://example.com/photos/mohammed.jpg",
  "role": "admin"
}
```

**مثال باستخدام JavaScript:**
```javascript
async function getUserDetails(userId) {
  try {
    const response = await fetch(`http://example.com/admin/users/${userId}`, {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer YOUR_AUTH_TOKEN'
      }
    });
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('المستخدم غير موجود');
      }
      throw new Error('فشل في الحصول على تفاصيل المستخدم');
    }
    
    const user = await response.json();
    console.log('تفاصيل المستخدم:', user);
    return user;
  } catch (error) {
    console.error('حدث خطأ:', error);
  }
}
```

### 3. تحديث بيانات مستخدم

**الطلب:**
```
PUT /admin/users/{user_id}
```

**جسم الطلب:**
```json
{
  "last_name": "السعدي",
  "first_name": "أحمد",
  "email": "ahmed@example.com",
  "department": "علوم الحاسوب",
  "skills": ["Python", "Django", "AWS"],
  "photo": "https://example.com/photos/ahmed.jpg",
  "role": "user"
}
```

**الاستجابة:**
```json
{
  "message": "User updated successfully",
  "user": {
    "id": 1,
    "last_name": "السعدي",
    "first_name": "أحمد",
    "email": "ahmed@example.com",
    "department": "علوم الحاسوب",
    "skills": ["Python", "Django", "AWS"],
    "photo": "https://example.com/photos/ahmed.jpg",
    "role": "user"
  }
}
```

**مثال باستخدام JavaScript:**
```javascript
async function updateUser(userId, userData) {
  try {
    const response = await fetch(`http://example.com/admin/users/${userId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_AUTH_TOKEN'
      },
      body: JSON.stringify(userData)
    });
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('المستخدم غير موجود');
      }
      throw new Error('فشل في تحديث بيانات المستخدم');
    }
    
    const result = await response.json();
    console.log('تم تحديث المستخدم بنجاح:', result);
    return result;
  } catch (error) {
    console.error('حدث خطأ:', error);
  }
}

// مثال للاستخدام
const updatedData = {
  last_name: "السعدي",
  first_name: "أحمد",
  email: "ahmed@example.com",
  department: "علوم الحاسوب",
  skills: ["Python", "Django", "AWS"],
  role: "user"
};

updateUser(1, updatedData);
```

### 4. حذف مستخدم

**الطلب:**
```
DELETE /admin/users/{user_id}
```

**الاستجابة:**
```json
{
  "message": "User deleted successfully"
}
```

**مثال باستخدام JavaScript:**
```javascript
async function deleteUser(userId) {
  try {
    const response = await fetch(`http://example.com/admin/users/${userId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': 'Bearer YOUR_AUTH_TOKEN'
      }
    });
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('المستخدم غير موجود');
      }
      throw new Error('فشل في حذف المستخدم');
    }
    
    const result = await response.json();
    console.log('تم حذف المستخدم بنجاح:', result);
    return result;
  } catch (error) {
    console.error('حدث خطأ:', error);
  }
}
```

## إدارة المنشورات

### 1. إنشاء منشور جديد

**الطلب:**
```
POST /admin/posts/create
```

**جسم الطلب:**
```json
{
  "user_id": 1,
  "title": "منشور جديد",
  "content": "محتوى المنشور الجديد",
  "image": "https://example.com/images/post1.jpg"
}
```

**الاستجابة:**
```json
{
  "message": "Post created successfully",
  "post": {
    "id": 5,
    "title": "منشور جديد",
    "content": "محتوى المنشور الجديد",
    "image": "https://example.com/images/post1.jpg",
    "created_at": "2023-05-23T14:30:45.123Z",
    "user_id": 1,
    "author": {
      "first_name": "محمد",
      "last_name": "العلوي",
      "photo": "https://example.com/photos/mohammed.jpg"
    }
  }
}
```

**مثال باستخدام JavaScript:**
```javascript
async function createPost(postData) {
  try {
    const response = await fetch('http://example.com/admin/posts/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_AUTH_TOKEN'
      },
      body: JSON.stringify(postData)
    });
    
    if (!response.ok) {
      throw new Error('فشل في إنشاء المنشور');
    }
    
    const result = await response.json();
    console.log('تم إنشاء المنشور بنجاح:', result);
    return result;
  } catch (error) {
    console.error('حدث خطأ:', error);
  }
}

// مثال للاستخدام
const newPost = {
  user_id: 1,
  title: "منشور جديد",
  content: "محتوى المنشور الجديد",
  image: "https://example.com/images/post1.jpg"
};

createPost(newPost);
```

### 2. الحصول على قائمة المنشورات

**الطلب:**
```
GET /admin/posts?page=1&per_page=10
```

**معلمات الاستعلام:**
- `page`: رقم الصفحة (افتراضياً: 1)
- `per_page`: عدد المنشورات في الصفحة الواحدة (افتراضياً: 10)

**الاستجابة:**
```json
{
  "posts": [
    {
      "id": 5,
      "title": "منشور جديد",
      "content": "محتوى المنشور الجديد",
      "image": "https://example.com/images/post1.jpg",
      "created_at": "2023-05-23T14:30:45.123Z",
      "user_id": 1,
      "author": {
        "first_name": "محمد",
        "last_name": "العلوي",
        "photo": "https://example.com/photos/mohammed.jpg"
      }
    },
    // المزيد من المنشورات...
  ],
  "total": 25,
  "page": 1,
  "pages": 3,
  "per_page": 10
}
```

**مثال باستخدام JavaScript:**
```javascript
async function getPosts(page = 1, perPage = 10) {
  try {
    const response = await fetch(`http://example.com/admin/posts?page=${page}&per_page=${perPage}`, {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer YOUR_AUTH_TOKEN'
      }
    });
    
    if (!response.ok) {
      throw new Error('فشل في الحصول على قائمة المنشورات');
    }
    
    const data = await response.json();
    console.log('قائمة المنشورات:', data);
    return data;
  } catch (error) {
    console.error('حدث خطأ:', error);
  }
}
```

### 3. تحديث منشور

**الطلب:**
```
PUT /admin/posts/{post_id}
```

**جسم الطلب:**
```json
{
  "title": "منشور تم تحديثه",
  "content": "محتوى المنشور بعد التحديث",
  "image": "https://example.com/images/updated_post.jpg"
}
```

**الاستجابة:**
```json
{
  "message": "Post updated successfully",
  "post": {
    "id": 5,
    "title": "منشور تم تحديثه",
    "content": "محتوى المنشور بعد التحديث",
    "image": "https://example.com/images/updated_post.jpg",
    "created_at": "2023-05-23T14:30:45.123Z",
    "user_id": 1,
    "author": {
      "first_name": "محمد",
      "last_name": "العلوي",
      "photo": "https://example.com/photos/mohammed.jpg"
    }
  }
}
```

**مثال باستخدام JavaScript:**
```javascript
async function updatePost(postId, postData) {
  try {
    const response = await fetch(`http://example.com/admin/posts/${postId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_AUTH_TOKEN'
      },
      body: JSON.stringify(postData)
    });
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('المنشور غير موجود');
      }
      throw new Error('فشل في تحديث المنشور');
    }
    
    const result = await response.json();
    console.log('تم تحديث المنشور بنجاح:', result);
    return result;
  } catch (error) {
    console.error('حدث خطأ:', error);
  }
}

// مثال للاستخدام
const updatedPostData = {
  title: "منشور تم تحديثه",
  content: "محتوى المنشور بعد التحديث",
  image: "https://example.com/images/updated_post.jpg"
};

updatePost(5, updatedPostData);
```

### 4. حذف منشور

**الطلب:**
```
DELETE /admin/posts/{post_id}
```

**الاستجابة:**
```json
{
  "message": "Post deleted successfully"
}
```

**مثال باستخدام JavaScript:**
```javascript
async function deletePost(postId) {
  try {
    const response = await fetch(`http://example.com/admin/posts/${postId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': 'Bearer YOUR_AUTH_TOKEN'
      }
    });
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('المنشور غير موجود');
      }
      throw new Error('فشل في حذف المنشور');
    }
    
    const result = await response.json();
    console.log('تم حذف المنشور بنجاح:', result);
    return result;
  } catch (error) {
    console.error('حدث خطأ:', error);
  }
}
```

## إدارة التعليقات

### 1. إضافة تعليق جديد على منشور

**الطلب:**
```
POST /admin/posts/{post_id}/comments
```

**جسم الطلب:**
```json
{
  "content": "محتوى التعليق الجديد",
  "created_at": "2023-05-23T15:30:45.123Z"
}
```

**الاستجابة:**
```json
{
  "message": "Comment added successfully",
  "comment": {
    "id": 7,
    "content": "محتوى التعليق الجديد",
    "created_at": "2023-05-23T15:30:45.123Z",
    "post_id": 5,
    "user_id": 0
  }
}
```

**مثال باستخدام JavaScript:**
```javascript
async function addComment(postId, commentData) {
  try {
    const response = await fetch(`http://example.com/admin/posts/${postId}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_AUTH_TOKEN'
      },
      body: JSON.stringify(commentData)
    });
    
    if (!response.ok) {
      throw new Error('فشل في إضافة التعليق');
    }
    
    const result = await response.json();
    console.log('تمت إضافة التعليق بنجاح:', result);
    return result;
  } catch (error) {
    console.error('حدث خطأ:', error);
  }
}

// مثال للاستخدام
const newComment = {
  content: "محتوى التعليق الجديد",
  created_at: new Date().toISOString()
};

addComment(5, newComment);
```

### 2. الحصول على قائمة التعليقات

**الطلب:**
```
GET /admin/comments?page=1&per_page=20
```

**معلمات الاستعلام:**
- `page`: رقم الصفحة (افتراضياً: 1)
- `per_page`: عدد التعليقات في الصفحة الواحدة (افتراضياً: 20)

**الاستجابة:**
```json
{
  "comments": [
    {
      "id": 7,
      "content": "محتوى التعليق الجديد",
      "created_at": "2023-05-23T15:30:45.123Z",
      "post_id": 5,
      "user_id": 0,
      "author": {
        "last_name": "العلوي",
        "first_name": "محمد",
        "photo": "https://example.com/photos/mohammed.jpg"
      }
    },
    // المزيد من التعليقات...
  ],
  "total": 50,
  "page": 1,
  "pages": 3,
  "per_page": 20
}
```

**مثال باستخدام JavaScript:**
```javascript
async function getComments(page = 1, perPage = 20) {
  try {
    const response = await fetch(`http://example.com/admin/comments?page=${page}&per_page=${perPage}`, {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer YOUR_AUTH_TOKEN'
      }
    });
    
    if (!response.ok) {
      throw new Error('فشل في الحصول على قائمة التعليقات');
    }
    
    const data = await response.json();
    console.log('قائمة التعليقات:', data);
    return data;
  } catch (error) {
    console.error('حدث خطأ:', error);
  }
}
```

### 3. تحديث تعليق

**الطلب:**
```
PUT /admin/comments/{comment_id}
```

**جسم الطلب:**
```json
{
  "content": "محتوى التعليق بعد التحديث"
}
```

**الاستجابة:**
```json
{
  "message": "Comment updated successfully",
  "comment": {
    "id": 7,
    "content": "محتوى التعليق بعد التحديث",
    "created_at": "2023-05-23T15:30:45.123Z",
    "post_id": 5,
    "user_id": 0,
    "author": {
      "last_name": "العلوي",
      "first_name": "محمد",
      "photo": "https://example.com/photos/mohammed.jpg"
    }
  }
}
```

**مثال باستخدام JavaScript:**
```javascript
async function updateComment(commentId, commentData) {
  try {
    const response = await fetch(`http://example.com/admin/comments/${commentId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_AUTH_TOKEN'
      },
      body: JSON.stringify(commentData)
    });
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('التعليق غير موجود');
      }
      throw new Error('فشل في تحديث التعليق');
    }
    
    const result = await response.json();
    console.log('تم تحديث التعليق بنجاح:', result);
    return result;
  } catch (error) {
    console.error('حدث خطأ:', error);
  }
}

// مثال للاستخدام
const updatedCommentData = {
  content: "محتوى التعليق بعد التحديث"
};

updateComment(7, updatedCommentData);
```

### 4. حذف تعليق

**الطلب:**
```
DELETE /admin/comments/{comment_id}
```

**الاستجابة:**
```json
{
  "message": "Comment deleted successfully"
}
```

**مثال باستخدام JavaScript:**
```javascript
async function deleteComment(commentId) {
  try {
    const response = await fetch(`http://example.com/admin/comments/${commentId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': 'Bearer YOUR_AUTH_TOKEN'
      }
    });
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('التعليق غير موجود');
      }
      throw new Error('فشل في حذف التعليق');
    }
    
    const result = await response.json();
    console.log('تم حذف التعليق بنجاح:', result);
    return result;
  } catch (error) {
    console.error('حدث خطأ:', error);
  }
}
```

## إدارة الرسائل

### 1. الحصول على قائمة الرسائل

**الطلب:**
```
GET /admin/messages?page=1&per_page=30
```

**معلمات الاستعلام:**
- `page`: رقم الصفحة (افتراضياً: 1)
- `per_page`: عدد الرسائل في الصفحة الواحدة (افتراضياً: 30)

**الاستجابة:**
```json
{
  "messages": [
    {
      "id": 10,
      "content": "محتوى الرسالة",
      "sender_id": 1,
      "receiver_id": 2,
      "created_at": "2023-05-23T16:30:45.123Z"
    },
    // المزيد من الرسائل...
  ],
  "total": 100,
  "page": 1,
  "pages": 4,
  "per_page": 30
}
```

**مثال باستخدام JavaScript:**
```javascript
async function getMessages(page = 1, perPage = 30) {
  try {
    const response = await fetch(`http://example.com/admin/messages?page=${page}&per_page=${perPage}`, {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer YOUR_AUTH_TOKEN'
      }
    });
    
    if (!response.ok) {
      throw new Error('فشل في الحصول على قائمة الرسائل');
    }
    
    const data = await response.json();
    console.log('قائمة الرسائل:', data);
    return data;
  } catch (error) {
    console.error('حدث خطأ:', error);
  }
}
```

### 2. إرسال رسالة جديدة

**الطلب:**
```
POST /admin/messages
```

**جسم الطلب:**
```json
{
  "sender_id": 1,
  "receiver_id": 2,
  "content": "محتوى الرسالة الجديدة"
}
```

**الاستجابة:**
```json
{
  "message": "Message sent successfully",
  "sent_message": {
    "id": 15,
    "content": "محتوى الرسالة الجديدة",
    "sender_id": 1,
    "receiver_id": 2,
    "created_at": "2023-05-23T17:30:45.123Z"
  }
}
```

**مثال باستخدام JavaScript:**
```javascript
async function sendMessage(messageData) {
  try {
    const response = await fetch('http://example.com/admin/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_AUTH_TOKEN'
      },
      body: JSON.stringify(messageData)
    });
    
    if (!response.ok) {
      throw new Error('فشل في إرسال الرسالة');
    }
    
    const result = await response.json();
    console.log('تم إرسال الرسالة بنجاح:', result);
    return result;
  } catch (error) {
    console.error('حدث خطأ:', error);
  }
}

// مثال للاستخدام
const newMessage = {
  sender_id: 1,
  receiver_id: 2,
  content: "محتوى الرسالة الجديدة"
};

sendMessage(newMessage);
```

### 3. الحصول على محادثة بين مستخدمين

**الطلب:**
```
POST /admin/messages/{other_user_id}
```

**جسم الطلب:**
```json
{
  "user_id": 1
}
```

**معلمات الاستعلام:**
- `page`: رقم الصفحة (افتراضياً: 1)
- `per_page`: عدد الرسائل في الصفحة الواحدة (افتراضياً: 30)

**الاستجابة:**
```json
{
  "messages": [
    {
      "id": 10,
      "content": "رسالة من المستخدم 1 إلى المستخدم 2",
      "sender_id": 1,
      "receiver_id": 2,
      "created_at": "2023-05-23T16:30:45.123Z"
    },
    {
      "id": 11,
      "content": "رسالة من المستخدم 2 إلى المستخدم 1",
      "sender_id": 2,
      "receiver_id": 1,
      "created_at": "2023-05-23T16:35:45.123Z"
    },
    // المزيد من الرسائل...
  ],
  "total": 20,
  "page": 1,
  "pages": 1,
  "per_page": 30
}
```

**مثال باستخدام JavaScript:**
```javascript
async function getConversation(userId, otherUserId, page = 1, perPage = 30) {
  try {
    const response = await fetch(`http://example.com/admin/messages/${otherUserId}?page=${page}&per_page=${perPage}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_AUTH_TOKEN'
      },
      body: JSON.stringify({ user_id: userId })
    });
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('المستخدم الآخر غير موجود');
      }
      throw new Error('فشل في الحصول على المحادثة');
    }
    
    const data = await response.json();
    console.log('محادثة المستخدمين:', data);
    return data;
  } catch (error) {
    console.error('حدث خطأ:', error);
  }
}

// مثال للاستخدام
getConversation(1, 2);
```

### 4. حذف رسالة

**الطلب:**
```
DELETE /admin/messages/{message_id}
```

**الاستجابة:**
```json
{
  "message": "Message deleted successfully"
}
```

**مثال باستخدام JavaScript:**
```javascript
async function deleteMessage(messageId) {
  try {
    const response = await fetch(`http://example.com/admin/messages/${messageId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': 'Bearer YOUR_AUTH_TOKEN'
      }
    });
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('الرسالة غير موجودة