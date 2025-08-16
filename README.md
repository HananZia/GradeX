# GradeX

**GradeX** is a lightweight web application designed to streamline **grade management** and **academic record tracking**.  
Built with a **Django REST framework backend** and a **Bootstrap-powered frontend**, GradeX provides a clean and intuitive platform for managing student grades, assessments, and related academic data.

---

## 🚀 Overview

GradeX aims to simplify the grading process for **teachers, administrators, and students**.  
It provides a backend API powered by Django REST Framework and a responsive frontend built with **HTML, CSS, JavaScript, and Bootstrap**.  
Data is stored securely in an **SQLite3 database** for easy setup and portability.

---

## ✨ Features

- 📊 **Grade Management** – Create, update, and view student grades.  
- 👨‍🎓 **Student Records** – Manage basic student data and associated grades.  
- 🔑 **User Authentication** – Secure login/logout with Django’s built-in auth system.  
- 📱 **Responsive UI** – Powered by **Bootstrap**, ensuring smooth performance across devices.  
- 🔌 **REST API** – Exposes endpoints for integrating with external systems or frontends.  
- 💾 **SQLite3 Database** – Lightweight and easy-to-configure database for local use.  
- 🛠️ **Admin Panel** – Leverages Django’s built-in admin interface for quick database management.  

---

## 🛠️ Tech Stack

### Backend
- **Python 3.x**
- **Django 4.x**
- **Django REST Framework**
- **SQLite3 Database**

### Frontend
- **HTML5**
- **CSS3**
- **JavaScript (Vanilla JS)**
- **Bootstrap 5**

### Tools & Utilities
- **Git/GitHub** – Version control & collaboration  
- **Heroku** (optional) – Deployment-ready (via `Procfile` and `runtime.txt`)  
- **Virtualenv** – Python environment management  
- **pip** – Dependency management (`requirements.txt`)  

---

## ⚙️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/HananZia/GradeX.git
cd GradeX

2. Create and Activate Virtual Environment
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Apply Database Migrations
python manage.py makemigrations
python manage.py migrate

5. Create Superuser (for Admin Panel)
python manage.py createsuperuser


➡️ You’ll be prompted to enter a username, email, and password.

6. Collect Static Files (for Bootstrap, CSS, JS)
python manage.py collectstatic

7. Run the Development Server
python manage.py runserver


By default, the app runs on:
👉 Frontend & API: http://127.0.0.1:8000/
👉 Admin Panel: http://127.0.0.1:8000/admin/

