from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, date, time
from functools import wraps
from bson import ObjectId
from dotenv import load_dotenv
import os
import pymongo
from markupsafe import escape

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# ─── Logging Configuration ────────────────────────────────────────────────────────
import logging
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

# ─── MongoDB Connection ────────────────────────────────────────────────────────
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/hospital')
client = pymongo.MongoClient(MONGO_URI)
db = client.get_database()

# Collections
users_col        = db['users']
departments_col  = db['departments']
doctors_col      = db['doctors']
patients_col     = db['patients']
availabilities_col = db['doctor_availabilities']
appointments_col = db['appointments']
treatments_col   = db['treatments']

# ─── Indexes ──────────────────────────────────────────────────────────────────
users_col.create_index('username', unique=True)
departments_col.create_index('name', unique=True)
appointments_col.create_index([('doctor_id', 1), ('date', 1), ('time', 1)])

# ─── Helper Utilities ─────────────────────────────────────────────────────────

def str_id(oid):
    """Convert ObjectId to string safely."""
    return str(oid) if oid else None

def oid(s):
    """Convert string to ObjectId safely."""
    try:
        return ObjectId(s)
    except Exception:
        return None
# ─── Validation Functions ─────────────────────────────────────────────────────

def validate_email(email):
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    """Validate phone number (at least 10 digits)."""
    import re
    pattern = r'^[0-9\-\+\(\)\s]{10,}$'
    return bool(re.match(pattern, phone))

def validate_password(password):
    """Validate password strength."""
    if len(password) < 8:
        return False, 'Password must be at least 8 characters'
    if not any(c.isupper() for c in password):
        return False, 'Password must contain at least one uppercase letter'
    if not any(c.isdigit() for c in password):
        return False, 'Password must contain at least one digit'
    return True, 'Password is valid'

def validate_date_format(date_str):
    """Validate date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d').date()
        return True
    except ValueError:
        return False

def validate_time_format(time_str):
    """Validate time format (HH:MM)."""
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def validate_dob(dob_str):
    """Validate DOB is not in future and valid format."""
    try:
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        if dob > date.today():
            return False, 'DOB cannot be in the future'
        # Optional: Check age (at least 13 for patient registration)
        age = (date.today() - dob).days // 365
        if age < 1:
            return False, 'Invalid date of birth'
        return True, 'Valid DOB'
    except ValueError:
        return False, 'Invalid date format'
def date_to_str(d):
    if isinstance(d, date):
        return d.strftime('%Y-%m-%d')
    return d

def time_to_str(t):
    if isinstance(t, time):
        return t.strftime('%H:%M')
    return t

def str_to_date(s):
    if isinstance(s, date):
        return s
    return datetime.strptime(s, '%Y-%m-%d').date()

def str_to_time(s):
    if isinstance(s, time):
        return s
    if len(s) == 5:
        return datetime.strptime(s, '%H:%M').time()
    return datetime.strptime(s, '%H:%M:%S').time()


# ─── Auth Decorators ──────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                flash('Access denied', 'error')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ─── Seed Initial Data ────────────────────────────────────────────────────────

def init_db():
    # Create admin if not exists
    if not users_col.find_one({'username': 'admin'}):
        users_col.insert_one({
            'username': 'admin',
            'password': generate_password_hash('admin123'),
            'role': 'admin',
            'name': 'Admin',
            'email': 'admin@hospital.com',
            'phone': '1234567890',
            'is_active': True
        })

    # Create sample departments
    if departments_col.count_documents({}) == 0:
        departments = [
            {'name': 'Cardiology',   'description': 'Heart and cardiovascular system'},
            {'name': 'Neurology',    'description': 'Brain and nervous system'},
            {'name': 'Orthopedics',  'description': 'Bones and joints'},
            {'name': 'Pediatrics',   'description': 'Child healthcare'},
            {'name': 'Dermatology',  'description': 'Skin conditions'},
        ]
        departments_col.insert_many(departments)


# ─── Routes: Auth ─────────────────────────────────────────────────────────────

@app.route('/')
def index():
    if 'user_id' in session:
        role = session.get('role')
        if role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif role == 'doctor':
            return redirect(url_for('doctor_dashboard'))
        elif role == 'patient':
            return redirect(url_for('patient_dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()

            if not username or not password:
                flash('Username and password required', 'error')
                return render_template('login.html')

            user = users_col.find_one({'username': username})
            if user and check_password_hash(user['password'], password):
                if not user.get('is_active', True):
                    flash('Your account has been deactivated', 'error')
                    return redirect(url_for('login'))

                session['user_id'] = str_id(user['_id'])
                session['username'] = user['username']
                session['role']     = user['role']
                session['name']     = user['name']

                flash(f"Welcome {user['name']}!", 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid credentials', 'error')
        except Exception as e:
            app.logger.error(f'Login error: {e}')
            flash('An error occurred during login', 'error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username    = request.form.get('username', '').strip()
            password    = request.form.get('password', '').strip()
            name        = request.form.get('name', '').strip()
            email       = request.form.get('email', '').strip()
            phone       = request.form.get('phone', '').strip()
            dob         = request.form.get('dob', '').strip()
            gender      = request.form.get('gender', '').strip()
            address     = request.form.get('address', '').strip()
            blood_group = request.form.get('blood_group', '').strip()

            # Validate all required fields
            if not all([username, password, name, email, phone, dob, gender, address]):
                flash('All fields are required', 'error')
                return render_template('register.html', today=date.today().strftime('%Y-%m-%d'))

            # Validate email format
            if not validate_email(email):
                flash('Invalid email format', 'error')
                return render_template('register.html', today=date.today().strftime('%Y-%m-%d'))

            # Validate phone format
            if not validate_phone(phone):
                flash('Phone must contain at least 10 digits', 'error')
                return render_template('register.html', today=date.today().strftime('%Y-%m-%d'))

            # Validate DOB
            is_valid_dob, dob_msg = validate_dob(dob)
            if not is_valid_dob:
                flash(dob_msg, 'error')
                return render_template('register.html', today=date.today().strftime('%Y-%m-%d'))

            # Validate password strength
            is_valid_pwd, pwd_msg = validate_password(password)
            if not is_valid_pwd:
                flash(pwd_msg, 'error')
                return render_template('register.html', today=date.today().strftime('%Y-%m-%d'))

            # Check duplicate username
            if users_col.find_one({'username': username}):
                flash('Username already exists', 'error')
                return render_template('register.html', today=date.today().strftime('%Y-%m-%d'))

            # Check duplicate email
            if users_col.find_one({'email': email}):
                flash('Email already registered', 'error')
                return render_template('register.html', today=date.today().strftime('%Y-%m-%d'))

            user_doc = {
                'username':  username,
                'password':  generate_password_hash(password),
                'role':      'patient',
                'name':      escape(name),
                'email':     email.lower(),
                'phone':     phone,
                'is_active': True
            }
            user_id = users_col.insert_one(user_doc).inserted_id

            patient_doc = {
                'user_id':       str_id(user_id),
                'date_of_birth': dob,
                'gender':        gender,
                'address':       escape(address),
                'blood_group':   blood_group
            }
            patients_col.insert_one(patient_doc)

            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            app.logger.error(f'Registration error: {e}')
            flash('An error occurred during registration', 'error')
            return render_template('register.html', today=date.today().strftime('%Y-%m-%d'))

    today_str = date.today().strftime('%Y-%m-%d')
    return render_template('register.html', today=today_str)


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))


# ─── Routes: Admin ────────────────────────────────────────────────────────────

@app.route('/admin/dashboard')
@login_required
@role_required('admin')
def admin_dashboard():
    total_doctors  = doctors_col.count_documents({})
    total_patients = patients_col.count_documents({})
    total_appointments = appointments_col.count_documents({})
    today_str = date.today().strftime('%Y-%m-%d')
    upcoming_appointments = appointments_col.count_documents({
        'date':   {'$gte': today_str},
        'status': 'Booked'
    })
    return render_template('admin_dashboard.html',
                           total_doctors=total_doctors,
                           total_patients=total_patients,
                           total_appointments=total_appointments,
                           upcoming_appointments=upcoming_appointments)


@app.route('/admin/doctors')
@login_required
@role_required('admin')
def admin_doctors():
    search = request.args.get('search', '')
    doctor_docs = list(doctors_col.find())
    doctors = []
    for doc in doctor_docs:
        user = users_col.find_one({'_id': oid(doc['user_id']), 'is_active': True})
        if not user:
            continue
        if search and search.lower() not in user['name'].lower() and \
                search.lower() not in doc.get('specialization', '').lower():
            continue
        dept = departments_col.find_one({'_id': oid(doc['department_id'])})
        doc['_user'] = user
        doc['_dept'] = dept
        doctors.append(doc)
    return render_template('admin_doctors.html', doctors=doctors, search=search)


@app.route('/admin/add_doctor', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_doctor():
    if request.method == 'POST':
        try:
            username       = request.form.get('username', '').strip()
            password       = request.form.get('password', '').strip()
            name           = request.form.get('name', '').strip()
            email          = request.form.get('email', '').strip()
            phone          = request.form.get('phone', '').strip()
            department_id  = request.form.get('department_id', '').strip()
            specialization = request.form.get('specialization', '').strip()
            qualification  = request.form.get('qualification', '').strip()
            experience     = request.form.get('experience', '').strip()

            # Validate all required fields
            if not all([username, password, name, email, phone, department_id, specialization, qualification, experience]):
                flash('All fields are required', 'error')
                departments = list(departments_col.find())
                return render_template('add_doctor.html', departments=departments)

            # Validate email format
            if not validate_email(email):
                flash('Invalid email format', 'error')
                departments = list(departments_col.find())
                return render_template('add_doctor.html', departments=departments)

            # Validate phone format
            if not validate_phone(phone):
                flash('Phone must contain at least 10 digits', 'error')
                departments = list(departments_col.find())
                return render_template('add_doctor.html', departments=departments)

            # Validate password strength
            is_valid_pwd, pwd_msg = validate_password(password)
            if not is_valid_pwd:
                flash(pwd_msg, 'error')
                departments = list(departments_col.find())
                return render_template('add_doctor.html', departments=departments)

            # Validate department exists
            dept = departments_col.find_one({'_id': oid(department_id)})
            if not dept:
                flash('Invalid department selected', 'error')
                departments = list(departments_col.find())
                return render_template('add_doctor.html', departments=departments)

            # Validate experience is numeric
            try:
                exp_years = int(experience)
                if exp_years < 0 or exp_years > 70:
                    flash('Experience must be between 0 and 70 years', 'error')
                    departments = list(departments_col.find())
                    return render_template('add_doctor.html', departments=departments)
            except ValueError:
                flash('Experience must be a valid number', 'error')
                departments = list(departments_col.find())
                return render_template('add_doctor.html', departments=departments)

            # Check duplicate username
            if users_col.find_one({'username': username}):
                flash('Username already exists', 'error')
                departments = list(departments_col.find())
                return render_template('add_doctor.html', departments=departments)

            # Check duplicate email
            if users_col.find_one({'email': email}):
                flash('Email already registered', 'error')
                departments = list(departments_col.find())
                return render_template('add_doctor.html', departments=departments)

            user_id = users_col.insert_one({
                'username':  username,
                'password':  generate_password_hash(password),
                'role':      'doctor',
                'name':      escape(name),
                'email':     email.lower(),
                'phone':     phone,
                'is_active': True
            }).inserted_id

            doctors_col.insert_one({
                'user_id':       str_id(user_id),
                'department_id': department_id,
                'specialization': escape(specialization),
                'qualification':  escape(qualification),
                'experience_years': exp_years
            })

            flash('Doctor added successfully', 'success')
            return redirect(url_for('admin_doctors'))
        except Exception as e:
            app.logger.error(f'Add doctor error: {e}')
            flash('An error occurred while adding doctor', 'error')
            departments = list(departments_col.find())
            return render_template('add_doctor.html', departments=departments)

    departments = list(departments_col.find())
    return render_template('add_doctor.html', departments=departments)


@app.route('/admin/edit_doctor/<doc_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_doctor(doc_id):
    doctor = doctors_col.find_one({'_id': oid(doc_id)})
    if not doctor:
        flash('Doctor not found', 'error')
        return redirect(url_for('admin_doctors'))

    user = users_col.find_one({'_id': oid(doctor['user_id'])})

    if request.method == 'POST':
        try:
            name           = request.form.get('name', '').strip()
            email          = request.form.get('email', '').strip()
            phone          = request.form.get('phone', '').strip()
            department_id  = request.form.get('department_id', '').strip()
            specialization = request.form.get('specialization', '').strip()
            qualification  = request.form.get('qualification', '').strip()
            experience     = request.form.get('experience', '').strip()

            if not all([name, email, phone, department_id, specialization, qualification, experience]):
                flash('All fields are required', 'error')
                departments = list(departments_col.find())
                doctor['_user'] = user
                doctor['_dept'] = departments_col.find_one({'_id': oid(doctor['department_id'])})
                return render_template('edit_doctor.html', doctor=doctor, departments=departments)

            if not validate_email(email):
                flash('Invalid email format', 'error')
                departments = list(departments_col.find())
                doctor['_user'] = user
                doctor['_dept'] = departments_col.find_one({'_id': oid(doctor['department_id'])})
                return render_template('edit_doctor.html', doctor=doctor, departments=departments)

            if not validate_phone(phone):
                flash('Phone must contain at least 10 digits', 'error')
                departments = list(departments_col.find())
                doctor['_user'] = user
                doctor['_dept'] = departments_col.find_one({'_id': oid(doctor['department_id'])})
                return render_template('edit_doctor.html', doctor=doctor, departments=departments)

            dept = departments_col.find_one({'_id': oid(department_id)})
            if not dept:
                flash('Invalid department selected', 'error')
                departments = list(departments_col.find())
                doctor['_user'] = user
                doctor['_dept'] = departments_col.find_one({'_id': oid(doctor['department_id'])})
                return render_template('edit_doctor.html', doctor=doctor, departments=departments)

            try:
                exp_years = int(experience)
                if exp_years < 0 or exp_years > 70:
                    flash('Experience must be between 0 and 70 years', 'error')
                    departments = list(departments_col.find())
                    doctor['_user'] = user
                    doctor['_dept'] = departments_col.find_one({'_id': oid(doctor['department_id'])})
                    return render_template('edit_doctor.html', doctor=doctor, departments=departments)
            except ValueError:
                flash('Experience must be a valid number', 'error')
                departments = list(departments_col.find())
                doctor['_user'] = user
                doctor['_dept'] = departments_col.find_one({'_id': oid(doctor['department_id'])})
                return render_template('edit_doctor.html', doctor=doctor, departments=departments)

            users_col.update_one({'_id': oid(doctor['user_id'])}, {'$set': {
                'name':  escape(name),
                'email': email.lower(),
                'phone': phone
            }})
            doctors_col.update_one({'_id': oid(doc_id)}, {'$set': {
                'department_id':  department_id,
                'specialization': escape(specialization),
                'qualification':  escape(qualification),
                'experience_years': exp_years
            }})
            flash('Doctor updated successfully', 'success')
            return redirect(url_for('admin_doctors'))
        except Exception as e:
            app.logger.error(f'Edit doctor error: {e}')
            flash('An error occurred while updating doctor', 'error')

    departments = list(departments_col.find())
    doctor['_user'] = user
    dept = departments_col.find_one({'_id': oid(doctor['department_id'])})
    doctor['_dept'] = dept
    return render_template('edit_doctor.html', doctor=doctor, departments=departments)


@app.route('/admin/delete_doctor/<doc_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def delete_doctor(doc_id):
    if request.method != 'POST':
        flash('Invalid request method', 'error')
        return redirect(url_for('admin_doctors'))
    doctor = doctors_col.find_one({'_id': oid(doc_id)})
    if doctor:
        users_col.update_one({'_id': oid(doctor['user_id'])}, {'$set': {'is_active': False}})
    flash('Doctor deactivated successfully', 'success')
    return redirect(url_for('admin_doctors'))


@app.route('/admin/patients')
@login_required
@role_required('admin')
def admin_patients():
    search = request.args.get('search', '')
    patient_docs = list(patients_col.find())
    patients = []
    for pat in patient_docs:
        user = users_col.find_one({'_id': oid(pat['user_id']), 'is_active': True})
        if not user:
            continue
        if search and search.lower() not in user['name'].lower() and \
                search.lower() not in user.get('phone', '').lower():
            continue
        pat['_user'] = user
        patients.append(pat)
    return render_template('admin_patients.html', patients=patients, search=search)


@app.route('/admin/edit_patient/<pat_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_patient(pat_id):
    patient = patients_col.find_one({'_id': oid(pat_id)})
    if not patient:
        flash('Patient not found', 'error')
        return redirect(url_for('admin_patients'))
    user = users_col.find_one({'_id': oid(patient['user_id'])})

    if request.method == 'POST':
        try:
            name        = request.form.get('name', '').strip()
            email       = request.form.get('email', '').strip()
            phone       = request.form.get('phone', '').strip()
            address     = request.form.get('address', '').strip()
            blood_group = request.form.get('blood_group', '').strip()

            if not all([name, email, phone, address]):
                flash('Name, email, phone, and address are required', 'error')
                patient['_user'] = user
                return render_template('edit_patient.html', patient=patient)

            if not validate_email(email):
                flash('Invalid email format', 'error')
                patient['_user'] = user
                return render_template('edit_patient.html', patient=patient)

            if not validate_phone(phone):
                flash('Phone must contain at least 10 digits', 'error')
                patient['_user'] = user
                return render_template('edit_patient.html', patient=patient)

            users_col.update_one({'_id': oid(patient['user_id'])}, {'$set': {
                'name':  escape(name),
                'email': email.lower(),
                'phone': phone
            }})
            patients_col.update_one({'_id': oid(pat_id)}, {'$set': {
                'address':     escape(address),
                'blood_group': blood_group
            }})
            flash('Patient updated successfully', 'success')
            return redirect(url_for('admin_patients'))
        except Exception as e:
            app.logger.error(f'Edit patient error: {e}')
            flash('An error occurred while updating patient', 'error')
            patient['_user'] = user
            return render_template('edit_patient.html', patient=patient)

    patient['_user'] = user
    return render_template('edit_patient.html', patient=patient)


@app.route('/admin/delete_patient/<pat_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def delete_patient(pat_id):
    if request.method != 'POST':
        flash('Invalid request method', 'error')
        return redirect(url_for('admin_patients'))
    patient = patients_col.find_one({'_id': oid(pat_id)})
    if patient:
        users_col.update_one({'_id': oid(patient['user_id'])}, {'$set': {'is_active': False}})
    flash('Patient deactivated successfully', 'success')
    return redirect(url_for('admin_patients'))


@app.route('/admin/appointments')
@login_required
@role_required('admin')
def admin_appointments():
    apts = list(appointments_col.find().sort([('date', -1), ('time', -1)]))
    for apt in apts:
        patient = patients_col.find_one({'_id': oid(apt['patient_id'])}) if apt.get('patient_id') else None
        doctor  = doctors_col.find_one({'_id': oid(apt['doctor_id'])}) if apt.get('doctor_id') else None
        apt['_patient_user'] = users_col.find_one({'_id': oid(patient['user_id'])}) if patient and patient.get('user_id') else None
        apt['_doctor_user']  = users_col.find_one({'_id': oid(doctor['user_id'])}) if doctor and doctor.get('user_id') else None
        apt['_doctor_dept']  = departments_col.find_one({'_id': oid(doctor['department_id'])}) if doctor and doctor.get('department_id') else None
    return render_template('admin_appointments.html', appointments=apts)


# ─── Routes: Doctor ───────────────────────────────────────────────────────────

@app.route('/doctor/dashboard')
@login_required
@role_required('doctor')
def doctor_dashboard():
    doctor = doctors_col.find_one({'user_id': session['user_id']})
    if not doctor:
        flash('Doctor profile not found. Please contact administrator.', 'error')
        return redirect(url_for('logout'))
    today_str    = date.today().strftime('%Y-%m-%d')
    week_end_str = (date.today() + timedelta(days=7)).strftime('%Y-%m-%d')

    upcoming_apts = list(appointments_col.find({
        'doctor_id': str_id(doctor['_id']),
        'date':      {'$gte': today_str, '$lte': week_end_str},
        'status':    'Booked'
    }).sort([('date', 1), ('time', 1)]))

    for apt in upcoming_apts:
        patient = patients_col.find_one({'_id': oid(apt['patient_id'])}) if apt.get('patient_id') else None
        apt['_patient_user'] = users_col.find_one({'_id': oid(patient['user_id'])}) if patient and patient.get('user_id') else None

    # Distinct patients for this doctor
    patient_ids = appointments_col.distinct('patient_id', {'doctor_id': str_id(doctor['_id'])})
    patients = []
    for pid in patient_ids:
        pat = patients_col.find_one({'_id': oid(pid)}) if pid else None
        if pat and pat.get('user_id'):
            pat['_user'] = users_col.find_one({'_id': oid(pat['user_id'])})
            if pat['_user']:  # Only append if user still exists
                patients.append(pat)

    doctor['_user'] = users_col.find_one({'_id': oid(doctor['user_id'])})
    dept = departments_col.find_one({'_id': oid(doctor['department_id'])})
    doctor['_dept'] = dept

    return render_template('doctor_dashboard.html',
                           doctor=doctor,
                           upcoming_appointments=upcoming_apts,
                           patients=patients)


@app.route('/doctor/availability', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def doctor_availability():
    doctor = doctors_col.find_one({'user_id': session['user_id']})
    if not doctor:
        flash('Doctor profile not found. Please contact administrator.', 'error')
        return redirect(url_for('logout'))
    today     = date.today()
    week_end  = today + timedelta(days=7)

    if request.method == 'POST':
        # Remove existing availability for the next 7 days
        today_str    = today.strftime('%Y-%m-%d')
        week_end_str = week_end.strftime('%Y-%m-%d')
        availabilities_col.delete_many({
            'doctor_id': str_id(doctor['_id']),
            'date':      {'$gte': today_str, '$lte': week_end_str}
        })

        for i in range(7):
            d = today + timedelta(days=i)
            date_str = d.strftime('%Y-%m-%d')

            morning_start = request.form.get(f'morning_start_{date_str}')
            morning_end   = request.form.get(f'morning_end_{date_str}')
            evening_start = request.form.get(f'evening_start_{date_str}')
            evening_end   = request.form.get(f'evening_end_{date_str}')

            if morning_start and morning_end:
                availabilities_col.insert_one({
                    'doctor_id':   str_id(doctor['_id']),
                    'date':        date_str,
                    'start_time':  morning_start,
                    'end_time':    morning_end,
                    'is_available': True
                })
            if evening_start and evening_end:
                availabilities_col.insert_one({
                    'doctor_id':   str_id(doctor['_id']),
                    'date':        date_str,
                    'start_time':  evening_start,
                    'end_time':    evening_end,
                    'is_available': True
                })

        flash('Availability updated successfully', 'success')
        return redirect(url_for('doctor_dashboard'))

    today_str    = today.strftime('%Y-%m-%d')
    week_end_str = week_end.strftime('%Y-%m-%d')
    avails = list(availabilities_col.find({
        'doctor_id': str_id(doctor['_id']),
        'date':      {'$gte': today_str, '$lte': week_end_str}
    }))

    availability_dict = {}
    for av in avails:
        ds = av['date']
        availability_dict.setdefault(ds, []).append(av)

    dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    return render_template('doctor_availability.html', dates=dates, availability_dict=availability_dict)


@app.route('/doctor/appointment/<apt_id>/complete', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def complete_appointment(apt_id):
    appointment = appointments_col.find_one({'_id': oid(apt_id)})
    if not appointment:
        flash('Appointment not found', 'error')
        return redirect(url_for('doctor_dashboard'))

    doctor = doctors_col.find_one({'user_id': session['user_id']})

    if appointment['doctor_id'] != str_id(doctor['_id']):
        flash('Access denied', 'error')
        return redirect(url_for('doctor_dashboard'))

    if request.method == 'POST':
        diagnosis    = request.form.get('diagnosis', '').strip()
        prescription = request.form.get('prescription', '').strip()
        notes        = request.form.get('notes', '').strip()

        if not diagnosis:
            flash('Diagnosis is required', 'error')
            return render_template('complete_appointment.html', appointment=appointment)
        
        diagnosis = escape(diagnosis)
        prescription = escape(prescription)
        notes = escape(notes)

        appointments_col.update_one({'_id': oid(apt_id)}, {'$set': {'status': 'Completed'}})
        treatments_col.insert_one({
            'appointment_id': apt_id,
            'diagnosis':      str(diagnosis),
            'prescription':   str(prescription),
            'notes':          str(notes),
            'created_at':     datetime.utcnow().isoformat()
        })

        flash('Appointment completed successfully', 'success')
        return redirect(url_for('doctor_dashboard'))

    patient = patients_col.find_one({'_id': oid(appointment['patient_id'])})
    appointment['_patient_user'] = users_col.find_one({'_id': oid(patient['user_id'])}) if patient else {}
    return render_template('complete_appointment.html', appointment=appointment)


@app.route('/doctor/patient_history/<pat_id>')
@login_required
@role_required('doctor')
def patient_history(pat_id):
    doctor  = doctors_col.find_one({'user_id': session['user_id']})
    patient = patients_col.find_one({'_id': oid(pat_id)})
    if not patient:
        flash('Patient not found', 'error')
        return redirect(url_for('doctor_dashboard'))

    apts = list(appointments_col.find({
        'patient_id': pat_id,
        'doctor_id':  str_id(doctor['_id']),
        'status':     'Completed'
    }).sort('date', -1))

    for apt in apts:
        patient = patients_col.find_one({'_id': oid(apt['patient_id'])}) if apt.get('patient_id') else None
        apt['_treatment'] = treatments_col.find_one({'appointment_id': str_id(apt['_id'])}) if apt.get('_id') else None

    patient['_user'] = users_col.find_one({'_id': oid(patient['user_id'])}) if patient.get('user_id') else None
    return render_template('patient_history.html', patient=patient, appointments=apts)


@app.route('/doctor/cancel_appointment/<apt_id>', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def doctor_cancel_appointment(apt_id):
    if request.method != 'POST':
        flash('Invalid request method', 'error')
        return redirect(url_for('doctor_dashboard'))
    
    appointment = appointments_col.find_one({'_id': oid(apt_id)})
    doctor = doctors_col.find_one({'user_id': session['user_id']})
    
    if not appointment:
        flash('Appointment not found', 'error')
        return redirect(url_for('doctor_dashboard'))
    
    if not doctor or appointment['doctor_id'] != str_id(doctor['_id']):
        flash('Access denied', 'error')
        return redirect(url_for('doctor_dashboard'))

    appointments_col.update_one({'_id': oid(apt_id)}, {'$set': {'status': 'Cancelled'}})
    flash('Appointment cancelled', 'success')
    return redirect(url_for('doctor_dashboard'))


# ─── Routes: Patient ──────────────────────────────────────────────────────────

@app.route('/patient/dashboard')
@login_required
@role_required('patient')
def patient_dashboard():
    patient = patients_col.find_one({'user_id': session['user_id']})
    if not patient:
        flash('Patient profile not found. Please contact administrator.', 'error')
        return redirect(url_for('logout'))

    today_str  = date.today().strftime('%Y-%m-%d')
    departments = list(departments_col.find())

    upcoming_apts = list(appointments_col.find({
        'patient_id': str_id(patient['_id']),
        'date':       {'$gte': today_str},
        'status':     'Booked'
    }).sort([('date', 1), ('time', 1)]))

    past_apts = list(appointments_col.find({
        'patient_id': str_id(patient['_id']),
        'status':     'Completed'
    }).sort('date', -1).limit(10))

    # Enrich with doctor info
    for apt in upcoming_apts + past_apts:
        doc = doctors_col.find_one({'_id': oid(apt['doctor_id'])}) if apt.get('doctor_id') else None
        apt['_doctor_user'] = users_col.find_one({'_id': oid(doc['user_id'])}) if doc and doc.get('user_id') else None
        apt['_treatment']   = treatments_col.find_one({'appointment_id': str_id(apt['_id'])}) if apt.get('_id') else None

    patient['_user'] = users_col.find_one({'_id': oid(patient['user_id'])})

    return render_template('patient_dashboard.html',
                           patient=patient,
                           departments=departments,
                           upcoming_appointments=upcoming_apts,
                           past_appointments=past_apts)


@app.route('/patient/doctors')
@login_required
@role_required('patient')
def patient_doctors():
    patient = patients_col.find_one({'user_id': session['user_id']})
    if not patient:
        flash('Patient profile not found. Please contact administrator.', 'error')
        return redirect(url_for('logout'))

    search  = request.args.get('search', '')
    dept_id = request.args.get('department', '')
    today_str    = date.today().strftime('%Y-%m-%d')
    week_end_str = (date.today() + timedelta(days=7)).strftime('%Y-%m-%d')

    all_doctors  = list(doctors_col.find())
    departments  = list(departments_col.find())
    doctors      = []

    for doc in all_doctors:
        user = users_col.find_one({'_id': oid(doc['user_id']), 'is_active': True})
        if not user:
            continue
        if dept_id and doc['department_id'] != dept_id:
            continue
        if search:
            s = search.lower()
            dept = departments_col.find_one({'_id': oid(doc['department_id'])})
            dept_name = dept['name'].lower() if dept else ''
            if s not in user['name'].lower() and s not in dept_name and \
               s not in doc.get('specialization', '').lower() and \
               s not in doc.get('qualification', '').lower():
                continue
        dept = departments_col.find_one({'_id': oid(doc['department_id'])})
        doc['_user'] = user
        doc['_dept'] = dept

        # Availability for next 7 days
        avails = list(availabilities_col.find({
            'doctor_id': str_id(doc['_id']),
            'date':      {'$gte': today_str, '$lte': week_end_str}
        }))
        doc['_availabilities'] = avails
        doctors.append(doc)

    return render_template('patient_doctors.html',
                           doctors=doctors,
                           departments=departments,
                           search=search,
                           selected_dept=dept_id)


@app.route('/patient/book_appointment/<doc_id>', methods=['GET', 'POST'])
@login_required
@role_required('patient')
def book_appointment(doc_id):
    doctor = doctors_col.find_one({'_id': oid(doc_id)})
    if not doctor:
        flash('Doctor not found', 'error')
        return redirect(url_for('patient_doctors'))

    patient = patients_col.find_one({'user_id': session['user_id']})
    if not patient:
        flash('Patient profile not found. Please contact administrator.', 'error')
        return redirect(url_for('logout'))

    if request.method == 'POST':
        try:
            date_str = request.form.get('date', '').strip()
            time_str = request.form.get('time', '').strip()

            if not date_str or not time_str:
                flash('Date and time are required', 'error')
                return redirect(url_for('book_appointment', doc_id=doc_id))

            # Validate date and time format
            if not validate_date_format(date_str):
                flash('Invalid date format', 'error')
                return redirect(url_for('book_appointment', doc_id=doc_id))

            if not validate_time_format(time_str):
                flash('Invalid time format', 'error')
                return redirect(url_for('book_appointment', doc_id=doc_id))

            # Validate date is not in past
            if datetime.strptime(date_str, '%Y-%m-%d').date() < date.today():
                flash('Cannot book appointment in the past', 'error')
                return redirect(url_for('book_appointment', doc_id=doc_id))

            # Validate time slot is within availability
            today_str = date.today().strftime('%Y-%m-%d')
            week_end_str = (date.today() + timedelta(days=7)).strftime('%Y-%m-%d')
            availability = availabilities_col.find_one({
                'doctor_id': doc_id,
                'date': date_str,
                'is_available': True
            })
            if not availability or time_str < availability['start_time'] or time_str > availability['end_time']:
                flash('Selected time is outside availability window', 'error')
                return redirect(url_for('book_appointment', doc_id=doc_id))

            # Check slot availability
            existing = appointments_col.find_one({
                'doctor_id': doc_id,
                'date':      date_str,
                'time':      time_str,
                'status':    'Booked'
            })
            if existing:
                flash('This slot is already booked', 'error')
                return redirect(url_for('book_appointment', doc_id=doc_id))

            appointments_col.insert_one({
                'patient_id': str_id(patient['_id']),
                'doctor_id':  doc_id,
                'date':       date_str,
                'time':       time_str,
                'status':     'Booked',
                'created_at': datetime.utcnow().isoformat()
            })
            flash('Appointment booked successfully', 'success')
            return redirect(url_for('patient_dashboard'))
        except Exception as e:
            app.logger.error(f'Book appointment error: {e}')
            flash('An error occurred while booking appointment', 'error')
            return redirect(url_for('book_appointment', doc_id=doc_id))

    today_str    = date.today().strftime('%Y-%m-%d')
    week_end_str = (date.today() + timedelta(days=7)).strftime('%Y-%m-%d')

    availabilities = list(availabilities_col.find({
        'doctor_id': doc_id,
        'date':      {'$gte': today_str, '$lte': week_end_str}
    }))
    booked = list(appointments_col.find({
        'doctor_id': doc_id,
        'date':      {'$gte': today_str, '$lte': week_end_str},
        'status':    'Booked'
    }))
    booked_slots = [(b['date'], b['time']) for b in booked]

    doctor['_user'] = users_col.find_one({'_id': oid(doctor['user_id'])})
    doctor['_dept'] = departments_col.find_one({'_id': oid(doctor['department_id'])})

    return render_template('book_appointment.html',
                           doctor=doctor,
                           availabilities=availabilities,
                           booked_slots=booked_slots)


@app.route('/patient/cancel_appointment/<apt_id>', methods=['GET', 'POST'])
@login_required
@role_required('patient')
def cancel_appointment(apt_id):
    if request.method != 'POST':
        flash('Invalid request method', 'error')
        return redirect(url_for('patient_dashboard'))
    
    patient = patients_col.find_one({'user_id': session['user_id']})
    if not patient:
        flash('Patient profile not found. Please contact administrator.', 'error')
        return redirect(url_for('logout'))

    appointment = appointments_col.find_one({'_id': oid(apt_id)})
    if not appointment or appointment['patient_id'] != str_id(patient['_id']):
        flash('Access denied', 'error')
        return redirect(url_for('patient_dashboard'))

    appointments_col.update_one({'_id': oid(apt_id)}, {'$set': {'status': 'Cancelled'}})
    flash('Appointment cancelled', 'success')
    return redirect(url_for('patient_dashboard'))


@app.route('/patient/reschedule_appointment/<apt_id>', methods=['GET', 'POST'])
@login_required
@role_required('patient')
def reschedule_appointment(apt_id):
    patient = patients_col.find_one({'user_id': session['user_id']})
    if not patient:
        flash('Patient profile not found. Please contact administrator.', 'error')
        return redirect(url_for('logout'))

    appointment = appointments_col.find_one({'_id': oid(apt_id)})
    if not appointment or appointment['patient_id'] != str_id(patient['_id']):
        flash('Access denied', 'error')
        return redirect(url_for('patient_dashboard'))

    if appointment['status'] != 'Booked':
        flash('Only booked appointments can be rescheduled', 'error')
        return redirect(url_for('patient_dashboard'))

    doctor = doctors_col.find_one({'_id': oid(appointment['doctor_id'])})
    doctor['_user'] = users_col.find_one({'_id': oid(doctor['user_id'])})
    doctor['_dept'] = departments_col.find_one({'_id': oid(doctor['department_id'])})

    if request.method == 'POST':
        try:
            new_date_str = request.form.get('date', '').strip()
            new_time_str = request.form.get('time', '').strip()

            if not new_date_str or not new_time_str:
                flash('Please select both date and time', 'error')
                return redirect(url_for('reschedule_appointment', apt_id=apt_id))

            # Validate date and time format
            if not validate_date_format(new_date_str):
                flash('Invalid date format', 'error')
                return redirect(url_for('reschedule_appointment', apt_id=apt_id))

            if not validate_time_format(new_time_str):
                flash('Invalid time format', 'error')
                return redirect(url_for('reschedule_appointment', apt_id=apt_id))

            # Validate date is not in past
            if datetime.strptime(new_date_str, '%Y-%m-%d').date() < date.today():
                flash('Cannot reschedule to a past date', 'error')
                return redirect(url_for('reschedule_appointment', apt_id=apt_id))

            if new_date_str == appointment['date'] and new_time_str == appointment['time']:
                flash('Please select a different date or time to reschedule', 'warning')
                return redirect(url_for('reschedule_appointment', apt_id=apt_id))

            # Validate new slot is within availability
            availability = availabilities_col.find_one({
                'doctor_id': appointment['doctor_id'],
                'date': new_date_str,
                'is_available': True
            })
            if not availability or new_time_str < availability['start_time'] or new_time_str > availability['end_time']:
                flash('Selected time is outside availability window', 'error')
                return redirect(url_for('reschedule_appointment', apt_id=apt_id))

            existing = appointments_col.find_one({
                'doctor_id': appointment['doctor_id'],
                'date':      new_date_str,
                'time':      new_time_str,
                'status':    'Booked',
                '_id':       {'$ne': oid(apt_id)}
            })
            if existing:
                flash('This slot is already booked. Please choose another time.', 'error')
                return redirect(url_for('reschedule_appointment', apt_id=apt_id))

            old_date = appointment['date']
            old_time = appointment['time']
            appointments_col.update_one({'_id': oid(apt_id)}, {'$set': {
                'date': new_date_str,
                'time': new_time_str
            }})
            flash(f'✅ Appointment rescheduled from {old_date} {old_time} to {new_date_str} {new_time_str}!', 'success')
            return redirect(url_for('patient_dashboard'))
        except Exception as e:
            app.logger.error(f'Reschedule error: {e}')
            flash('An error occurred while rescheduling appointment', 'error')
            return redirect(url_for('reschedule_appointment', apt_id=apt_id))

    today_str    = date.today().strftime('%Y-%m-%d')
    week_end_str = (date.today() + timedelta(days=7)).strftime('%Y-%m-%d')

    availabilities = list(availabilities_col.find({
        'doctor_id': appointment['doctor_id'],
        'date':      {'$gte': today_str, '$lte': week_end_str}
    }).sort([('date', 1), ('start_time', 1)]))

    booked = list(appointments_col.find({
        'doctor_id': appointment['doctor_id'],
        'date':      {'$gte': today_str, '$lte': week_end_str},
        'status':    'Booked',
        '_id':       {'$ne': oid(apt_id)}
    }))
    booked_slots = [(b['date'], b['time']) for b in booked]

    return render_template('reschedule_appointment.html',
                           appointment=appointment,
                           doctor=doctor,
                           availabilities=availabilities,
                           booked_slots=booked_slots,
                           timedelta=timedelta)


@app.route('/patient/profile', methods=['GET', 'POST'])
@login_required
@role_required('patient')
def patient_profile():
    patient = patients_col.find_one({'user_id': session['user_id']})
    if not patient:
        flash('Patient profile not found. Please contact administrator.', 'error')
        return redirect(url_for('logout'))

    if request.method == 'POST':
        try:
            name        = request.form.get('name', '').strip()
            email       = request.form.get('email', '').strip()
            phone       = request.form.get('phone', '').strip()
            address     = request.form.get('address', '').strip()
            blood_group = request.form.get('blood_group', '').strip()

            if not all([name, email, phone, address]):
                flash('Name, email, phone, and address are required', 'error')
                patient['_user'] = users_col.find_one({'_id': oid(patient['user_id'])})
                return render_template('patient_profile.html', patient=patient)

            if not validate_email(email):
                flash('Invalid email format', 'error')
                patient['_user'] = users_col.find_one({'_id': oid(patient['user_id'])})
                return render_template('patient_profile.html', patient=patient)

            if not validate_phone(phone):
                flash('Phone must contain at least 10 digits', 'error')
                patient['_user'] = users_col.find_one({'_id': oid(patient['user_id'])})
                return render_template('patient_profile.html', patient=patient)

            users_col.update_one({'_id': oid(patient['user_id'])}, {'$set': {
                'name':  escape(name),
                'email': email.lower(),
                'phone': phone
            }})
            patients_col.update_one({'_id': patient['_id']}, {'$set': {
                'address':     escape(address),
                'blood_group': blood_group
            }})
            flash('Profile updated successfully', 'success')
            return redirect(url_for('patient_dashboard'))
        except Exception as e:
            app.logger.error(f'Update profile error: {e}')
            flash('An error occurred while updating profile', 'error')
            patient['_user'] = users_col.find_one({'_id': oid(patient['user_id'])})
            return render_template('patient_profile.html', patient=patient)

    patient['_user'] = users_col.find_one({'_id': oid(patient['user_id'])})
    return render_template('patient_profile.html', patient=patient)


@app.route('/patient/treatment_history')
@login_required
@role_required('patient')
def treatment_history():
    patient = patients_col.find_one({'user_id': session['user_id']})
    if not patient:
        flash('Patient profile not found. Please contact administrator.', 'error')
        return redirect(url_for('logout'))

    apts = list(appointments_col.find({
        'patient_id': str_id(patient['_id']),
        'status':     'Completed'
    }).sort('date', -1))

    for apt in apts:
        doc = doctors_col.find_one({'_id': oid(apt['doctor_id'])}) if apt.get('doctor_id') else None
        apt['_doctor_user'] = users_col.find_one({'_id': oid(doc['user_id'])}) if doc and doc.get('user_id') else None
        apt['_doctor_dept']  = departments_col.find_one({'_id': oid(doc['department_id'])}) if doc and doc.get('department_id') else None
        apt['_treatment']   = treatments_col.find_one({'appointment_id': str_id(apt['_id'])}) if apt.get('_id') else None

    return render_template('treatment_history.html', appointments=apts)


# ─── API Routes ───────────────────────────────────────────────────────────────

@app.route('/api/doctors', methods=['GET'])
def api_doctors():
    result = []
    for doc in doctors_col.find():
        user = users_col.find_one({'_id': oid(doc['user_id']), 'is_active': True})
        if not user:
            continue
        dept = departments_col.find_one({'_id': oid(doc['department_id'])})
        result.append({
            'id':             str_id(doc['_id']),
            'name':           user['name'],
            'specialization': doc.get('specialization', ''),
            'department':     dept['name'] if dept else '',
            'experience':     doc.get('experience_years', 0)
        })
    return jsonify(result)


@app.route('/api/appointments', methods=['GET'])
def api_appointments():
    result = []
    for apt in appointments_col.find():
        patient = patients_col.find_one({'_id': oid(apt['patient_id'])}) if apt.get('patient_id') else None
        doctor  = doctors_col.find_one({'_id': oid(apt['doctor_id'])}) if apt.get('doctor_id') else None
        p_user  = users_col.find_one({'_id': oid(patient['user_id'])}) if patient and patient.get('user_id') else None
        d_user  = users_col.find_one({'_id': oid(doctor['user_id'])}) if doctor and doctor.get('user_id') else None
        result.append({
            'id':      str_id(apt['_id']),
            'patient': p_user.get('name', '') if p_user else '',
            'doctor':  d_user.get('name', '') if d_user else '',
            'date':    apt['date'],
            'time':    apt['time'],
            'status':  apt['status']
        })
    return jsonify(result)


@app.route('/api/appointment/<apt_id>', methods=['GET', 'PUT', 'DELETE'])
def api_appointment(apt_id):
    appointment = appointments_col.find_one({'_id': oid(apt_id)})
    if not appointment:
        return jsonify({'error': 'Not found'}), 404

    if request.method == 'GET':
        patient = patients_col.find_one({'_id': oid(appointment['patient_id'])}) if appointment.get('patient_id') else None
        doctor  = doctors_col.find_one({'_id': oid(appointment['doctor_id'])}) if appointment.get('doctor_id') else None
        p_user  = users_col.find_one({'_id': oid(patient['user_id'])}) if patient and patient.get('user_id') else None
        d_user  = users_col.find_one({'_id': oid(doctor['user_id'])}) if doctor and doctor.get('user_id') else None
        return jsonify({
            'id':      str_id(appointment['_id']),
            'patient': p_user.get('name', '') if p_user else '',
            'doctor':  d_user.get('name', '') if d_user else '',
            'date':    appointment['date'],
            'time':    appointment['time'],
            'status':  appointment['status']
        })

    elif request.method == 'PUT':
        data = request.get_json()
        if 'status' in data:
            appointments_col.update_one({'_id': oid(apt_id)}, {'$set': {'status': data['status']}})
        return jsonify({'message': 'Appointment updated'})

    elif request.method == 'DELETE':
        appointments_col.update_one({'_id': oid(apt_id)}, {'$set': {'status': 'Cancelled'}})
        return jsonify({'message': 'Appointment cancelled'})


# ─── Error Handlers ───────────────────────────────────────────────────────────

@app.errorhandler(404)
def page_not_found(error):
    flash('Page not found', 'error')
    return redirect(url_for('index'))


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error(f'Internal Server Error: {error}')
    flash('An internal server error occurred. Please try again.', 'error')
    return redirect(url_for('index'))


@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.error(f'Unhandled Exception: {error}', exc_info=True)
    flash('An unexpected error occurred. Please try again.', 'error')
    return redirect(url_for('index'))


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='127.0.0.1', port=5000)