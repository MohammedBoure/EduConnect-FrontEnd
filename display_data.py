import sqlite3

# الاتصال بقاعدة البيانات
DATABASE_PATH = 'C:/Users/AES/Desktop/EduConnect/student_directory.db'
conn = sqlite3.connect(DATABASE_PATH)

# إنشاء مؤشر للعمل مع قاعدة البيانات
cursor = conn.cursor()

# دالة لعرض بيانات المستخدمين
def afficher_utilisateurs():
    cursor.execute("SELECT * FROM utilisateurs")
    utilisateurs = cursor.fetchall()
    if utilisateurs:
        for utilisateur in utilisateurs:
            print(f"ID: {utilisateur[0]}")
            print(f"الاسم: {utilisateur[1]} {utilisateur[2]}")
            print(f"البريد الإلكتروني: {utilisateur[3]}")
            print(f"التخصص: {utilisateur[4]}")
            print(f"المهارات: {utilisateur[5]}")
            print(f"الصورة: {utilisateur[6]}")
            print("-" * 40)
    else:
        print("لا يوجد مستخدمين في قاعدة البيانات.")

# دالة لعرض بيانات المنشورات
def afficher_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    if posts:
        for post in posts:
            print(f"ID: {post[0]}")
            print(f"المحتوى: {post[1]}")
            print(f"تاريخ الإنشاء: {post[2]}")
            print(f"المستخدم: {post[3]}")
            print("-" * 40)
    else:
        print("لا توجد منشورات في قاعدة البيانات.")

# دالة لعرض بيانات الرسائل
def afficher_messages():
    cursor.execute("SELECT * FROM messages")
    messages = cursor.fetchall()
    if messages:
        for message in messages:
            print(f"ID: {message[0]}")
            print(f"المحتوى: {message[1]}")
            print(f"تاريخ الإنشاء: {message[2]}")
            print(f"المرسل: {message[3]}")
            print(f"المستقبل: {message[4]}")
            print("-" * 40)
    else:
        print("لا توجد رسائل في قاعدة البيانات.")

# استدعاء الوظائف لعرض البيانات
if __name__ == '__main__':
    print("عرض بيانات المستخدمين:")
    afficher_utilisateurs()
    
    print("\nعرض بيانات المنشورات:")
    afficher_posts()
    
    print("\nعرض بيانات الرسائل:")
    afficher_messages()

# إغلاق الاتصال بقاعدة البيانات
conn.close()
