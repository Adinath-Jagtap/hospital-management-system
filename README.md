# 🏥 Hospital Management System

A comprehensive full-stack web application for managing hospital operations, including doctor and patient management, appointment scheduling, and medical treatment tracking. Built with Flask and MongoDB for scalability and reliability.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Locally](#running-locally)
- [Deployment on Render](#deployment-on-render)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Default Credentials](#default-credentials)
- [Database Collections](#database-collections)
- [Security Features](#security-features)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The Hospital Management System is a robust, production-ready application designed to streamline hospital operations and improve patient care. It provides an intuitive interface for administrators to manage facilities, doctors to organize their schedules, and patients to book and manage their appointments seamlessly.

This system implements role-based access control with three distinct user roles: **Admin**, **Doctor**, and **Patient**, each with specialized dashboards and functionalities tailored to their needs.

---

## ✨ Features

### 🔐 Authentication & Authorization
- **Secure User Registration & Login** with role-based access control (Admin, Doctor, Patient)
- **Strong Password Validation** (minimum 8 characters, uppercase letter, digit required)
- **Email and Phone Number Validation**
- **User Account Management** with activation/deactivation capabilities
- **Session Management** with secure cookie-based sessions

### 👨‍💼 Admin Dashboard
- **Comprehensive Analytics Dashboard** displaying total doctors, patients, and appointments
- **Doctor Management**
  - Add new doctors with department assignment
  - Edit doctor information (qualifications, experience, specialization)
  - Deactivate/remove doctors from the system
  - View complete doctor directory with search functionality
- **Patient Management**
  - View all registered patients
  - Edit patient information
  - Manage patient account status
  - Search patients by name or contact information
- **Appointment Oversight**
  - Monitor all appointments across the hospital
  - Track appointment status
  - Historical appointment records
- **Department Configuration** (Pre-loaded: Cardiology, Neurology, Orthopedics, Pediatrics, Dermatology)

### 👨‍⚕️ Doctor Features
- **Smart Dashboard**
  - View upcoming appointments for the next 7 days
  - List of patients they are treating
  - Quick access to patient history
- **Availability Management**
  - Set morning and evening availability slots for the next week
  - Flexible time slot configuration
  - Easy update and rescheduling of availability
- **Appointment Management**
  - View all appointments with patient information
  - Complete appointments with medical documentation
  - Cancel appointments when necessary
- **Medical Records**
  - Record diagnosis, prescription, and clinical notes
  - Access patient treatment history
  - Track all previous interactions with patients
  - View past appointment records

### 👥 Patient Features
- **User-Friendly Dashboard**
  - Upcoming appointments overview
  - Past appointment history (last 10 records)
  - Quick appointment management options
  - Treatment history at a glance
- **Doctor Discovery**
  - Browse all available doctors
  - Filter doctors by department
  - View doctor qualifications, specialization, and experience
  - Search doctors by name or specialization
  - Check doctor availability for the next 7 days
- **Appointment Booking**
  - Intuitive appointment scheduling
  - Real-time availability checking
  - Prevent double-booking
  - Date and time validation
  - Slot availability confirmation
- **Appointment Management**
  - Cancel upcoming appointments
  - Reschedule appointments to different dates/times
  - View appointment confirmation details
- **Medical History**
  - Complete treatment history with diagnoses
  - View prescribed medications
  - Access doctor's clinical notes
  - Track all past appointments
- **Profile Management**
  - View and edit personal information
  - Update contact details (email, phone, address)
  - Manage blood group and medical information

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.3.3
- **Database**: MongoDB 4.5.0
- **Web Server**: Gunicorn 21.2.0
- **Password Hashing**: Werkzeug 2.3.7

### Security & Utilities
- **Password Management**: Werkzeug Security
- **Configuration Management**: python-dotenv 1.0.0
- **Templating Engine**: Jinja2 3.1.2
- **Markup Safety**: MarkupSafe 2.1.3
- **DNS Resolution**: dnspython 2.4.2

### Frontend
- **Template Engine**: Jinja2
- **CSS Framework**: Custom responsive CSS
- **Session Management**: Flask Sessions

### Development Tools
- **WSGI Server**: Gunicorn
- **Configuration**: Environment variables (.env)

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8+** (verify with `python --version`)
- **pip** (Python package manager, included with Python)
- **MongoDB** (local or cloud instance)
- **Git** (optional, for version control)
- **Render Account** (for cloud deployment) - [Create Free Account](https://render.com)

### MongoDB Setup Options

1. **Local MongoDB**: Install from [mongodb.com](https://www.mongodb.com/try/download/community)
2. **MongoDB Atlas** (Recommended for cloud deployment):
   - Create free account at [mongodb.com/atlas](https://www.mongodb.com/atlas)
   - Create a cluster and database
   - Get connection string: `mongodb+srv://username:password@cluster.mongodb.net/database_name`

---

## 📥 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/hospital-management-system.git
cd hospital-management-system
```

### Step 2: Create a Python Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Verify installation:
```bash
pip list
```

---

## ⚙️ Configuration

### Step 1: Create Environment Variables File

Create a `.env` file in the project root directory:

```bash
# Windows
type nul > .env

# macOS/Linux
touch .env
```

### Step 2: Configure Environment Variables

Edit the `.env` file and add the following:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production

# MongoDB Connection
# For local MongoDB
MONGO_URI=mongodb://localhost:27017/hospital

# For MongoDB Atlas (Cloud)
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/hospital?retryWrites=true&w=majority
```

### Step 3: Generate a Secure Secret Key

```bash
# Install secrets generator (if needed)
pip install secrets

# Generate key in Python shell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the generated key and update the `SECRET_KEY` in your `.env` file:

```env
SECRET_KEY=your-generated-hex-key-here
```

---

## 🗄️ Database Setup

### Option 1: Local MongoDB

```bash
# Start MongoDB service (Windows)
mongod

# On macOS with Homebrew
brew services start mongodb-community

# Verify connection
mongo
```

### Option 2: MongoDB Atlas (Recommended for Production)

1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas) and create an account
2. Create a new cluster
3. Create a database user with password
4. Whitelist your IP address (use 0.0.0.0/0 for development)
5. Get your connection string
6. Update `MONGO_URI` in `.env`:

```env
MONGO_URI=mongodb+srv://user:password@cluster0.xxxxx.mongodb.net/hospital?retryWrites=true&w=majority
```

### Database Initialization

The application automatically initializes the database on first run with:
- **Admin user** (username: `admin`, password: `admin123`)
- **Sample departments** (Cardiology, Neurology, Orthopedics, Pediatrics, Dermatology)
- **Database indexes** for optimal query performance

---

## 🚀 Running Locally

### Start the Application

```bash
# Ensure virtual environment is activated
python app.py
```

### Expected Output

```
Running on http://127.0.0.1:5000
Press CTRL+C to quit
Restarting with reloader
```

### Access the Application

Open your web browser and navigate to:

```
http://localhost:5000
```

### Testing the Application

**Admin Login**:
- Navigate to login page
- Username: `admin`
- Password: `admin123`
- Click "Login"

**Patient Registration**:
- Click "Register" on login page
- Fill in all required fields (password must have 8+ chars, 1 uppercase, 1 digit)
- Submit and login

**Doctor Registration** (Admin only):
- Login as Admin
- Go to "Manage Doctors"
- Click "Add New Doctor"
- Fill in doctor details and assign department

---

## 🌐 Deployment on Render

### Prerequisites
- GitHub repository with your code
- MongoDB Atlas account with a cluster

### Step 1: Push Code to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Hospital Management System"
git branch -M main
git remote add origin https://github.com/yourusername/hospital-management-system.git
git push -u origin main
```

### Step 2: Create on Render

1. Go to [Render.com](https://render.com) and sign in
2. Click "New +" → "Web Service"
3. Select "Deploy an existing repository" or connect your GitHub
4. Choose the hospital-management-system repository
5. Fill in the configuration:

   | Setting | Value |
   |---------|-------|
   | **Name** | hospital-management-system |
   | **Environment** | Python 3 |
   | **Region** | Choose closest to users |
   | **Branch** | main |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn app:app` |

### Step 3: Add Environment Variables

In Render Dashboard:
1. Go to your service settings
2. Click "Environment"
3. Add the following variables:

```
SECRET_KEY=your-generated-secret-key-here
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/hospital?retryWrites=true&w=majority
```

### Step 4: Deploy

1. Click "Create Web Service"
2. Render will automatically deploy your application
3. Wait for the deployment to complete (typically 2-5 minutes)
4. Your application will be available at: `https://your-app-name.onrender.com`

### Step 5: Verify Deployment

- Visit your Render URL
- Login with admin credentials
- Test core functionality

### Important Notes for Production

- **Change admin password immediately** after first login
- **Use environment variables** for all sensitive data
- **Keep MongoDB backups** enabled in Atlas
- **Monitor application logs** in Render Dashboard
- **Set up auto-scaling** for high traffic (Render Pro)

---

## 📡 API Documentation

### Public Endpoints (No Authentication Required)

#### 1. Get All Doctors
```http
GET /api/doctors
```

**Response**:
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

#### 2. Get All Appointments
```http
GET /api/appointments
```

**Response**:
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

#### 3. Get Single Appointment
```http
GET /api/appointment/{appointment_id}
```

**Response**:
```json
{
  "id": "507f1f77bcf86cd799439012",
  "patient": "John Doe",
  "doctor": "Dr. Jane Watson",
  "date": "2024-04-15",
  "time": "10:30",
  "status": "Booked"
}
```

#### 4. Update Appointment Status
```http
PUT /api/appointment/{appointment_id}
Content-Type: application/json

{
  "status": "Completed"
}
```

#### 5. Delete/Cancel Appointment
```http
DELETE /api/appointment/{appointment_id}
```

**Response**:
```json
{
  "message": "Appointment cancelled"
}
```

---

## 📁 Project Structure

```
hospital-management-system/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .env.example                    # Environment variables template
│
├── templates/                      # HTML templates
│   ├── base.html                  # Base template with navigation
│   ├── login.html                 # Login page
│   ├── register.html              # Patient registration
│   │
│   ├── admin_dashboard.html       # Admin dashboard
│   ├── admin_doctors.html         # Doctor management
│   ├── admin_patients.html        # Patient management
│   ├── admin_appointments.html    # Appointment overview
│   ├── add_doctor.html            # Add new doctor
│   ├── edit_doctor.html           # Edit doctor info
│   ├── edit_patient.html          # Edit patient info
│   │
│   ├── doctor_dashboard.html      # Doctor home
│   ├── doctor_availability.html   # Set availability
│   ├── patient_history.html       # View patient history
│   ├── complete_appointment.html  # Record treatment
│   │
│   ├── patient_dashboard.html     # Patient home
│   ├── patient_doctors.html       # Browse doctors
│   ├── book_appointment.html      # Book appointment
│   ├── reschedule_appointment.html # Reschedule appointment
│   ├── patient_profile.html       # Patient profile
│   └── treatment_history.html     # Medical history
│
└── static/                         # Static files
    └── css/
        └── hospital.css           # Custom styling
```

---

## 🔑 Default Credentials

After installation, the following default account is automatically created:

| Role | Username | Password | Purpose |
|------|----------|----------|---------|
| Admin | `admin` | `admin123` | System administration |

⚠️ **IMPORTANT**: Change the admin password immediately after first login in production environments.

---

## 🗄️ Database Collections

### 1. Users Collection
```json
{
  "_id": ObjectId,
  "username": "string (unique)",
  "password": "string (hashed)",
  "role": "admin|doctor|patient",
  "name": "string",
  "email": "string",
  "phone": "string",
  "is_active": "boolean"
}
```

### 2. Departments Collection
```json
{
  "_id": ObjectId,
  "name": "string (unique)",
  "description": "string"
}
```

### 3. Doctors Collection
```json
{
  "_id": ObjectId,
  "user_id": "string (reference to users)",
  "department_id": "string (reference to departments)",
  "specialization": "string",
  "qualification": "string",
  "experience_years": "number"
}
```

### 4. Patients Collection
```json
{
  "_id": ObjectId,
  "user_id": "string (reference to users)",
  "date_of_birth": "string (YYYY-MM-DD)",
  "gender": "string",
  "address": "string",
  "blood_group": "string"
}
```

### 5. Appointments Collection
```json
{
  "_id": ObjectId,
  "patient_id": "string (reference to patients)",
  "doctor_id": "string (reference to doctors)",
  "date": "string (YYYY-MM-DD)",
  "time": "string (HH:MM)",
  "status": "Booked|Completed|Cancelled",
  "created_at": "ISO timestamp"
}
```

### 6. Doctor Availabilities Collection
```json
{
  "_id": ObjectId,
  "doctor_id": "string (reference to doctors)",
  "date": "string (YYYY-MM-DD)",
  "start_time": "string (HH:MM)",
  "end_time": "string (HH:MM)",
  "is_available": "boolean"
}
```

### 7. Treatments Collection
```json
{
  "_id": ObjectId,
  "appointment_id": "string (reference to appointments)",
  "diagnosis": "string",
  "prescription": "string",
  "notes": "string",
  "created_at": "ISO timestamp"
}
```

---

## 🔒 Security Features

### Authentication & Authorization
- ✅ Role-based access control (RBAC)
- ✅ Secure password hashing with Werkzeug
- ✅ Session-based authentication
- ✅ Login required decorators on protected routes
- ✅ Account activation/deactivation

### Input Validation
- ✅ Email format validation
- ✅ Phone number validation (minimum 10 digits)
- ✅ Password strength enforcement (8+ chars, uppercase, digit)
- ✅ Date of birth validation (not in future)
- ✅ Date and time format validation
- ✅ XSS protection via MarkupSafe escape()

### Database Security
- ✅ Unique indexes on username
- ✅ Indexed queries for performance
- ✅ MongoDB URI via environment variables
- ✅ Prepared statements with parameterized queries

### Production Recommendations
- 🔐 Use HTTPS/SSL in production
- 🔐 Set `debug=False` in production (already configured)
- 🔐 Use strong SECRET_KEY (minimum 32 characters)
- 🔐 Enable MongoDB Atlas IP Whitelisting
- 🔐 Implement rate limiting on login attempts
- 🔐 Set up CSRF protection for form submissions
- 🔐 Use environment variables for all secrets
- 🔐 Enable MongoDB authentication

---

## 🧪 Testing the System

### Admin Test Flow
1. Login with admin/admin123
2. Navigate to "Manage Doctors" and add a doctor
3. Navigate to "Manage Patients" to view registered patients
4. Check "View Appointments" to see all bookings

### Doctor Test Flow
1. Login as a doctor (created by admin)
2. Go to "Availability" and set your weekly schedule
3. View upcoming appointments on dashboard
4. Complete an appointment with diagnosis and notes

### Patient Test Flow
1. Register as a new patient
2. Update profile information
3. Browse doctors by department
4. Book an appointment with a doctor
5. View appointment in dashboard
6. Reschedule or cancel appointment
7. View treatment history after appointment completion

---

## 🐛 Troubleshooting

### Common Issues

#### MongoDBConnectionError
```
Error: Could not connect to MongoDB
```
**Solution**: 
- Verify MongoDB service is running
- Check MONGO_URI in .env file
- Ensure IP whitelist in MongoDB Atlas includes your IP

#### ImportError: No module named 'flask'
```
Solution: Activate virtual environment and run: pip install -r requirements.txt
```

#### Port 5000 already in use
```bash
# Find process using port 5000 (Windows)
netstat -ano | findstr :5000

# Kill process (Windows)
taskkill /PID <PID> /F

# On macOS/Linux
lsof -ti:5000 | xargs kill -9
```

#### .env file not being read
- Ensure python-dotenv is installed
- Verify .env file is in the project root
- Restart Flask application after editing .env

#### Admin login failing
- Ensure MongoDB is initialized (app.py runs init_db() automatically)
- Check MongoDB connection
- Verify admin user exists in database

---

## 📧 Support & Documentation

- **Report Issues**: Open an issue on GitHub
- **Documentation**: Check inline code comments
- **MongoDB Docs**: [docs.mongodb.com](https://docs.mongodb.com)
- **Flask Docs**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- **Render Docs**: [render.com/docs](https://render.com/docs)

---

## 📝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 Hospital Management System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙌 Acknowledgments

- Flask framework and community
- MongoDB for robust database solutions
- Render for seamless cloud deployment
- All contributors and users

---

## 📞 Contact

For questions or inquiries, please reach out through:
- GitHub Issues
- Email: [your-email@example.com]
- LinkedIn: [your-linkedin-profile]

---

**Last Updated**: April 2024
**Version**: 1.0.0
**Status**: Production Ready ✅