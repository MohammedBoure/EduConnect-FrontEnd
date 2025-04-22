# تسجيل الدخول (User Login)

## نظرة عامة
نقطة النهاية هذه تتيح للمستخدم تسجيل الدخول إلى النظام عن طريق إرسال البريد الإلكتروني وكلمة المرور عبر طلب `POST`. يتم التحقق من صحة بيانات الاعتماد، وفي حال نجاح العملية، يتم إرجاع رمز وصول (access token) ومعرف المستخدم (user ID).

## تفاصيل نقطة النهاية
- **الطريقة:** `POST`
- **الرابط:** `/api/login`
- **الوصف:** تسجيل دخول مستخدم باستخدام البريد الإلكتروني وكلمة المرور.
- **نوع المحتوى:** `application/json`

## جسم الطلب (Request Body)
يجب أن يحتوي جسم الطلب على البيانات التالية بتنسيق JSON. جميع الحقول مطلوبة.

| الحقل          | النوع   | الوصف                           | ملاحظات                       |
|-----------------|---------|---------------------------------|-------------------------------|
| `email` *       | String  | البريد الإلكتروني للمستخدم   | يجب أن يكون بريدًا صالحًا   |
| `mot_de_passe` *| String  | كلمة المرور للمستخدم         | لا يمكن أن تكون فارغة        |

### مثال على جسم الطلب
```json
{
  "email": "ahmed.benali@example.com",
  "mot_de_passe": "SecurePass123"
}
```

## الاستجابات

### استجابة ناجحة (`200 OK`)
يتم إرجاع هذه الاستجابة عند تسجيل الدخول بنجاح، مع رمز الوصول ومعرف المستخدم.

**جسم الاستجابة:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 123
}
```

### الأخطاء الشائعة
- **400 Bad Request**: يتم إرجاع هذا الخطأ إذا كان البريد الإلكتروني أو كلمة المرور مفقودة أو فارغة.
  ```json
  {
    "error": "Email and password are required"
  }
  ```
  **مثال على الطلب الذي يسبب هذا الخطأ:**
  ```json
  {
    "email": "ahmed.benali@example.com"
  }
  ```

- **401 Unauthorized**: يتم إرجاع هذا الخطأ إذا كان البريد الإلكتروني غير موجود أو كلمة المرور غير صحيحة.
  ```json
  {
    "error": "Invalid email or password"
  }
  ```

## ملاحظات إضافية
- يتم التحقق من كلمة المرور باستخدام دالة `check_password_hash`، مما يعني أن كلمة المرور المخزنة في قاعدة البيانات مشفرة (hashed).
- رمز الوصول (access token) المُرجع هو رمز JWT (JSON Web Token) يمكن استخدامه لتأمين الطلبات اللاحقة إلى نقاط نهاية محمية.
- يُنصح باستخدام HTTPS لتشفير البيانات أثناء النقل، خاصة لأن الطلب يحتوي على بيانات حساسة مثل كلمة المرور.
- إذا كنت تستخدم هذه النقطة في بيئة اختبار، تأكد من أن خادم الـ API يعمل على `http://127.0.0.1:5000` (أو العنوان المناسب).

## مثال على طلب باستخدام cURL
```bash
curl -X POST http://127.0.0.1:5000/api/login \
-H "Content-Type: application/json" \
-d '{
  "email": "ahmed.benali@example.com",
  "mot_de_passe": "SecurePass123"
}'
```

**الاستجابة المتوقعة:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 123
}
```

## مثال على طلب باستخدام JavaScript (fetch)
```javascript
const url = "http://127.0.0.1:5000/api/login";
const data = {
  email: "ahmed.benali@example.com",
  mot_de_passe: "SecurePass123"
};

fetch(url, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(data)
})
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => {
    console.log(status, body);
  })
  .catch(error => {
    console.error("Error:", error);
  });
```

**الاستجابة المتوقعة في وحدة التحكم:**
```javascript
200 {
  access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  user_id: 123
}
```