# وثائق واجهات برمجة التطبيقات للتعليقات (Comments APIs)

## رابط الخادم
`https://educonnect-wp9t.onrender.com`  
استبدل هذا المسار بـ `http://127.0.0.1:5000` إذا كنت تعمل في بيئة الاختبار.

## نظرة عامة
تتيح واجهات التعليقات إضافة، استرجاع، تحديث، وحذف التعليقات على المنشورات.

## المتطلبات الأساسية
- **الخادم**: يعمل على `https://educonnect-wp9t.onrender.com` في الإنتاج.
- **المصادقة**: مطلوبة (JWT) لإضافة، تحديث، وحذف التعليقات.
- **نوع المحتوى**: `application/json` للطلبات التي تحتوي على جسم.
- **HTTPS**: يُوصى به في الإنتاج لحماية البيانات الحساسة.

## نقاط النهاية (Endpoints)

### 1. إضافة تعليق
- **الطريقة**: `POST`
- **الرابط**: `/api/posts/<post_id>/comments`
- **الوصف**: إضافة تعليق إلى منشور.
- **المصادقة**: مطلوبة (JWT).

#### معلمات المسار
| المعلم      | النوع   | الوصف                  | ملاحظات          |
|-------------|---------|------------------------|--------------------|
| `post_id` * | Integer | معرف المنشور          | رقم صحيح         |

#### جسم الطلب
| الحقل         | النوع   | الوصف                  | ملاحظات          |
|---------------|---------|------------------------|--------------------|
| `content` *   | String  | محتوى التعليق         | لا يمكن أن يكون فارغًا |
| `created_at` *| String  | تاريخ ووقت الإنشاء    | تنسيق ISO (مثال: "2025-04-21T10:00:00Z") |

**مثال**:
```json
{
  "content": "Great post!",
  "created_at": "2025-04-21T10:00:00Z"
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
      "user_id": 0
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "Missing content or created_at field"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to create comment"}
  ```

### 2. استرجاع التعليقات
- **الطريقة**: `GET`
- **الرابط**: `/api/posts/<post_id>/comments`
- **الوصف**: استرجاع تعليقات منشور.
- **المصادقة**: غير مطلوبة.

#### معلمات المسار
| المعلم      | النوع   | الوصف                  | ملاحظات          |
|-------------|---------|------------------------|--------------------|
| `post_id` * | Integer | معرف المنشور          | رقم صحيح         |

#### معلمات الاستعلام
| المعلمة    | النوع   | الوصف                    | الافتراضي |
|-------------|---------|--------------------------|-----------|
| `page`      | Integer | رقم الصفحة              | 1         |
| `per_page`  | Integer | عدد التعليقات لكل صفحة | 20        |

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
        "user_id": 0,
        "author": {
          "first_name": "Admin",
          "last_name": "User",
          "photo": null
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

### 3. تحديث تعليق
- **الطريقة**: `PUT`
- **الرابط**: `/api/comments/<comment_id>`
- **الوصف**: تحديث محتوى تعليق.
- **المصادقة**: مطلوبة (JWT).

#### معلمات المسار
| المعلم        | النوع   | الوصف                  | ملاحظات          |
|---------------|---------|------------------------|--------------------|
| `comment_id` *| Integer | معرف التعليق          | رقم صحيح         |

#### جسم الطلب
| الحقل       | النوع   | الوصف                  | ملاحظات          |
|-------------|---------|------------------------|--------------------|
| `content` * | String  | محتوى التعليق المحدث  | لا يمكن أن يكون فارغًا |

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
      "user_id": 0,
      "author": {
        "first_name": "Admin",
        "last_name": "User",
        "photo": null
      }
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "Comment content cannot be empty"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Comment not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to update comment"}
  ```

### 4. حذف تعليق
- **الطريقة**: `DELETE`
- **الرابط**: `/api/comments/<comment_id>`
- **الوصف**: حذف تعليق.
- **المصادقة**: مطلوبة (JWT).

#### معلمات المسار
| المعلم        | النوع   | الوصف                  | ملاحظات          |
|---------------|---------|------------------------|--------------------|
| `comment_id` *| Integer | معرف التعليق          | رقم صحيح         |

#### الاستجابات
- **200 OK**:
  ```json
  {"message": "Comment deleted successfully"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Comment not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to delete comment"}
  ```

## ملاحظات عامة
- يُوصى باستخدام HTTPS في الإنتاج.
- اختبر الواجهات باستخدام أدوات مثل Postman أو cURL.
- يتم تسجيل جميع الإجراءات الإدارية (مثل تحديث أو حذف التعليقات) باستخدام `AuditLogManager` لأغراض التدقيق.