<div align="center">

# 🏥 Hospital Management System

### Built with Flask & MongoDB · Role-Based · Scalable · Secure

<br/>

<!-- Action Badges -->
[![Live Demo](https://img.shields.io/badge/🌐%20Live%20Demo-Visit%20App-00B4D8?style=for-the-badge)](https://hospital-management-system-uzp9.onrender.com/)
[![Source Code](https://img.shields.io/badge/GitHub-Source%20Code-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Adinath-Jagtap/hospital-management-system)

<br/>

<!-- Tech Stack Badges -->
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3.3-000000?style=flat-square&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4.5.0-47A248?style=flat-square&logo=mongodb&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-21.2.0-499848?style=flat-square&logo=gunicorn&logoColor=white)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat-square&logo=render&logoColor=white)

<br/>

> **A comprehensive full-stack web application for managing hospital operations** — including doctor and patient management, appointment scheduling, and medical treatment tracking.

<br/>

</div>

---

## 📋 Table of Contents

<details>
<summary>Click to expand</summary>

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#️-technology-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Running Locally](#-running-locally)
- [Deployment on Render](#-deployment-on-render)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Default Credentials](#-default-credentials)
- [Database Collections](#️-database-collections)
- [Security Features](#-security-features)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

</details>

---

## 🎯 Overview

The **Hospital Management System** is a robust, production-ready application designed to streamline hospital operations and improve patient care. It provides an intuitive interface for administrators to manage facilities, doctors to organize their schedules, and patients to book and manage their appointments seamlessly.

This system implements **role-based access control** with three distinct user roles — each with specialized dashboards tailored to their needs:

<br/>

<div align="center">

| 👨‍💼 Admin | 👨‍⚕️ Doctor | 👥 Patient |
|:---:|:---:|:---:|
| Full system control | Manage schedules & patients | Book & track appointments |
| Analytics dashboard | Set availability | View treatment history |
| Doctor & patient management | Record diagnoses | Browse & filter doctors |

</div>

---

## ✨ Features

<details open>
<summary><b>🔐 Authentication & Authorization</b></summary>
<br/>

- Secure **User Registration & Login** with role-based access control (Admin, Doctor, Patient)
- **Strong Password Validation** — minimum 8 characters, uppercase letter, and digit required
- **Email and Phone Number Validation**
- **User Account Management** with activation/deactivation capabilities
- **Session Management** with secure cookie-based sessions

</details>

<details>
<summary><b>👨‍💼 Admin Dashboard</b></summary>
<br/>

- **Comprehensive Analytics Dashboard** — total doctors, patients, and appointments at a glance
- **Doctor Management** — add, edit, deactivate, and search doctors across departments
- **Patient Management** — view, edit, and manage patient account status
- **Appointment Oversight** — monitor all appointments with full status tracking
- **Pre-loaded Departments**: Cardiology · Neurology · Orthopedics · Pediatrics · Dermatology

</details>

<details>
<summary><b>👨‍⚕️ Doctor Features</b></summary>
<br/>

- **Smart Dashboard** — upcoming appointments for the next 7 days, patient list, and quick access to history
- **Availability Management** — set morning/evening slots for the next week with flexible configuration
- **Appointment Management** — view, complete with documentation, or cancel appointments
- **Medical Records** — record diagnosis, prescription, and clinical notes; access full patient treatment history

</details>

<details>
<summary><b>👥 Patient Features</b></summary>
<br/>

- **User-Friendly Dashboard** — upcoming appointments, past 10 records, and treatment history
- **Doctor Discovery** — browse, filter by department, and check real-time availability for next 7 days
- **Smart Appointment Booking** — real-time availability checking, double-booking prevention, slot confirmation
- **Appointment Management** — cancel or reschedule upcoming appointments
- **Medical History** — complete treatment records with diagnoses, prescriptions, and doctor notes
- **Profile Management** — update personal details, contact info, and medical information

</details>

---

## 🛠️ Technology Stack

<div align="center">

| Layer | Technology | Version |
|:------|:-----------|:--------|
| **Backend Framework** | Flask | 2.3.3 |
| **Database** | MongoDB | 4.5.0 |
| **Web Server** | Gunicorn | 21.2.0 |
| **Password Hashing** | Werkzeug Security | 2.3.7 |
| **Templating Engine** | Jinja2 | 3.1.2 |
| **Config Management** | python-dotenv | 1.0.0 |
| **DNS Resolution** | dnspython | 2.4.2 |
| **Frontend Styling** | Custom Responsive CSS | — |

</div>

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

```
✅  Python 3.8+       →  python --version
✅  pip               →  Included with Python
✅  MongoDB           →  Local or MongoDB Atlas (cloud)
✅  Git               →  For version control (optional)
✅  Render Account    →  https://render.com  (for deployment)
```

### MongoDB Setup Options

**Option A — Local MongoDB**
```
Download from: https://www.mongodb.com/try/download/community
```

**Option B — MongoDB Atlas** *(Recommended for production)*
```
1. Create account at:  https://www.mongodb.com/atlas
2. Create a cluster and database
3. Get connection string:
   mongodb+srv://username:password@cluster.mongodb.net/database_name
```

---

## 📥 Installation

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Adinath-Jagtap/hospital-management-system.git
cd hospital-management-system
```

### Step 2 — Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt

# Verify installation
pip list
```

---

## ⚙️ Configuration

### Step 1 — Create the Environment File

```bash
# Windows
type nul > .env

# macOS / Linux
touch .env
```

### Step 2 — Add Environment Variables

```env
# ─── Flask Configuration ────────────────────────────────────────
SECRET_KEY=your-super-secret-key-change-this-in-production

# ─── MongoDB Connection ──────────────────────────────────────────
# Local MongoDB
MONGO_URI=mongodb://localhost:27017/hospital

# MongoDB Atlas (Cloud) — Recommended
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/hospital?retryWrites=true&w=majority
```

### Step 3 — Generate a Secure Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and set it as your `SECRET_KEY` in `.env`.

---

## 🗄️ Database Setup

<details>
<summary><b>Option 1 — Local MongoDB</b></summary>

```bash
# Start MongoDB (Windows)
mongod

# Start MongoDB (macOS with Homebrew)
brew services start mongodb-community

# Verify connection
mongo
```

</details>

<details>
<summary><b>Option 2 — MongoDB Atlas (Recommended)</b></summary>

1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas) and create an account
2. Create a new cluster and database user
3. Whitelist your IP address (`0.0.0.0/0` for development)
4. Get your connection string and update `.env`:

```env
MONGO_URI=mongodb+srv://user:password@cluster0.xxxxx.mongodb.net/hospital?retryWrites=true&w=majority
```

</details>

> **ℹ️ Note:** The application **automatically initializes the database** on first run with an admin user, sample departments, and performance indexes.

---

## 🚀 Running Locally

```bash
# Ensure your virtual environment is activated, then:
python app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
 * Restarting with reloader
```

Open **http://localhost:5000** in your browser.

### Quick Test Guide

| Role | Steps |
|------|-------|
| **Admin** | Login with `admin` / `admin123` |
| **Patient** | Click "Register" → fill required fields → login |
| **Doctor** | Admin must add doctor via "Manage Doctors" |

---

## 🌐 Deployment on Render

### Step 1 — Push Code to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Hospital Management System"
git branch -M main
git remote add origin https://github.com/Adinath-Jagtap/hospital-management-system.git
git push -u origin main
```

### Step 2 — Create a Web Service on Render

1. Go to [render.com](https://render.com) and sign in
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Fill in the configuration:

| Setting | Value |
|:--------|:------|
| **Name** | `hospital-management-system` |
| **Environment** | `Python 3` |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |

### Step 3 — Add Environment Variables

In your Render service settings, under **Environment**, add:

```
SECRET_KEY   →   your-generated-secret-key
MONGO_URI    →   mongodb+srv://user:pass@cluster.mongodb.net/hospital?...
```

### Step 4 — Deploy

Click **Create Web Service**. Render will deploy your app in 2–5 minutes.
Your app will be live at: `https://your-app-name.onrender.com`

> ⚠️ **Production Checklist**
> - Change the admin password immediately after first login
> - Use environment variables for all sensitive data
> - Enable MongoDB Atlas IP Whitelisting
> - Keep MongoDB backups enabled

---

## 📡 API Documentation

> All endpoints listed below are **public** and require no authentication.

### `GET /api/doctors`
Returns a list of all doctors.

```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "name": "Dr. John Smith",
    "specialization": "Cardiology",
    "department": "Cardiology",
    "experience": 15
  }
]
```

---

### `GET /api/appointments`
Returns all appointments.

```json
[
  {
    "id": "507f1f77bcf86cd799439012",
    "patient": "John Doe",
    "doctor": "Dr. Jane Watson",
    "date": "2024-04-15",
    "time": "10:30",
    "status": "Booked"
  }
]
```

---

### `GET /api/appointment/{appointment_id}`
Returns a single appointment by ID.

---

### `PUT /api/appointment/{appointment_id}`
Updates appointment status.

```json
{ "status": "Completed" }
```

---

### `DELETE /api/appointment/{appointment_id}`
Cancels an appointment.

```json
{ "message": "Appointment cancelled" }
```

---

## 📁 Project Structure

```
hospital-management-system/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── .env.example                    # Environment variables template
│
├── templates/                      # Jinja2 HTML templates
│   ├── base.html                   # Base layout with navigation
│   ├── login.html                  # Login page
│   ├── register.html               # Patient registration
│   │
│   ├── admin_dashboard.html        # Admin dashboard
│   ├── admin_doctors.html          # Doctor management
│   ├── admin_patients.html         # Patient management
│   ├── admin_appointments.html     # Appointment overview
│   ├── add_doctor.html             # Add new doctor
│   ├── edit_doctor.html            # Edit doctor info
│   ├── edit_patient.html           # Edit patient info
│   │
│   ├── doctor_dashboard.html       # Doctor home
│   ├── doctor_availability.html    # Set availability
│   ├── patient_history.html        # View patient history
│   ├── complete_appointment.html   # Record treatment
│   │
│   ├── patient_dashboard.html      # Patient home
│   ├── patient_doctors.html        # Browse doctors
│   ├── book_appointment.html       # Book appointment
│   ├── reschedule_appointment.html # Reschedule appointment
│   ├── patient_profile.html        # Patient profile
│   └── treatment_history.html      # Medical history
│
└── static/
    └── css/
        └── hospital.css            # Custom responsive styling
```

---

## 🔑 Default Credentials

> Auto-created on first run.

<div align="center">

| Role | Username | Password |
|:----:|:--------:|:--------:|
| 👨‍💼 Admin | `admin` | `admin123` |

</div>

> ⚠️ **IMPORTANT**: Change the admin password immediately after first login in any production environment.

---

## 🗄️ Database Collections

<details>
<summary><b>Users Collection</b></summary>

```json
{
  "_id": "ObjectId",
  "username": "string (unique)",
  "password": "string (hashed)",
  "role": "admin | doctor | patient",
  "name": "string",
  "email": "string",
  "phone": "string",
  "is_active": "boolean"
}
```
</details>

<details>
<summary><b>Departments Collection</b></summary>

```json
{
  "_id": "ObjectId",
  "name": "string (unique)",
  "description": "string"
}
```
</details>

<details>
<summary><b>Doctors Collection</b></summary>

```json
{
  "_id": "ObjectId",
  "user_id": "string (ref → users)",
  "department_id": "string (ref → departments)",
  "specialization": "string",
  "qualification": "string",
  "experience_years": "number"
}
```
</details>

<details>
<summary><b>Patients Collection</b></summary>

```json
{
  "_id": "ObjectId",
  "user_id": "string (ref → users)",
  "date_of_birth": "string (YYYY-MM-DD)",
  "gender": "string",
  "address": "string",
  "blood_group": "string"
}
```
</details>

<details>
<summary><b>Appointments Collection</b></summary>

```json
{
  "_id": "ObjectId",
  "patient_id": "string (ref → patients)",
  "doctor_id": "string (ref → doctors)",
  "date": "string (YYYY-MM-DD)",
  "time": "string (HH:MM)",
  "status": "Booked | Completed | Cancelled",
  "created_at": "ISO timestamp"
}
```
</details>

<details>
<summary><b>Doctor Availabilities Collection</b></summary>

```json
{
  "_id": "ObjectId",
  "doctor_id": "string (ref → doctors)",
  "date": "string (YYYY-MM-DD)",
  "start_time": "string (HH:MM)",
  "end_time": "string (HH:MM)",
  "is_available": "boolean"
}
```
</details>

<details>
<summary><b>Treatments Collection</b></summary>

```json
{
  "_id": "ObjectId",
  "appointment_id": "string (ref → appointments)",
  "diagnosis": "string",
  "prescription": "string",
  "notes": "string",
  "created_at": "ISO timestamp"
}
```
</details>

---

## 🔒 Security Features

### Authentication & Authorization
```
✅  Role-based access control (RBAC)
✅  Secure password hashing with Werkzeug
✅  Session-based authentication
✅  Login-required decorators on protected routes
✅  Account activation / deactivation
```

### Input Validation
```
✅  Email format validation
✅  Phone number validation (minimum 10 digits)
✅  Password strength enforcement (8+ chars, uppercase, digit)
✅  Date of birth validation (not in future)
✅  Date and time format validation
✅  XSS protection via MarkupSafe escape()
```

### Database Security
```
✅  Unique indexes on username
✅  Indexed queries for performance
✅  MongoDB URI stored via environment variables
✅  Parameterized queries
```

### Production Recommendations
```
🔐  Use HTTPS / SSL in production
🔐  Set debug=False (already configured)
🔐  Use a strong SECRET_KEY (32+ characters)
🔐  Enable MongoDB Atlas IP Whitelisting
🔐  Implement rate limiting on login attempts
🔐  Add CSRF protection for form submissions
🔐  Enable MongoDB authentication
```

---

## 🐛 Troubleshooting

<details>
<summary><b>MongoDB Connection Error</b></summary>

```
Error: Could not connect to MongoDB
```
- Verify MongoDB service is running
- Check `MONGO_URI` in your `.env` file
- Ensure your IP is whitelisted in MongoDB Atlas

</details>

<details>
<summary><b>ImportError: No module named 'flask'</b></summary>

Activate your virtual environment, then:
```bash
pip install -r requirements.txt
```

</details>

<details>
<summary><b>Port 5000 already in use</b></summary>

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS / Linux
lsof -ti:5000 | xargs kill -9
```

</details>

<details>
<summary><b>.env file not being read</b></summary>

- Ensure `python-dotenv` is installed
- Verify `.env` is in the project root directory
- Restart the Flask application after editing `.env`

</details>

<details>
<summary><b>Admin login failing</b></summary>

- Ensure MongoDB is running and connected
- The `init_db()` function in `app.py` auto-creates the admin on first run
- Verify the admin user exists in your database

</details>

---

## 📝 Contributing

Contributions are welcome! Here's how to get started:

```bash
# 1. Fork the repository
# 2. Create your feature branch
git checkout -b feature/AmazingFeature

# 3. Commit your changes
git commit -m "Add AmazingFeature"

# 4. Push to your branch
git push origin feature/AmazingFeature

# 5. Open a Pull Request on GitHub
```

---

## 📚 Resources

| Resource | Link |
|----------|------|
| Flask Documentation | [flask.palletsprojects.com](https://flask.palletsprojects.com) |
| MongoDB Documentation | [docs.mongodb.com](https://docs.mongodb.com) |
| MongoDB Atlas | [mongodb.com/atlas](https://www.mongodb.com/atlas) |
| Render Documentation | [render.com/docs](https://render.com/docs) |
| Live Application | [hospital-management-system-uzp9.onrender.com](https://hospital-management-system-uzp9.onrender.com/) |

---

<div align="center">

**Made with ❤️ by [Adinath Jagtap](https://github.com/Adinath-Jagtap)**

[![GitHub followers](https://img.shields.io/github/followers/Adinath-Jagtap?style=social)](https://github.com/Adinath-Jagtap)

</div>
