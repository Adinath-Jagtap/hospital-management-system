# ⚡ Quick Start Guide

Get the Hospital Management System running in **5 minutes**!

---

## 🚀 Local Development (Quickest Way)

### 1. Install Python & Git (if not already installed)

Download and install:

- Python 3.8+: https://www.python.org/downloads/
- Git: https://git-scm.com/download/

### 2. Clone Repository

```bash
git clone https://github.com/yourusername/hospital-management-system.git
cd hospital-management-system
```

### 3. Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Create .env File

```bash
# Create .env file
type nul > .env  # Windows
# or
touch .env  # macOS/Linux

# Add this to .env:
SECRET_KEY=dev-key-change-in-production
MONGO_URI=mongodb://localhost:27017/hospital
```

### 6. Start MongoDB

```bash
# Option A: If MongoDB is installed locally
mongod

# Option B: Use MongoDB Atlas (cloud)
# Update MONGO_URI in .env with your MongoDB Atlas connection string
```

### 7. Run Application

```bash
python app.py
```

### 8. Access Application

Open browser and go to: **http://localhost:5000**

### 9. Default Login

```
Username: admin
Password: admin123
```

---

## 📝 First Steps After Login

### As Admin:

1. **Change Admin Password** (⚠️ Required)

   - Click Settings/Profile
   - Update password to something secure
2. **Add a Doctor**

   - Go to "Manage Doctors"
   - Click "Add New Doctor"
   - Fill in doctor details
3. **View Patients**

   - Go to "Manage Patients"
   - See registered patients

### As Patient (Test User):

1. **Register**

   - Click "Register" on login page
   - Fill form (password needs: 8+ chars, 1 uppercase, 1 digit)
   - Submit and login
2. **Browse Doctors**

   - Click "Available Doctors"
   - Filter by department
   - View doctor info and availability
3. **Book Appointment**

   - Select a doctor
   - Choose date/time
   - Confirm booking
4. **View Appointments**

   - Dashboard shows upcoming appointments
   - Can reschedule or cancel

### As Doctor:

1. **Set Availability**

   - Click "Set Availability"
   - Choose morning/evening slots for next 7 days
   - Save
2. **View Appointments**

   - Dashboard shows upcoming appointments
   - View patient list
3. **Complete Appointment**

   - Click appointment
   - Add diagnosis and prescription
   - Mark as completed

---

## 🐛 Quick Troubleshooting

### MongoDB Connection Error

```
Error: Could not connect to MongoDB
```

**Fix**: Ensure MongoDB service is running (`mongod` command)

### Port Already in Use

```
Error: Address already in use
```

**Fix**: Change port in app.py or kill process using port 5000

### Module Not Found

```
Error: No module named 'flask'
```

**Fix**: Run: `pip install -r requirements.txt`

### .env File Not Working

**Fix**:

- Ensure .env is in project root folder
- Restart Flask app after creating/editing .env

---

## 📦 Using MongoDB Atlas (Cloud Database)

Instead of local MongoDB:

1. Go to https://www.mongodb.com/atlas
2. Create free account
3. Create cluster (free tier available)
4. Get connection string
5. Update `.env`:
   ```
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/hospital?retryWrites=true&w=majority
   ```
6. Restart Flask app

---

## 📤 Deploy to Render (Free)

See **DEPLOYMENT_GUIDE.md** for detailed instructions.

Quick version:

1. Push code to GitHub
2. Go to https://render.com
3. Create new Web Service from GitHub repo
4. Add environment variables (SECRET_KEY, MONGO_URI)
5. Deploy (3-5 minutes)

---

## 🎨 Customize the UI

Edit templates in `templates/` folder:

- `base.html` - Navigation and layout
- `hospital.css` - Styling in `static/css/`
- Modify and refresh browser to see changes

---

## 📚 Learn More

- **Full README**: See `README.md`
- **Deployment**: See `DEPLOYMENT_GUIDE.md`
- **API Docs**: In `README.md` under API Documentation

---

## 💡 Pro Tips

1. **Use MongoDB Atlas for cloud database** - no local setup needed
2. **Create multiple test accounts** - try different roles
3. **Check browser console** (F12) for errors
4. **Use Firefox/Chrome DevTools** for debugging
5. **Keep admin password safe** - change from default

---

## ✅ What's Next?

- [ ] Get application running locally
- [ ] Test with sample data
- [ ] Customize UI/styling
- [ ] Deploy to Render
- [ ] Change admin password
- [ ] Share with team

---

**Need Help?**

- Check README.md for detailed docs
- See DEPLOYMENT_GUIDE.md for deployment issues
- Check app logs: `python app.py` shows errors
- MongoDB docs: https://docs.mongodb.com

**Happy Coding! 🎉**
