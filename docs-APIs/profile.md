# وثائق واجهات برمجة التطبيقات للملفات الشخصية (Profile APIs)

## رابط الخادم
`https://educonnect-wp9t.onrender.com`  
استبدل هذا المسار بـ `http://127.0.0.1:5000` إذا كنت تعمل في بيئة الاختبار.

## نظرة عامة
تتيح واجهات الملفات الشخصية استرجاع، تحديث، وحذف الملفات الشخصية والبحث عن مستخدمين بناءً على معايير محددة.

## المتطلبات الأساسية
- **الخادم**: يعمل على `https://educonnect-wp9t.onrender.com` في الإنتاج.
- **المصادقة**: مطلوبة (JWT) لتحديث، حذف، والبحث عن الملفات.
- **نوع المحتوى**: `application/json` للطلبات التي تحتوي على جسم.
- **HTTPS**: يُوصى به في الإنتاج لحماية البيانات الحساسة.

## نقاط النهاية (Endpoints)

### 1. استرجاع ملف المستخدم
- **الطريقة**: `GET`
- **الرابط**: `/api/profile/<user_id>`
- **الوصف**: استرجاع بيانات ملف مستخدم محدد بواسطة المعرف.
- **المصادقة**: غير مطلوبة.

#### معلمات المسار
| المعلم      | النوع   | الوصف                  | ملاحظات          |
|-------------|---------|------------------------|--------------------|
| `user_id` * | Integer | معرف المستخدم         | رقم صحيح موجب    |

#### الاستجابات
- **200 OK**:
  ```json
  {
    "id": 123,
    "last_name": "علي",
    "first_name": "أحمد",
    "email": "ahmed.ali@example.com",
    "department": "علوم الحاسوب",
    "skills": ["Python", "JavaScript", "React"],
    "photo": "https://example.com/photos/ahmed.jpg",
    "role": "user"
  }
  ```
- **404 Not Found**:
  ```json
  {"error": "User not found"}
  ```

#### مثال JavaScript (Frontend):
```javascript
async function getUserProfile(userId) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/api/profile/${userId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to retrieve profile');
    }
    console.log('Profile retrieved:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// استخدام الدالة
const userId = 123;
getUserProfile(userId)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 2. تحديث ملف المستخدم
- **الطريقة**: `PUT`
- **الرابط**: `/api/profile/<user_id>`
- **الوصف**: تحديث بيانات ملف المستخدم.
- **المصادقة**: مطلوبة (JWT، المستخدم صاحب الملف فقط).

#### معلمات المسار
| المعلم      | النوع   | الوصف                  | ملاحظات          |
|-------------|---------|------------------------|--------------------|
| `user_id` * | Integer | معرف المستخدم         | رقم صحيح موجب    |

#### جسم الطلب
| الحقل         | النوع           | الوصف                  | ملاحظات          |
|----------------|-----------------|------------------------|--------------------|
| `last_name`    | String          | الاسم الأخير          | اختياري          |
| `first_name`   | String          | الاسم الأول           | اختياري          |
| `department`   | String          | القسم أو التخصص      | اختياري          |
| `skills`       | Array/String    | قائمة المهارات        | اختياري، يمكن تقديمه كمصفوفة أو كسلسلة مفصولة بفواصل |
| `photo`        | String          | رابط الصورة           | اختياري          |
| `email`        | String          | البريد الإلكتروني     | اختياري          |
| `password`     | String          | كلمة المرور           | اختياري، يجب أن تكون 8 أحرف على الأقل |
| `role`         | String          | دور المستخدم          | اختياري، يقبل 'user' أو 'admin' فقط |

**مثال**:
```json
{
  "last_name": "محمد",
  "first_name": "أحمد",
  "department": "هندسة البرمجيات",
  "skills": ["Python", "Java", "SQL"],
  "photo": "https://example.com/photos/ahmed_new.jpg",
  "email": "ahmed.mohamed@example.com"
}
```

#### الاستجابات
- **200 OK**:
  ```json
  {
    "message": "User updated successfully",
    "user": {
      "id": 123,
      "last_name": "محمد",
      "first_name": "أحمد",
      "email": "ahmed.mohamed@example.com",
      "department": "هندسة البرمجيات",
      "skills": ["Python", "Java", "SQL"],
      "photo": "https://example.com/photos/ahmed_new.jpg",
      "role": "user"
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "No update data provided"}
  ```
- **400 Bad Request**:
  ```json
  {"error": "No valid fields provided for update"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **403 Forbidden**:
  ```json
  {"error": "Unauthorized: You can only update your own profile"}
  ```
- **404 Not Found**:
  ```json
  {"error": "User not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to update user"}
  ```

#### مثال JavaScript (Frontend):
```javascript
async function updateUserProfile(userId, updateData, token) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/api/profile/${userId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(updateData),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to update profile');
    }
    console.log('Profile updated:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// استخدام الدالة
const userId = 123;
const updateData = {
  last_name: 'محمد',
  first_name: 'أحمد',
  department: 'هندسة البرمجيات',
  skills: ['Python', 'Java', 'SQL'],
  photo: 'https://example.com/photos/ahmed_new.jpg',
  email: 'ahmed.mohamed@example.com',
};
const jwtToken = 'your_jwt_token_here';

updateUserProfile(userId, updateData, jwtToken)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 3. حذف ملف المستخدم
- **الطريقة**: `DELETE`
- **الرابط**: `/api/profile/<user_id>`
- **الوصف**: حذف ملف مستخدم.
- **المصادقة**: مطلوبة (JWT، المستخدم صاحب الملف فقط).

#### معلمات المسار
| المعلم      | النوع   | الوصف                  | ملاحظات          |
|-------------|---------|------------------------|--------------------|
| `user_id` * | Integer | معرف المستخدم         | رقم صحيح موجب    |

#### الاستجابات
- **200 OK**:
  ```json
  {"message": "User deleted successfully"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **403 Forbidden**:
  ```json
  {"error": "Unauthorized: You can only delete your own profile"}
  ```
- **404 Not Found**:
  ```json
  {"error": "User not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to delete user"}
  ```

#### مثال JavaScript (Frontend):
```javascript
async function deleteUserProfile(userId, token) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/api/profile/${userId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to delete profile');
    }
    console.log('Profile deleted:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// استخدام الدالة
const userId = 123;
const jwtToken = 'your_jwt_token_here';

deleteUserProfile(userId, jwtToken)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 4. البحث عن ملفات المستخدمين
- **الطريقة**: `GET`
- **الرابط**: `/api/search`
- **الوصف**: البحث عن ملفات المستخدمين بناءً على معايير محددة.
- **المصادقة**: مطلوبة (JWT).

#### معلمات الاستعلام
| المعلمة         | النوع   | الوصف                      | ملاحظات                   |
|-----------------|---------|----------------------------|-----------------------------|
| `name`          | String  | البحث بالاسم              | اختياري، يبحث في الاسم الأول والأخير |
| `department`    | String  | البحث حسب القسم           | اختياري                   |
| `skill`         | String  | البحث حسب المهارة         | اختياري                   |
| `exclude_user_id`| Integer | استبعاد مستخدم محدد      | اختياري                   |
| `page`          | Integer | رقم الصفحة                | اختياري، الافتراضي 1      |
| `per_page`      | Integer | عدد النتائج لكل صفحة     | اختياري، الافتراضي 10     |

#### الاستجابات
- **200 OK**:
  ```json
  {
    "results": [
      {
        "id": 124,
        "last_name": "عمر",
        "first_name": "محمد",
        "email": "mohamed.omar@example.com",
        "department": "علوم الحاسوب",
        "skills": ["Java", "SQL", "Spring"],
        "photo": "https://example.com/photos/mohamed.jpg",
        "role": "user"
      }
    ],
    "total": 1,
    "page": 1,
    "pages": 1,
    "per_page": 10
  }
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Missing JWT token"}
  ```

#### مثال JavaScript (Frontend):
```javascript
async function searchUsers(searchParams, token) {
  try {
    const query = new URLSearchParams(searchParams).toString();
    const response = await fetch(`https://educonnect-wp9t.onrender.com/api/search?${query}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to search users');
    }
    console.log('Search results:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// استخدام الدالة
const searchParams = {
  skill: 'Python',
  department: 'علوم الحاسوب',
  page: 1,
  per_page: 20,
};
const jwtToken = 'your_jwt_token_here';

searchUsers(searchParams, jwtToken)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## ملاحظات عامة
- يُوصى باستخدام HTTPS في الإنتاج لحماية البيانات الحساسة.
- اختبر الواجهات باستخدام أدوات مثل Postman أو cURL.
- رمز الوصول (JWT) يجب تضمينه في رأس الطلب كـ `Authorization: Bearer <token>` للواجهات التي تتطلب المصادقة.
- يتم تسجيل الإجراءات الإدارية (مثل تحديث أو حذف الملفات) باستخدام `AuditLogManager` لأغراض التدقيق.
- المهارات يمكن تقديمها كمصفوفة أو كسلسلة نصية مفصولة بفواصل، وسيتم معالجتها بشكل مناسب.
- لا يمكن للمستخدمين تعديل أو حذف ملفات مستخدمين آخرين، حتى لو كانوا مسؤولين.