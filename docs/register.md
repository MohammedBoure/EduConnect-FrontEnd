# تسجيل مستخدم جديد (User Registration)

## نظرة عامة
نقطة النهاية هذه تتيح تسجيل مستخدم جديد في النظام عن طريق إرسال بيانات المستخدم عبر طلب `POST`. يتم التحقق من صحة البيانات، بما في ذلك التحقق من عدم وجود البريد الإلكتروني مسبقًا، قبل إنشاء حساب المستخدم.

## تفاصيل نقطة النهاية
- **الطريقة:** `POST`
- **الرابط:** `/api/register`
- **الوصف:** تسجيل مستخدم جديد باستخدام بيانات مثل الاسم، البريد الإلكتروني، وكلمة المرور.
- **نوع المحتوى:** `application/json`

## جسم الطلب (Request Body)
يجب أن يحتوي جسم الطلب على البيانات التالية بتنسيق JSON. الحقول المميزة بـ (*) مطلوبة.

| الحقل          | النوع           | الوصف                                      | ملاحظات                           |
|-----------------|-----------------|--------------------------------------------|-----------------------------------|
| `nom` *         | String          | الاسم الأخير للمستخدم                   | لا يمكن أن يكون فارغًا           |
| `prenom` *      | String          | الاسم الأول للمستخدم                    | لا يمكن أن يكون فارغًا           |
| `email` *       | String          | البريد الإلكتروني للمستخدم              | يجب أن يكون بريدًا صالحًا وفريدًا |
| `mot_de_passe` *| String          | كلمة المرور للمستخدم                    | يُفضل أن تكون قوية (8 أحرف على الأقل) |
| `filiere` *     | String          | التخصص الدراسي للمستخدم                 | لا يمكن أن يكون فارغًا           |
| `competences` * | Array of Strings| قائمة بالمهارات (مثل "Python", "Java")   | يمكن أن تكون سلسلة نصية مفصولة بفواصل |
| `photo`         | String          | رابط الصورة الشخصية (اختياري)           | يمكن أن يكون فارغًا أو غائبًا     |

### مثال على جسم الطلب
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

#### ملاحظة حول `competences`
- يمكن إرسال `competences` كقائمة (مثل `["Python", "Java"]`) أو كسلسلة نصية مفصولة بفواصل (مثل `"Python,Java"`).
- إذا تم إرسال قائمة، سيتم تحويلها إلى سلسلة مفصولة بفواصل (بدون مسافات، مثل `"Python,Java"`) في قاعدة البيانات.

## الاستجابات

### استجابة ناجحة (`201 Created`)
يتم إرجاع هذه الاستجابة عند تسجيل المستخدم بنجاح.

**جسم الاستجابة:**
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

### الأخطاء الشائعة
- **400 Bad Request**: يتم إرجاع هذا الخطأ إذا كانت هناك حقول مطلوبة مفقودة أو فارغة.
  ```json
  {
    "error": "All fields are required and cannot be empty"
  }
  ```
  **مثال على الطلب الذي يسبب هذا الخطأ:**
  ```json
  {
    "nom": "",
    "prenom": "Ahmed",
    "email": "ahmed.benali@example.com",
    "mot_de_passe": "SecurePass123",
    "filiere": "Informatique",
    "competences": []
  }
  ```

- **409 Conflict**: يتم إرجاع هذا الخطأ إذا كان البريد الإلكتروني موجودًا بالفعل في قاعدة البيانات.
  ```json
  {
    "error": "Email already exists"
  }
  ```

- **500 Internal Server Error**: يتم إرجاع هذا الخطأ إذا حدث خطأ داخلي أثناء التسجيل (مثل مشكلة في قاعدة البيانات).
  ```json
  {
    "error": "Database error during registration"
  }
  ```

## ملاحظات إضافية
- يتم افتراض أن كلمة المرور يتم تشفيرها (hashing) داخل دالة `create_user` في قاعدة البيانات.
- يُنصح باستخدام HTTPS لتشفير البيانات أثناء النقل.
- يُفضل التحقق من تنسيق البريد الإلكتروني على مستوى العميل قبل إرسال الطلب.
- إذا كنت تستخدم هذه النقطة في بيئة اختبار، تأكد من أن خادم الـ API يعمل على `http://127.0.0.1:5000` (أو العنوان المناسب).

## مثال على طلب باستخدام cURL
```bash
curl -X POST http://127.0.0.1:5000/api/register \
-H "Content-Type: application/json" \
-d '{
  "nom": "Benali",
  "prenom": "Ahmed",
  "email": "ahmed.benali@example.com",
  "mot_de_passe": "SecurePass123",
  "filiere": "Informatique",
  "competences": ["Python", "JavaScript"],
  "photo": "https://example.com/photos/ahmed.jpg"
}'
```

**الاستجابة المتوقعة:**
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

## مثال على طلب باستخدام JavaScript (fetch)
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
201 {
  message: "User registered successfully",
  user: {
    id: 123,
    nom: "Benali",
    prenom: "Ahmed",
    email: "ahmed.benali@example.com"
  }
}
```