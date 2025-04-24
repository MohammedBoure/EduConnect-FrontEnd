# وثائق واجهات برمجة التطبيقات للرسائل (Messages APIs)

## رابط الخادم
`https://educonnect-wp9t.onrender.com`  
استبدل هذا المسار بـ `http://127.0.0.1:5000` إذا كنت تعمل في بيئة الاختبار.

## نظرة عامة
تتيح واجهات الرسائل إرسال الرسائل بين المستخدمين واسترجاع الرسائل المتبادلة بين مستخدمين مع دعم التصفح (pagination).

## المتطلبات الأساسية
- **الخادم**: يعمل على `https://educonnect-wp9t.onrender.com` في الإنتاج.
- **المصادقة**: مطلوبة (JWT) لجميع النقاط النهائية.
- **نوع المحتوى**: `application/json` للطلبات التي تحتوي على جسم.
- **HTTPS**: يُوصى به في الإنتاج لحماية البيانات الحساسة.

## نقاط النهاية (Endpoints)

### 1. إرسال رسالة
- **الطريقة**: `POST`
- **الرابط**: `/api/messages`
- **الوصف**: إرسال رسالة جديدة من مستخدم إلى مستخدم آخر.
- **المصادقة**: مطلوبة (JWT).

#### جسم الطلب
| الحقل          | النوع   | الوصف                     | ملاحظات                     |
|----------------|---------|---------------------------|-----------------------------|
| `sender_id` *  | Integer | معرف المرسل              | رقم صحيح، يجب أن يكون معرف المستخدم الحالي |
| `receiver_id` *| Integer | معرف المستقبل            | رقم صحيح، لا يمكن أن يكون نفس معرف المرسل |
| `content` *    | String  | محتوى الرسالة            | لا يمكن أن يكون فارغًا      |

**مثال**:
```json
{
  "sender_id": 1,
  "receiver_id": 2,
  "content": "Hello! How are you?"
}
```

#### الاستجابات
- **201 Created**:
  ```json
  {
    "message": "Message sent successfully",
    "sent_message": {
      "id": 1,
      "content": "Hello! How are you?",
      "sender_id": 1,
      "receiver_id": 2,
      "created_at": "2025-04-24T10:00:00Z"
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "Sender ID, receiver ID, and non-empty content are required"}
  ```
- **400 Bad Request**:
  ```json
  {"error": "Invalid sender_id or receiver_id format"}
  ```
- **400 Bad Request**:
  ```json
  {"error": "Cannot send messages to yourself"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Receiver not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to send message"}
  ```

#### مثال JavaScript (Frontend):
```javascript
async function sendMessage(messageData, token) {
  try {
    const response = await fetch('https://educonnect-wp9t.onrender.com/api/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(messageData),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to send message');
    }
    console.log('Message sent:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// استخدام الدالة
const messageData = {
  sender_id: 1,
  receiver_id: 2,
  content: 'Hello! How are you?',
};
const jwtToken = 'your_jwt_token_here';

sendMessage(messageData, jwtToken)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 2. استرجاع الرسائل
- **الطريقة**: `GET`
- **الرابط**: `/api/messages/<other_user_id>`
- **الوصف**: استرجاع الرسائل المتبادلة بين المستخدم الحالي ومستخدم آخر مع دعم التصفح.
- **المصادقة**: مطلوبة (JWT).

#### معلمات المسار
| المعلم         | النوع   | الوصف                     | ملاحظات          |
|----------------|---------|---------------------------|--------------------|
| `other_user_id` * | Integer | معرف المستخدم الآخر     | رقم صحيح         |

#### جسم الطلب
| الحقل       | النوع   | الوصف                     | ملاحظات          |
|-------------|---------|---------------------------|--------------------|
| `user_id` * | Integer | معرف المستخدم الحالي     | رقم صحيح         |

#### معلمات الاستعلام
| المعلمة    | النوع   | الوصف                    | الافتراضي |
|-------------|---------|--------------------------|-----------|
| `page`      | Integer | رقم الصفحة              | 1         |
| `per_page`  | Integer | عدد الرسائل لكل صفحة    | 30        |

**مثال جسم الطلب**:
```json
{
  "user_id": 1
}
```

#### الاستجابات
- **200 OK**:
  ```json
  {
    "messages": [
      {
        "id": 1,
        "content": "Hello! How are you?",
        "sender_id": 1,
        "receiver_id": 2,
        "created_at": "2025-04-24T10:00:00Z"
      },
      {
        "id": 2,
        "content": "I'm good, thanks!",
        "sender_id": 2,
        "receiver_id": 1,
        "created_at": "2025-04-24T10:01:00Z"
      }
    ],
    "total": 2,
    "page": 1,
    "pages": 1,
    "per_page": 30
  }
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Missing user_id"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Other user not found"}
  ```

#### مثال JavaScript (Frontend):
```javascript
async function getMessages(otherUserId, userId, token, page = 1, perPage = 30) {
  try {
    const response = await fetch(
      `https://educonnect-wp9t.onrender.com/api/messages/${otherUserId}?page=${page}&per_page=${perPage}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ user_id: userId }),
      }
    );

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to retrieve messages');
    }
    console.log('Messages retrieved:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// استخدام الدالة
const otherUserId = 2;
const userId = 1;
const jwtToken = 'your_jwt_token_here';

getMessages(otherUserId, userId, jwtToken)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## ملاحظات عامة
- يُوصى باستخدام HTTPS في الإنتاج لحماية البيانات الحساسة.
- اختبر الواجهات باستخدام أدوات مثل Postman أو cURL.
- رمز الوصول (JWT) يجب تضمينه في رأس الطلب كـ `Authorization: Bearer <token>` لجميع الواجهات.
- يتم تسجيل الإجراءات الإدارية باستخدام `AuditLogManager` لأغراض التدقيق.
- الرسائل يتم استرجاعها بترتيب عكسي (الأحدث أولاً) لتحسين تجربة المستخدم.