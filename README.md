# Smart Curriculum Activity & Attendance App (SIH25011)

A backend-focused attendance management system built with **Django + Django REST Framework**.
Built as an MVP for SIH 2025 (Government of Punjab — Smart Education theme).

## Features
- **Role-based auth**: Separate signup/login flow for Students and Teachers
- **Attendance marking**: Teacher creates a class session, marks Present/Absent for each student
- **Student dashboard**: View attendance history + live attendance percentage
- **Teacher dashboard**: View recent sessions, generate per-session reports
- **REST API**: Full CRUD via Django REST Framework
- **JWT Authentication**: Secure token-based API access (`djangorestframework-simplejwt`)
- **Django Admin**: Manage all data (students, teachers, sessions, attendance) from `/admin/`

## Tech Stack
- Python 3 + Django 6
- Django REST Framework
- SQLite (default, easy to switch to PostgreSQL)
- JWT auth (SimpleJWT)

## Project Structure
```
attendance_system/
├── attendance_system/       # Project settings, root urls
├── core/                    # Main app
│   ├── models.py            # Teacher, Student, ClassSession, Attendance
│   ├── views.py             # Web views (login, dashboards, attendance)
│   ├── forms.py             # Signup + attendance forms
│   ├── serializers.py       # DRF serializers
│   ├── api_views.py         # DRF ViewSets (REST API)
│   ├── admin.py             # Django admin registration
│   ├── urls.py               # App-level URLs (web + API)
│   └── templates/core/      # HTML templates
├── manage.py
└── requirements.txt
```

## Setup Instructions (Run Locally)

1. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (for admin panel access)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the server**
   ```bash
   python manage.py runserver
   ```

6. **Open in browser**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## How to Use

1. Go to `/signup/` → choose **Teacher** or **Student** → fill the form.
2. **Teacher** logs in → clicks "Start New Attendance Session" → enters class name (e.g. `BCA-3A`) and subject.
3. Teacher is redirected to the mark-attendance page → sees all students whose `class_name` matches → marks Present/Absent → saves.
4. **Student** (with matching `class_name`) logs in → sees their attendance history and live attendance %.

> Note: A student only shows up in a teacher's attendance list if their `class_name` (entered at signup) exactly matches the session's class name. Keep class names consistent (e.g. always `BCA-3A`, not sometimes `bca3a`).

## REST API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/token/` | POST | Get JWT access + refresh token (send `username`, `password`) |
| `/api/token/refresh/` | POST | Refresh access token |
| `/api/students/` | GET/POST | List/create students |
| `/api/teachers/` | GET/POST | List/create teachers |
| `/api/sessions/` | GET/POST | List/create class sessions |
| `/api/attendance/` | GET/POST | List/create attendance records |
| `/api/attendance/my_attendance/` | GET | Logged-in student's own attendance (JWT required) |

All API endpoints (except token endpoints) require:
```
Authorization: Bearer <access_token>
```

## What This Covers (Interview Talking Points)
- Django models, migrations, relationships (ForeignKey, OneToOne)
- Custom forms + validation
- Session-based auth (web) + JWT auth (API) — both implemented, so you can explain both
- Django admin customization
- REST API design with DRF ViewSets + Routers
- Role-based access control (student_profile vs teacher_profile)

## Next Steps / Possible Extensions
- QR-code based attendance (generate QR per session, scan to mark present)
- Email notifications for low attendance
- Timetable module
- Deploy to Render/Railway for a live demo link
