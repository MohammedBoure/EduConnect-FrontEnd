# وثائق واجهات برمجة التطبيقات للمصادقة (Authentication APIs)

## رابط الخادم
`https://educonnect-wp9t.onrender.com`  
استبدل هذا المسار بـ `http://127.0.0.1:5000` إذا كنت تعمل في بيئة الاختبار.

## نظرة عامة
تتيح واجهات المصادقة تسجيل المستخدمين الجدد وتسجيل الدخول للحصول على رمز الوصول (JWT).

## المتطلبات الأساسية
- **الخادم**: يعمل على `https://educonnect-wp9t.onrender.com` في الإنتاج.
- **المصادقة**: غير مطلوبة لهذه الواجهات (تسجيل وتسجيل دخول).
- **نوع المحتوى**: `application/json` للطلبات التي تحتوي على جسم.
- **HTTPS**: يُوصى به في الإنتاج لحماية البيانات الحساسة.

## نقاط النهاية (Endpoints)

### 1. تسجيل مستخدم جديد
- **الطريقة**: `POST`
- **الرابط**: `/api/register`
- **الوصف**: إنشاء حساب مستخدم جديد.
- **المصادقة**: غير مطلوبة.

#### جسم الطلب
| الحقل          | النوع   | الوصف                     | ملاحظات                     |
|----------------|---------|---------------------------|-----------------------------|
| `first_name` * | String  | الاسم الأول              | لا يمكن أن يكون فارغًا      |
| `last_name` *  | String  | الاسم الأخير             | لا يمكن أن يكون فارغًا      |
| `email` *      | String  | البريد الإلكتروني        | يجب أن يكون فريدًا         |
| `password` *   | String  | كلمة المرور              | لا تقل عن 8 أحرف           |
| `department` * | String  | القسم/التخصص             | لا يمكن أن يكون فارغًا      |
| `skills` *     | String  | المهارات                 | لا يمكن أن يكون فارغًا      |
| `photo`        | String  | رابط صورة الملف الشخصي   | اختياري                   |

**مثال**:
```json
{
  "first_name": "Ahmed",
  "last_name": "Benali",
  "email": "ahmed.benali@example.com",
  "password": "securepassword123",
  "department": "Computer Science",
  "skills": "Python, JavaScript",
  "photo": "https://example.com/photos/ahmed.jpg"
}
```

#### الاستجابات
- **201 Created**:
  ```json
  {
    "message": "User registered successfully",
    "user": {
      "id": 1,
      "first_name": "Ahmed",
      "last_name": "Benali",
      "email": "ahmed.benali@example.com"
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "All fields are required and cannot be empty"}
  ```
- **400 Bad Request**:
  ```json
  {"error": "Password must be at least 8 characters long"}
  ```
- **409 Conflict**:
  ```json
  {"error": "Email already exists"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Database error during registration"}
  ```

#### مثال JavaScript (Frontend):
```javascript
async function registerUser(userData) {
  try {
    const response = await fetch('https://educonnect-wp9t.onrender.com/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Registration failed');
    }
    console.log('Registration successful:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// استخدام الدالة
const userData = {
  first_name: 'Ahmed',
  last_name: 'Benali',
  email: 'ahmed.benali@example.com',
  password: 'securepassword123',
  department: 'Computer Science',
  skills: 'Python, JavaScript',
  photo: 'https://example.com/photos/ahmed.jpg',
};

registerUser(userData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 2. تسجيل الدخول
- **الطريقة**: `POST`
- **الرابط**: `/api/login`
- **الوصف**: تسجيل دخول المستخدم والحصول على رمز الوصول (JWT).
- **المصادقة**: غير مطلوبة.

#### جسم الطلب
| الحقل        | النوع   | الوصف                     | ملاحظات                     |
|--------------|---------|---------------------------|-----------------------------|
| `email` *    | String  | البريد الإلكتروني        | لا يمكن أن يكون فارغًا      |
| `password` * | String  | كلمة المرور              | لا يمكن أن يكون فارغًا      |

**مثال**:
```json
{
  "email": "ahmed.benali@example.com",
  "password": "securepassword123"
}
```

#### الاستجابات
- **200 OK**:
  ```json
  {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user_id": 1
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

#### مثال JavaScript (Frontend):
```javascript
async function loginUser(credentials) {
  try {
    const response = await fetch('https://educonnect-wp9t.onrender.com/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Login failed');
    }
    // تخزين التوكن في localStorage أو مكان آخر
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('user_id', data.user_id);
    console.log('Login successful:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// استخدام الدالة
const credentials = {
  email: 'ahmed.benali@example.com',
  password: 'securepassword123',
};

loginUser(credentials)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## ملاحظات عامة
- يُوصى باستخدام HTTPS في الإنتاج لحماية البيانات الحساسة.
- اختبر الواجهات باستخدام أدوات مثل Postman أو cURL.
- رمز الوصول (JWT) يجب تضمينه في رأس الطلب كـ `Authorization: Bearer <token>` للواجهات التي تتطلب المصادقة.
- لتحسين الأمان، قم بتخزين رمز الوصول في مكان آمن (مثل HttpOnly cookies) بدلاً من localStorage في بيئة الإنتاج.