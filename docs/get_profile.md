# استرجاع ملف المستخدم (User Profile)

## نظرة عامة
نقطة النهاية هذه تتيح استرجاع بيانات ملف المستخدم بناءً على معرف المستخدم (user ID) المُمرر في عنوان الطلب. يتم إرجاع تفاصيل المستخدم مثل الاسم، البريد الإلكتروني، التخصص، والمهارات.

## تفاصيل نقطة النهاية
- **الطريقة:** `GET`
- **الرابط:** `/api/profile/<user_id>`
- **الوصف:** استرجاع بيانات ملف المستخدم باستخدام معرف المستخدم.
- **نوع المحتوى:** لا يلزم جسم طلب (لا يتم إرسال بيانات في الطلب).

## معلمات المسار (Path Parameters)
| المعلم       | النوع | الوصف                           | ملاحظات                     |
|---------------|-------|---------------------------------|-----------------------------|
| `user_id` *   | Integer | معرف المستخدم (ID)            | يجب أن يكون رقمًا صحيحًا   |

## جسم الطلب (Request Body)
- لا يلزم جسم طلب، حيث أن هذا طلب `GET`.

## الاستجابات

### استجابة ناجحة (`200 OK`)
يتم إرجاع هذه الاستجابة عند العثور على المستخدم، مع تفاصيل ملفه الشخصي.

**جسم الاستجابة:**
```json
{
  "id": 123,
  "nom": "Benali",
  "prenom": "Ahmed",
  "email": "ahmed.benali@example.com",
  "filiere": "Informatique",
  "competences": ["Python", "JavaScript", "SQL"],
  "photo": "https://example.com/photos/ahmed.jpg"
}
```

### الأخطاء الشائعة
- **404 Not Found**: يتم إرجاع هذا الخطأ إذا لم يتم العثور على مستخدم بمعرف المستخدم المحدد.
  ```json
  {
    "error": "User not found"
  }
  ```

## ملاحظات إضافية
- حقل `competences` يتم إرجاعه كقائمة من المهارات، حيث يتم تقسيم السلسلة النصية المخزنة في قاعدة البيانات (مثل `"Python,JavaScript,SQL"`) إلى قائمة، مع إزالة أي عناصر فارغة.
- حقل `photo` قد يكون `null` أو سلسلة نصية تحتوي على رابط الصورة، حسب ما تم تخزينه عند تسجيل المستخدم.
- يُنصح بالتفكير فيما إذا كان يجب إرجاع حقل `email` علنًا، حيث أنه قد يحتوي على معلومات حساسة. يمكن تقييد الوصول إليه بناءً على سياسات الأمان.
- قد تتطلب هذه النقطة مصادقة (مثل إرسال رمز وصول JWT) في بيئة الإنتاج لتقييد الوصول إلى بيانات المستخدم.
- إذا كنت تستخدم هذه النقطة في بيئة اختبار، تأكد من أن خادم الـ API يعمل على `http://127.0.0.1:5000` (أو العنوان المناسب).

## مثال على طلب باستخدام cURL
```bash
curl -X GET http://127.0.0.1:5000/api/profile/123
```

**الاستجابة المتوقعة:**
```json
{
  "id": 123,
  "nom": "Benali",
  "prenom": "Ahmed",
  "email": "ahmed.benali@example.com",
  "filiere": "Informatique",
  "competences": ["Python", "JavaScript", "SQL"],
  "photo": "https://example.com/photos/ahmed.jpg"
}
```

## مثال على طلب باستخدام JavaScript (fetch)
```javascript
const userId = 123;
const url = `http://127.0.0.1:5000/api/profile/${userId}`;

fetch(url, {
  method: "GET",
  headers: {
    "Content-Type": "application/json"
  }
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
  id: 123,
  nom: "Benali",
  prenom: "Ahmed",
  email: "ahmed.benali@example.com",
  filiere: "Informatique",
  competences: ["Python", "JavaScript", "SQL"],
  photo: "https://example.com/photos/ahmed.jpg"
}
```