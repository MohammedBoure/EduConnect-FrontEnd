# توثيق واجهة برمجة التطبيقات (API) لمنصة اجتماعية

## نظرة عامة
هذه الواجهة البرمجية (API) تتيح إدارة المستخدمين، الملفات الشخصية، الرسائل، المنشورات، والتعليقات في منصة اجتماعية. يعتمد التطبيق على **Flask** مع مصادقة باستخدام **JWT (JSON Web Token)**. يتم تشفير كلمات المرور وتخزينها في قاعدة بيانات، وتدعم الواجهة عمليات التسجيل، تسجيل الدخول، تحديث الملفات، البحث، إرسال الرسائل، وإدارة المنشورات والتعليقات.

## المتطلبات الأساسية
- **الخادم**: يعمل على `http://127.0.0.1:5000` في بيئة الاختبار.
- **المصادقة**: تتطلب معظم نقاط النهاية رمز وصول JWT يتم إرساله في رأس الطلب كـ `Authorization: Bearer <token>`.
- **نوع المحتوى**: `application/json` لجميع الطلبات التي تحتوي على جسم.
- **HTTPS**: يُوصى باستخدامه في الإنتاج لحماية البيانات الحساسة.

## نقاط النهاية (Endpoints)

### 1. تسجيل مستخدم جديد (User Registration)
- **الطريقة**: `POST`
- **الرابط**: `/api/register`
- **الوصف**: تسجيل مستخدم جديد بإدخال بيانات مثل الاسم، البريد الإلكتروني، وكلمة المرور.
- **المصادقة**: غير مطلوبة.

#### جسم الطلب
| الحقل           | النوع           | الوصف                                     | ملاحظات                           |
|------------------|-----------------|-------------------------------------------|-----------------------------------|
| `nom` *          | String          | الاسم الأخير                            | لا يمكن أن يكون فارغًا           |
| `prenom` *       | String          | الاسم الأول                             | لا يمكن أن يكون فارغًا           |
| `email` *        | String          | البريد الإلكتروني                       | يجب أن يكون صالحًا وفريدًا      |
| `mot_de_passe` * | String          | كلمة المرور                             | يُفضل أن تكون قوية (8 أحرف على الأقل) |
| `filiere` *      | String          | التخصص الدراسي                          | لا يمكن أن يكون فارغًا           |
| `competences` *  | Array/String    | قائمة المهارات (مثل ["Python"])         | يمكن أن تكون سلسلة مفصولة بفواصل |
| `photo`          | String          | رابط الصورة الشخصية (اختياري)          | يمكن أن يكون فارغًا              |

**مثال**:
```json
{
  "nom": "Benali",
  "prenom": "Ahmed",
  "email": "ahmed.benali@example.com",
  "mot_de_passe": "SecurePass123",
  "filiere": "Informatique",
  "competences": ["Python", "JavaScript"],
  "photo": "https://example.com/photos/ahmed.jpg"
}
```

#### الاستجابات
- **201 Created**:
  ```json
  {
    "message": "User registered successfully",
    "user": {
      "id": 123,
      "nom": "Benali",
      "prenom": "Ahmed",
      "email": "ahmed.benali@example.com"
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "All fields are required and cannot be empty"}
  ```
- **409 Conflict**:
  ```json
  {"error": "Email already exists"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Database error during registration"}
  ```

#### مثال باستخدام cURL
```bash
curl -X POST http://127.0.0.1:5000/api/register \
-H "Content-Type: application/json" \
-d '{"nom":"Benali","prenom":"Ahmed","email":"ahmed.benali@example.com","mot_de_passe":"SecurePass123","filiere":"Informatique","competences":["Python","JavaScript"],"photo":"https://example.com/photos/ahmed.jpg"}'
```

#### مثال باستخدام JavaScript (fetch)
```javascript
const url = "http://127.0.0.1:5000/api/register";
const data = {
  nom: "Benali",
  prenom: "Ahmed",
  email: "ahmed.benali@example.com",
  mot_de_passe: "SecurePass123",
  filiere: "Informatique",
  competences: ["Python", "JavaScript"],
  photo: "https://example.com/photos/ahmed.jpg"
};

fetch(url, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(data)
})
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => console.log(status, body))
  .catch(error => console.error("Error:", error));
```

---

### 2. تسجيل الدخول (User Login)
- **الطريقة**: `POST`
- **الرابط**: `/api/login`
- **الوصف**: تسجيل دخول المستخدم باستخدام البريد الإلكتروني وكلمة المرور للحصول على رمز وصول JWT.
- **المصادقة**: غير مطلوبة.

#### جسم الطلب
| الحقل           | النوع   | الوصف                           | ملاحظات                       |
|------------------|---------|---------------------------------|-------------------------------|
| `email` *        | String  | البريد الإلكتروني             | يجب أن يكون صالحًا           |
| `mot_de_passe` * | String  | كلمة المرور                   | لا يمكن أن تكون فارغة        |

**مثال**:
```json
{
  "email": "ahmed.benali@example.com",
  "mot_de_passe": "SecurePass123"
}
```

#### الاستجابات
- **200 OK**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user_id": 123
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "Email and password are required"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid email or password"}
  ```

#### مثال باستخدام cURL
```bash
curl -X POST http://127.0.0.1:5000/api/login \
-H "Content-Type: application/json" \
-d '{"email":"ahmed.benali@example.com","mot_de_passe":"SecurePass123"}'
```

#### مثال باستخدام JavaScript (fetch)
```javascript
const url = "http://127.0.0.1:5000/api/login";
const data = {
  email: "ahmed.benali@example.com",
  mot_de_passe: "SecurePass123"
};

fetch(url, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(data)
})
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => console.log(status, body))
  .catch(error => console.error("Error:", error));
```

---

### 3. استرجاع ملف المستخدم (Get User Profile)
- **الطريقة**: `GET`
- **الرابط**: `/api/profile/<user_id>`
- **الوصف**: استرجاع بيانات ملف المستخدم بناءً على معرف المستخدم.
- **المصادقة**: غير مطلوبة (عامة).

#### معلمات المسار
| المعلم     | النوع   | الوصف                  | ملاحظات                     |
|------------|---------|------------------------|-----------------------------|
| `user_id` *| Integer | معرف المستخدم         | يجب أن يكون رقمًا صحيحًا   |

#### الاستجابات
- **200 OK**:
  ```json
  {
    "id": 123,
    "nom": "Benali",
    "prenom": "Ahmed",
    "email": "ahmed.benali@example.com",
    "filiere": "Informatique",
    "competences": ["Python", "JavaScript"],
    "photo": "https://example.com/photos/ahmed.jpg"
  }
  ```
- **404 Not Found**:
  ```json
  {"error": "User not found"}
  ```

#### مثال باستخدام cURL
```bash
curl -X GET http://127.0.0.1:5000/api/profile/123
```

#### مثال باستخدام JavaScript (fetch)
```javascript
const userId = 123;
const url = `http://127.0.0.1:5000/api/profile/${userId}`;

fetch(url, {
  method: "GET",
  headers: { "Content-Type": "application/json" }
})
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => console.log(status, body))
  .catch(error => console.error("Error:", error));
```

---

### 4. تحديث ملف المستخدم (Update User Profile)
- **الطريقة**: `PUT`
- **الرابط**: `/api/profile/<user_id>`
- **الوصف**: تحديث بيانات ملف المستخدم (مثل الاسم، التخصص، أو المهارات).
- **المصادقة**: مطلوبة (JWT). يمكن للمستخدم تحديث ملفه الشخصي فقط.

#### معلمات المسار
| المعلم     | النوع   | الوصف                  | ملاحظات                     |
|------------|---------|------------------------|-----------------------------|
| `user_id` *| Integer | معرف المستخدم         | يجب أن يكون رقمًا صحيحًا   |

#### جسم الطلب
| الحقل         | النوع           | الوصف                           | ملاحظات                     |
|----------------|-----------------|---------------------------------|-----------------------------|
| `nom`          | String          | الاسم الأخير (اختياري)        |                             |
| `prenom`       | String          | الاسم الأول (اختياري)         |                             |
| `filiere`      | String          | التخصص الدراسي (اختياري)      |                             |
| `competences`  | Array/String    | قائمة المهارات (اختياري)      | يمكن أن تكون سلسلة مفصولة |
| `photo`        | String          | رابط الصورة (اختياري)         |                             |

**مثال**:
```json
{
  "nom": "Benali",
  "prenom": "Ahmed",
  "filiere": "Informatique",
  "competences": ["Python", "Java"],
  "photo": "https://example.com/photos/new_ahmed.jpg"
}
```

#### الاستجابات
- **200 OK**:
  ```json
  {
    "message": "Profile updated successfully",
    "user": {
      "id": 123,
      "nom": "Benali",
      "prenom": "Ahmed",
      "filiere": "Informatique",
      "competences": ["Python", "Java"],
      "photo": "https://example.com/photos/new_ahmed.jpg"
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "No update data provided"}
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
  {"error": "An error occurred during profile update"}
  ```

#### مثال باستخدام cURL
```bash
curl -X PUT http://127.0.0.1:5000/api/profile/123 \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_jwt_token>" \
-d '{"nom":"Benali","prenom":"Ahmed","filiere":"Informatique","competences":["Python","Java"],"photo":"https://example.com/photos/new_ahmed.jpg"}'
```

#### مثال باستخدام JavaScript (fetch)
```javascript
const userId = 123;
const url = `http://127.0.0.1:5000/api/profile/${userId}`;
const token = "<your_jwt_token>";
const data = {
  nom: "Benali",
  prenom: "Ahmed",
  filiere: "Informatique",
  competences: ["Python", "Java"],
  photo: "https://example.com/photos/new_ahmed.jpg"
};

fetch(url, {
  method: "PUT",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify(data)
})
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => console.log(status, body))
  .catch(error => console.error("Error:", error));
```

---

### 5. حذف ملف المستخدم (Delete User Profile)
- **الطريقة**: `DELETE`
- **الرابط**: `/api/profile/<user_id>`
- **الوصف**: حذف ملف المستخدم بناءً على معرف المستخدم.
- **المصادقة**: مطلوبة (JWT). يمكن للمستخدم حذف ملفه الشخصي فقط.

#### معلمات المسار
| المعلم     | النوع   | الوصف                  | ملاحظات                     |
|------------|---------|------------------------|-----------------------------|
| `user_id` *| Integer | معرف المستخدم         | يجب أن يكون رقمًا صحيحًا   |

#### الاستجابات
- **200 OK**:
  ```json
  {"message": "Profile deleted successfully"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **403 Forbidden**:
  ```json
  {"error": "Unauthorized: You can only delete your own profile"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "An error occurred during profile deletion or user not found"}
  ```

#### مثال باستخدام cURL
```bash
curl -X DELETE http://127.0.0.1:5000/api/profile/123 \
-H "Authorization: Bearer <your_jwt_token>"
```

#### مثال باستخدام JavaScript (fetch)
```javascript
const userId = 123;
const url = `http://127.0.0.1:5000/api/profile/${userId}`;
const token = "<your_jwt_token>";

fetch(url, {
  method: "DELETE",
  headers: { "Authorization": `Bearer ${token}` }
})
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => console.log(status, body))
  .catch(error => console.error("Error:", error));
```

---

### 6. البحث عن ملفات المستخدمين (Search Profiles)
- **الطريقة**: `GET`
- **الرابط**: `/api/search`
- **الوصف**: البحث عن ملفات المستخدمين بناءً على الاسم، التخصص، أو المهارات.
- **المصادقة**: مطلوبة (JWT).

#### معلمات الاستعلام (Query Parameters)
| المعلم       | النوع   | الوصف                           | ملاحظات                     |
|---------------|---------|---------------------------------|-----------------------------|
| `nom`         | String  | الاسم (جزئي أو كامل)          | اختياري                    |
| `filiere`     | String  | التخصص الدراسي                | اختياري                    |
| `competence`  | String  | مهارة معينة                   | اختياري                    |
| `page`        | Integer | رقم الصفحة                    | افتراضي: 1                 |
| `per_page`    | Integer | عدد النتائج لكل صفحة          | افتراضي: 10                |

#### الاستجابات
- **200 OK**:
  ```json
  {
    "results": [
      {
        "id": 124,
        "nom": "Hassan",
        "prenom": "Mohamed",
        "filiere": "Informatique",
        "competences": ["Java", "SQL"],
        "photo": "https://example.com/photos/mohamed.jpg"
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
  {"error": "Invalid token identity"}
  ```

#### مثال باستخدام cURL
```bash
curl -X GET "http://127.0.0.1:5000/api/search?nom=Hassan&filiere=Informatique&competence=Java&page=1&per_page=10" \
-H "Authorization: Bearer <your_jwt_token>"
```

#### مثال باستخدام JavaScript (fetch)
```javascript
const url = "http://127.0.0.1:5000/api/search?nom=Hassan&filiere=Informatique&competence=Java&page=1&per_page=10";
const token = "<your_jwt_token>";

fetch(url, {
  method: "GET",
  headers: { "Authorization": `Bearer ${token}` }
})
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => console.log(status, body))
  .catch(error => console.error("Error:", error));
```

---

### 7. إرسال رسالة (Send Message)
- **الطريقة**: `POST`
- **الرابط**: `/api/messages`
- **الوصف**: إرسال رسالة إلى مستخدم آخر.
- **المصادقة**: مطلوبة (JWT).

#### جسم الطلب
| الحقل         | النوع   | الوصف                           | ملاحظات                     |
|----------------|---------|---------------------------------|-----------------------------|
| `receiver_id` *| Integer | معرف المستلم                  | يجب أن يكون رقمًا صحيحًا   |
| `content` *    | String  | محتوى الرسالة                 | لا يمكن أن يكون فارغًا     |

**مثال**:
```json
{
  "receiver_id": 124,
  "content": "Hello, how are you?"
}
```

#### الاستجابات
- **201 Created**:
  ```json
  {
    "message": "Message sent successfully",
    "sent_message": {
      "id": 1,
      "content": "Hello, how are you?",
      "sender_id": 123,
      "receiver_id": 124,
      "created_at": "2025-04-21T10:00:00Z"
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "receiver_id and non-empty content are required"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Receiver user not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "An error occurred while sending the message"}
  ```

#### مثال باستخدام cURL
```bash
curl -X POST http://127.0.0.1:5000/api/messages \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_jwt_token>" \
-d '{"receiver_id":124,"content":"Hello, how are you?"}'
```

#### مثال باستخدام JavaScript (fetch)
```javascript
const url = "http://127.0.0.1:5000/api/messages";
const token = "<your_jwt_token>";
const data = {
  receiver_id: 124,
  content: "Hello, how are you?"
};

fetch(url, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify(data)
})
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => console.log(status, body))
  .catch(error => console.error("Error:", error));
```

---

### 8. استرجاع الرسائل (Get Messages)
- **الطريقة**: `GET`
- **الرابط**: `/api/messages/<other_user_id>`
- **الوصف**: استرجاع الرسائل بين المستخدم الحالي ومستخدم آخر.
- **المصادقة**: مطلوبة (JWT).

#### معلمات المسار
| المعلم          | النوع   | الوصف                           | ملاحظات                     |
|------------------|---------|---------------------------------|-----------------------------|
| `other_user_id` *| Integer | معرف المستخدم الآخر            | يجب أن يكون رقمًا صحيحًا   |

#### معلمات الاستعلام
| المعلم      | النوع   | الوصف                           | ملاحظات                     |
|-------------|---------|---------------------------------|-----------------------------|
| `page`      | Integer | رقم الصفحة                    | افتراضي: 1                 |
| `per_page`  | Integer | عدد الرسائل لكل صفحة          | افتراضي: 30                |

#### الاستجابات
- **200 OK**:
  ```json
  {
    "messages": [
      {
        "id": 1,
        "content": "Hello, how are you?",
        "sender_id": 123,
        "receiver_id": 124,
        "created_at": "2025-04-21T10:00:00Z"
      }
    ],
    "total": 1,
    "page": 1,
    "pages": 1,
    "per_page": 30
  }
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Other user not found"}
  ```

#### مثال باستخدام cURL
```bash
curl -X GET "http://127.0.0.1:5000/api/messages/124?page=1&per_page=30" \
-H "Authorization: Bearer <your_jwt_token>"
```

#### مثال باستخدام JavaScript (fetch)
```javascript
const otherUserId = 124;
const url = `http://127.0.0.1:5000/api/messages/${otherUserId}?page=1&per_page=30`;
const token = "<your_jwt_token>";

fetch(url, {
  method: "GET",
  headers: { "Authorization": `Bearer ${token}` }
})
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => console.log(status, body))
  .catch(error => console.error("Error:", error));
```

---

### 9. إنشاء منشور (Create Post)
- **الطريقة**: `POST`
- **الرابط**: `/api/posts`
- **الوصف**: إنشاء منشور جديد.
- **المصادقة**: مطلوبة (JWT).

#### جسم الطلب
| الحقل       | النوع   | الوصف                           | ملاحظات                     |
|-------------|---------|---------------------------------|-----------------------------|
| `content` * | String  | محتوى المنشور                 | لا يمكن أن يكون فارغًا     |

**مثال**:
```json
{
  "content": "This is my first post!"
}
```

#### الاستجابات
- **201 Created**:
  ```json
  {
    "message": "Post created successfully",
    "post": {
      "id": 1,
      "content": "This is my first post!",
      "created_at": "2025-04-21T10:00:00Z",
      "user_id": 123,
      "author": {
        "nom": "Benali",
        "prenom": "Ahmed"
      }
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "Post content cannot be empty"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "An error occurred while creating the post"}
  ```

#### مثال باستخدام cURL
```bash
curl -X POST http://127.0.0.1:5000/api/posts \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_jwt_token>" \
-d '{"content":"This is my first post!"}'
```

#### مثال باستخدام JavaScript (fetch)
```javascript
const url = "http://127.0.0.1:5000/api/posts";
const token = "<your_jwt_token>";
const data = {
  content: "This is my first post!"
};

fetch(url, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify(data)
})
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => console.log(status, body))
  .catch(error => console.error("Error:", error));
```

---

### 10. استرجاع منشورات المستخدم (Get User Posts)
- **الطريقة**: `GET`
- **الرابط**: `/api/posts/user/<user_id>` (مصادقة مطلوبة) أو `/api/posts/public/user/<user_id>` (عام)
- **الوصف**: استرجاع منشورات مستخدم معين.
- **المصادقة**: مطلوبة لـ `/api/posts/user/<user_id>`، غير مطلوبة لـ `/api/posts/public/user/<user_id>`.

#### معلمات المسار
| المعلم     | النوع   | الوصف                  | ملاحظات                     |
|------------|---------|------------------------|-----------------------------|
| `user_id` *| Integer | معرف المستخدم         | يجب أن يكون رقمًا صحيحًا   |

#### معلمات الاستعلام
| المعلم      | النوع   | الوصف                           | ملاحظات                     |
|-------------|---------|---------------------------------|-----------------------------|
| `page`      | Integer | رقم الصفحة                    | افتراضي: 1                 |
| `per_page`  | Integer | عدد المنشورات لكل صفحة        | افتراضي: 10                |

#### الاستجابات
- **200 OK**:
  ```json
  {
    "posts": [
      {
        "id": 1,
        "content": "This is my first post!",
        "created_at": "2025-04-21T10:00:00Z",
        "user_id": 123,
        "author": {
          "nom": "Benali",
          "prenom": "Ahmed",
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
- **401 Unauthorized** (لـ `/api/posts/user/<user_id>` فقط):
  ```json
  {"error": "Invalid token identity"}
  ```

#### مثال باستخدام cURL (عام)
```bash
curl -X GET "http://127.0.0.1:5000/api/posts/public/user/123?page=1&per_page=10"
```

#### مثال باستخدام JavaScript (fetch) (مصادقة)
```javascript
const userId = 123;
const url = `http://127.0.0.1:5000/api/posts/user/${userId}?page=1&per_page=10`;
const token = "<your_jwt_token>";

fetch(url, {
  method: "GET",
  headers: { "Authorization": `Bearer ${token}` }
})
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => console.log(status, body))
  .catch(error => console.error("Error:", error));
```

---

### 11. تحديث منشور (Update Post)
- **الطريقة**: `PUT`
- **الرابط**: `/api/posts/<post_id>`
- **الوصف**: تحديث محتوى منشور موجود.
- **المصادقة**: مطلوبة (JWT). يمكن للمستخدم تحديث منشوراته فقط.

#### معلمات المسار
| المعلم      | النوع   | الوصف                  | ملاحظات                     |
|-------------|---------|------------------------|-----------------------------|
| `post_id` * | Integer | معرف المنشور          | يجب أن يكون رقمًا صحيحًا   |

#### جسم الطلب
| الحقل       | النوع   | الوصف                           | ملاحظات                     |
|-------------|---------|---------------------------------|-----------------------------|
| `content` * | String  | محتوى المنشور المحدث          | لا يمكن أن يكون فارغًا     |

**مثال**:
```json
{
  "content": "This is my updated post!"
}
```

#### الاستجابات
- **200 OK**:
  ```json
  {
    "message": "Post updated successfully",
    "post": {
      "id": 1,
      "content": "This is my updated post!",
      "created_at": "2025-04-21T10:00:00Z",
      "user_id": 123,
      "author": {
        "nom": "Benali",
        "prenom": "Ahmed"
      }
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "Post content cannot be empty"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **403 Forbidden**:
  ```json
  {"error": "Unauthorized: You can only update your own posts"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Post not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "An error occurred while updating the post"}
  ```

#### مثال باستخدام cURL
```bash
curl -X PUT http://127.0.0.1:5000/api/posts/1 \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_jwt_token>" \
-d '{"content":"This is my updated post!"}'
```

#### مثال باستخدام JavaScript (fetch)
```javascript
const postId = 1;
const url = `http://127.0.0.1:5000/api/posts/${postId}`;
const token = "<your_jwt_token>";
const data = {
  content: "This is my updated post!"
};

fetch(url, {
  method: "PUT",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify(data)
})
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => console.log(status, body))
  .catch(error => console.error("Error:", error));
```

---

### 12. حذف منشور (Delete Post)
- **الطريقة**: `DELETE`
- **الرابط**: `/api/posts/<post_id>`
- **الوصف**: حذف منشور موجود.
- **المصادقة**: مطلوبة (JWT). يمكن للمستخدم حذف منشوراته فقط.

#### معلمات المسار
| المعلم      | النوع   | الوصف                  | ملاحظات                     |
|-------------|---------|------------------------|-----------------------------|
| `post_id` * | Integer | معرف المنشور          | يجب أن يكون رقمًا صحيحًا   |

#### الاستجابات
- **200 OK**:
  ```json
  {"message": "Post deleted successfully"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **403 Forbidden**:
  ```json
  {"error": "Unauthorized: You can only delete your own posts"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Post not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "An error occurred while deleting the post"}
  ```

#### مثال باستخدام cURL
```bash
curl -X DELETE http://127.0.0.1:5000/api/posts/1 \
-H "Authorization: Bearer <your_jwt_token>"
```

#### مثال باستخدام JavaScript (fetch)
```javascript
const postId = 1;
const url = `http://127.0.0.1:5000/api/posts/${postId}`;
const token = "<your_jwt_token>";

fetch(url, {
  method: "DELETE",
  headers: { "Authorization": `Bearer ${token}` }
})
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => console.log(status, body))
  .catch(error => console.error("Error:", error));
```

---

### 13. إضافة تعليق (Add Comment)
- **الطريقة**: `POST`
- **الرابط**: `/api/posts/<post_id>/comments`
- **الوصف**: إضافة تعليق إلى منشور.
- **المصادقة**: مطلوبة (JWT).

#### معلمات المسار
| المعلم      | النوع   | الوصف                  | ملاحظات                     |
|-------------|---------|------------------------|-----------------------------|
| `post_id` * | Integer | معرف المنشور          | يجب أن يكون رقمًا صحيحًا   |

#### جسم الطلب
| الحقل       | النوع   | الوصف                           | ملاحظات                     |
|-------------|---------|---------------------------------|-----------------------------|
| `content` * | String  | محتوى التعليق                 | لا يمكن أن يكون فارغًا     |

**مثال**:
```json
{
  "content": "Great post!"
}
```

#### الاستجابات
- **201 Created**:
  ```json
  {
    "message": "Comment added successfully",
    "comment": {
      "id": 1,
      "content": "Great post!",
      "created_at": "2025-04-21T10:00:00Z",
      "post_id": 1,
      "user_id": 123,
      "author": {
        "nom": "Benali",
        "prenom": "Ahmed",
        "photo": "https://example.com/photos/ahmed.jpg"
      }
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "Comment content cannot be empty"}
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
  {"error": "Failed to add comment"}
  ```

#### مثال باستخدام cURL
```bash
curl -X POST http://127.0.0.1:5000/api/posts/1/comments \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_jwt_token>" \
-d '{"content":"Great post!"}'
```

#### مثال باستخدام JavaScript (fetch)
```javascript
const postId = 1;
const url = `http://127.0.0.1:5000/api/posts/${postId}/comments`;
const token = "<your_jwt_token>";
const data = {
  content: "Great post!"
};

fetch(url, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify(data)
})
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => console.log(status, body))
  .catch(error => console.error("Error:", error));
```

---

### 14. استرجاع التعليقات (Get Comments)
- **الطريقة**: `GET`
- **الرابط**: `/api/posts/<post_id>/comments`
- **الوصف**: استرجاع تعليقات منشور معين.
- **المصادقة**: غير مطلوبة (عامة).

#### معلمات المسار
| المعلم      | النوع   | الوصف                  | ملاحظات                     |
|-------------|---------|------------------------|-----------------------------|
| `post_id` * | Integer | معرف المنشور          | يجب أن يكون رقمًا صحيحًا   |

#### معلمات الاستعلام
| المعلم      | النوع   | الوصف                           | ملاحظات                     |
|-------------|---------|---------------------------------|-----------------------------|
| `page`      | Integer | رقم الصفحة                    | افتراضي: 1                 |
| `per_page`  | Integer | عدد التعليقات لكل صفحة        | افتراضي: 20                |

#### الاستجابات
- **200 OK**:
  ```json
  {
    "comments": [
      {
        "id": 1,
        "content": "Great post!",
        "created_at": "2025-04-21T10:00:00Z",
        "post_id": 1,
        "user_id": 123,
        "author": {
          "nom": "Benali",
          "prenom": "Ahmed",
          "photo": "https://example.com/photos/ahmed.jpg"
        }
      }
    ],
    "total": 1,
    "page": 1,
    "pages": 1,
    "per_page": 20
  }
  ```
- **404 Not Found**:
  ```json
  {"error": "Post not found"}
  ```

#### مثال باستخدام cURL
```bash
curl -X GET "http://127.0.0.1:5000/api/posts/1/comments?page=1&per_page=20"
```

#### مثال باستخدام JavaScript (fetch)
```javascript
const postId = 1;
const url = `http://127.0.0.1:5000/api/posts/${postId}/comments?page=1&per_page=20`;

fetch(url, {
  method: "GET",
  headers: { "Content-Type": "application/json" }
})
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => console.log(status, body))
  .catch(error => console.error("Error:", error));
```

---

### 15. تحديث تعليق (Update Comment)
- **الطريقة**: `PUT`
- **الرابط**: `/api/comments/<comment_id>`
- **الوصف**: تحديث محتوى تعليق موجود.
- **المصادقة**: مطلوبة (JWT). يمكن للمستخدم تحديث تعليقاته فقط.

#### معلمات المسار
| المعلم        | النوع   | الوصف                  | ملاحظات                     |
|---------------|---------|------------------------|-----------------------------|
| `comment_id` *| Integer | معرف التعليق          | يجب أن يكون رقمًا صحيحًا   |

#### جسم الطلب
| الحقل       | النوع   | الوصف                           | ملاحظات                     |
|-------------|---------|---------------------------------|-----------------------------|
| `content` * | String  | محتوى التعليق المحدث          | لا يمكن أن يكون فارغًا     |

**مثال**:
```json
{
  "content": "Updated comment!"
}
```

#### الاستجابات
- **200 OK**:
  ```json
  {
    "message": "Comment updated successfully",
    "comment": {
      "id": 1,
      "content": "Updated comment!",
      "created_at": "2025-04-21T10:00:00Z",
      "post_id": 1,
      "user_id": 123,
      "author": {
        "nom": "Benali",
        "prenom": "Ahmed",
        "photo": "https://example.com/photos/ahmed.jpg"
      }
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "Comment content cannot be empty"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **403 Forbidden**:
  ```json
  {"error": "Unauthorized: You can only update your own comments"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Comment not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to update comment"}
  ```

#### مثال باستخدام cURL
```bash
curl -X PUT http://127.0.0.1:5000/api/comments/1 \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_jwt_token>" \
-d '{"content":"Updated comment!"}'
```

#### مثال باستخدام JavaScript (fetch)
```javascript
const commentId = 1;
const url = `http://127.0.0.1:5000/api/comments/${commentId}`;
const token = "<your_jwt_token>";
const data = {
  content: "Updated comment!"
};

fetch(url, {
  method: "PUT",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify(data)
})
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => console.log(status, body))
  .catch(error => console.error("Error:", error));
```

---

### 16. حذف تعليق (Delete Comment)
- **الطريقة**: `DELETE`
- **الرابط**: `/api/comments/<comment_id>`
- **الوصف**: حذف تعليق موجود.
- **المصادقة**: مطلوبة (JWT). يمكن للمستخدم حذف تعليقاته فقط.

#### معلمات المسار
| المعلم        | النوع   | الوصف                  | ملاحظات                     |
|---------------|---------|------------------------|-----------------------------|
| `comment_id` *| Integer | معرف التعليق          | يجب أن يكون رقمًا صحيحًا   |

#### الاستجابات
- **200 OK**:
  ```json
  {"message": "Comment deleted successfully"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **403 Forbidden**:
  ```json
  {"error": "Unauthorized: You can only delete your own comments"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Comment not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to delete comment"}
  ```

#### مثال باستخدام cURL
```bash
curl -X DELETE http://127.0.0.1:5000/api/comments/1 \
-H "Authorization: Bearer <your_jwt_token>"
```

#### مثال باستخدام JavaScript (fetch)
```javascript
const commentId = 1;
const url = `http://127.0.0.1:5000/api/comments/${commentId}`;
const token = "<your_jwt_token>";

fetch(url, {
  method: "DELETE",
  headers: { "Authorization": `Bearer ${token}` }
})
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => console.log(status, body))
  .catch(error => console.error("Error:", error));
```

---

## ملاحظات عامة
- **المصادقة**: يتم استخدام رمز JWT في رأس `Authorization: Bearer <token>` لنقاط النهاية التي تتطلب المصادقة. يتم الحصول على الرمز من نقطة `/api/login`.
- **تشفير كلمات المرور**: يتم افتراض أن كلمات المرور تُشفر (hashed) داخل دالة `create_user` باستخدام مكتبة مثل `bcrypt`.
- **تنسيق التاريخ**: يتم إرجاع التواريخ بتنسيق ISO 8601 (مثل `2025-04-21T10:00:00Z`).
- **التقسيم إلى صفحات**: تدعم نقاط النهاية التي تُرجع قوائم (مثل البحث، الرسائل، المنشورات، التعليقات) التقسيم إلى صفحات باستخدام معلمات `page` و`per_page`.
- **الأمان**:
  - يُوصى باستخدام HTTPS في الإنتاج.
  - يجب تغيير `JWT_SECRET_KEY` إلى قيمة آمنة وفريدة.
  - قد تكون هناك حاجة إلى قيود إضافية على استرجاع بيانات حساسة مثل `email`.
- **قاعدة البيانات**: تعتمد الواجهة على وحدة `database` التي تحتوي على دوال مثل `get_user_by_id`, `create_post`, إلخ. تأكد من أن هذه الدوال مُنفذة بشكل صحيح.

## كيفية التشغيل
1. تأكد من تثبيت المتطلبات:
   ```bash
   pip install flask flask-jwt-extended flask-cors
   ```
2. قم بتشغيل الخادم:
   ```bash
   python app.py
   ```
3. اختبر الواجهة باستخدام أدوات مثل `cURL`, Postman، أو تطبيقات العميل المكتوبة بلغات مثل JavaScript.