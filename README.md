# EduConnect FrontEnd

EduConnect FrontEnd is the client-side interface for the EduConnect platform, a web application designed to facilitate educational content sharing and user interaction. This repository contains the front-end code, built with HTML, CSS, and JavaScript, and integrates with the [EduConnect BackEnd](https://github.com/MohammedBoure/EduConnect-BackEnd) for full functionality.

## Project Overview

EduConnect provides a user-friendly interface for browsing, creating, editing, and managing educational posts, as well as user authentication and messaging features. The admin panel allows for user and content management, while the public interface supports post interaction and profile management.

## Access and Testing

### Site URL
The live application can be accessed at:  
[https://educonnect-admin.onrender.com](https://educonnect-admin.onrender.com)

### Admin Interface
To access the admin interface, use the following link:  
[https://educonnect-admin.onrender.com/admin.html](https://educonnect-admin.onrender.com/admin.html)

### Test Accounts
The following accounts can be used for testing the API and admin interface (all accounts share the same password: `11111111`):  
- Carlos@gmail.com  
- Chloe@gmail.com  
- Liam@gmail.com  
- Rajesh@gmail.com  
- admin@gmail.com (designated for admin access, required for the admin interface)

### واجهة برمجة التطبيقات (API) - نظرة عامة (بالعربية)
واجهة برمجة تطبيقات EduConnect هي واجهة RESTful مبنية باستخدام إطار عمل Flask، مصممة لمنصة اجتماعية تدير المستخدمين، الملفات الشخصية، المنشورات، التعليقات، الرسائل، والمهام الإدارية. تستخدم التوثيق القائم على الجلسات وتعتمد على قاعدة بيانات SQLite (student_directory.db) لتخزين البيانات. تدعم الواجهة تسجيل المستخدمين، تسجيل الدخول، إدارة الملفات الشخصية، الرسائل، المنشورات، التعليقات، والعمليات الإدارية.

## Features
- **User Authentication**: Login, registration, and profile management.
- **Post Management**: Create, edit, view, and delete educational posts.
- **Admin Dashboard**: Manage users, posts, and messages with dedicated views.
- **Messaging System**: Real-time messaging for user communication.
- **Responsive Design**: Styled with CSS for a seamless experience across devices.

## Project Structure

The project is organized as follows:

```
EduConnect-FrontEnd/
├── src/
│   ├── admin/                    # Admin panel files
│   │   ├── css/                 # Admin-specific CSS styles
│   │   ├── js/                  # Admin-specific JavaScript (API and auth)
│   │   ├── *.html               # Admin HTML pages (e.g., admin_posts.html, admin_users.html)
│   │   ├── css_analysis_report.md # CSS analysis report
│   │   ├── recursive_directory_printer.py # Utility script for directory analysis
│   │   └── README.md            # Admin-specific documentation
│   ├── css/                     # Public-facing CSS styles
│   ├── images/                  # Static assets (e.g., MainImage.jpg)
│   ├── js/                      # Public-facing JavaScript (API and auth)
│   ├── node_modules/            # Dependencies (e.g., DOMPurify, Marked)
│   └── *.html                   # Public HTML pages (e.g., index.html, login.html)
├── CHANGELOG.md                 # Project changelog
├── LICENSE                      # License file
├── README.md                    # This file
├── commit_msg                   # Commit message template
├── commit_msgs                  # Commit message history
└── git_push.sh                  # Script for Git push automation
```

- **Total Files**: 87
- **Total Lines**: 21,073
- **Total Size**: 829.6KB
- **File Types**:
  - CSS: 21 files (5,433 lines, 107.1KB)
  - JavaScript: 12 files (8,967 lines, 425.7KB)
  - Markdown: 9 files (765 lines, 37.1KB)
  - HTML: 20 files (4,539 lines, 213.9KB)
  - Python: 1 file (82 lines, 3.4KB)
  - TypeScript: 4 files (1,287 lines, 42.5KB)

## Prerequisites

To run the project locally, ensure you have:
- A modern web browser (e.g., Chrome, Firefox)
- Node.js and npm (for managing dependencies)
- Access to the [EduConnect BackEnd](https://github.com/MohammedBoure/EduConnect-BackEnd) for API connectivity

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/EduConnect-FrontEnd.git
   cd EduConnect-FrontEnd
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```
   This will install required packages like `dompurify` and `marked` located in `node_modules/`.

3. **Set Up the Backend**:
   Follow the instructions in the [EduConnect BackEnd repository](https://github.com/MohammedBoure/EduConnect-BackEnd) to set up the server and API.

4. **Run the Application**:
   - Serve the front-end files using a local server (e.g., `live-server` or any static file server).
   ```bash
   npm install -g live-server
   live-server src/
   ```
   - Ensure the backend API is running and accessible.

## Usage

- **Public Pages**:
  - `index.html`: Homepage with post listings.
  - `login.html` / `register.html`: User authentication.
  - `post.html` / `posts.html`: View and manage posts.
  - `messenger.html`: Access the messaging system.
  - `aboutUS.html`: Information about the platform.

- **Admin Pages**:
  - `admin/index.html`: Admin dashboard.
  - `admin/admin_posts.html`: Manage posts.
  - `admin/admin_users.html`: Manage users.
  - `admin/admin_messages.html`: Manage messages.

- **Scripts**:
  - `js/api.js` and `js/auth.js`: Handle API requests and authentication logic.
  - `admin/js/api.js` and `admin/js/auth.js`: Admin-specific API and auth logic.

## Development

- **CSS Styling**:
  - Public styles are in `src/css/`.
  - Admin-specific styles are in `src/admin/css/`.
  - Shared styles are defined in `admin/css/shared_rules.css`.

- **JavaScript**:
  - API interactions are managed via `api.js`.
  - Authentication logic is in `auth.js`.

- **Dependencies**:
  - `dompurify`: Sanitizes HTML to prevent XSS attacks.
  - `marked`: Converts Markdown to HTML for rendering content.

- **Utility**:
  - `recursive_directory_printer.py`: A Python script for generating directory structure reports.

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

Please follow the `commit_msg` template for consistent commit messages.

## License

This project is licensed under the terms specified in the `LICENSE` file.

## Contact

For issues or inquiries, please open an issue on this repository or contact the maintainers via the [EduConnect BackEnd repository](https://github.com/MohammedBoure/EduConnect-BackEnd).