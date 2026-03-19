# MBA Application

A comprehensive Django-based MBA administrative application for managing students, supervisors, projects, and academic workflows.

## Deployment

**Live URL**: https://mba-app-ko03.onrender.com

**Status**: ✅ Deployed on Render with PostgreSQL

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Blessing-Mbalaka/MBA_APP.git
   cd MBA_APP
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database configuration**
   - Update `.env` with your database credentials
   - Run migrations: `python manage.py migrate`
   - Create test data: `python manage.py inject_test_data_comprehensive --clean`

5. **Run development server**
   ```bash
   python manage.py runserver
   ```

Access the app at: `http://127.0.0.1:8000`

---

## Easy to Run Settings

### One-Command Setup (Development)
```bash
# Windows PowerShell
& ".\venv\Scripts\Activate.ps1"; pip install -r requirements.txt; python manage.py migrate; python manage.py inject_test_data_comprehensive --clean; python manage.py runserver

# Linux/Mac
source venv/bin/activate && pip install -r requirements.txt && python manage.py migrate && python manage.py inject_test_data_comprehensive --clean && python manage.py runserver
```

### Quick Setup Scripts

**Windows (PowerShell):**
```powershell
# Run once to setup everything
.\setup_and_run.ps1
```

**Linux/Mac (Bash):**
```bash
# Run once to setup everything
bash setup_and_run.sh
```

### Pre-Configured .env Template

Copy and save as `.env` in the project root:
```
# Django
DEBUG=True
DJANGO_SETTINGS_MODULE=mysite.settings
PYTHONUNBUFFERED=true
SECRET_KEY=your-secret-key-here

# Local Development Database (SQLite - default)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Production Database (PostgreSQL on Render)
# Uncomment to use Render PostgreSQL
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=mba_ieux
# DB_USER_NAME=mba_ieux_user
# DB_PASSWORD=your_password
# DB_HOST=dpg-d6phcdngi27c738f02sg-a.oregon-postgres.render.com
# DB_PORT=5432

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False

# Application Settings
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

### Useful Quick Commands

```bash
# Activate virtual environment
source venv/bin/activate              # Linux/Mac
venv\Scripts\activate                 # Windows CMD
& ".\venv\Scripts\Activate.ps1"       # Windows PowerShell

# Database setup
python manage.py migrate

# Create comprehensive test data
python manage.py inject_test_data_comprehensive --clean

# Create specific test data
python manage.py inject_test_data_intent --clean      # Intent test data
python manage.py inject_test_data_nomination --clean  # Nomination test data

# Run development server
python manage.py runserver

# Run tests
python systemtest.py

# Reset and restart (clean slate)
rm db.sqlite3 && python manage.py migrate && python manage.py inject_test_data_comprehensive --clean
```

### Development Setup Presets

**For Local Testing:**
```bash
python manage.py migrate
python manage.py inject_test_data_comprehensive --clean
python manage.py runserver
```

**For Feature Development:**
```bash
python manage.py migrate
python manage.py runserver --nothreading  # Useful for debugging
```

**For Database-Only Testing:**
```bash
python manage.py migrate
# Use shell for manual testing
python manage.py shell
```

---

## Test User Credentials

### Login URL
`https://mba-app-ko03.onrender.com/signin` (or local: `http://127.0.0.1:8000/signin`)

### Admin Users
| Email | Password | Role |
|-------|----------|------|
| mainAdmin@test.com | mainAdmin@123 | Main Admin |
| admin@test.com | admin@123 | Admin |
| hdc@test.com | hdc@123 | HDC |
| examiner@test.com | examiner@123 | Examiner |

### Test Supervisors (5)
| Email | Password | Skills |
|-------|----------|--------|
| supervisor_1@test.mba.local | testpass123 | Machine Learning, Data Science |
| supervisor_2@test.mba.local | testpass123 | Cloud Computing, DevOps |
| supervisor_3@test.mba.local | testpass123 | Cybersecurity, Network Architecture |
| supervisor_4@test.mba.local | testpass123 | Business Analytics, Finance |
| supervisor_5@test.mba.local | testpass123 | Digital Marketing, Brand Strategy |

### Test Students (15)
| Email | Password | Status |
|-------|----------|--------|
| student_1@test.mba.local | testpass123 | Project Created |
| student_2@test.mba.local | testpass123 | HDC Submitted |
| student_3@test.mba.local | testpass123 | JBS5 Submitted |
| student_4@test.mba.local | testpass123 | Project Created |
| ... | testpass123 | Rotating Status |
| student_15@test.mba.local | testpass123 | JBS5 Submitted |

### Special Test Cases
| Student | Email | Purpose |
|---------|-------|---------|
| Tobey Mbatoa | tobey.mbatoa@test.mba.local | Intent Form Testing |
| (inject_test_student) | student_*@test.mba.local | Nomination Form Testing |

---

## Key Features

- **Student Management**: Track student profiles, projects, and workflow progress
- **Supervisor Management**: Allocate supervisors to students and manage supervision
- **Project Workflow**: Multi-stage project submission and approval process
- **Forms**: Intent forms, nomination forms, JBS5/JBS10 forms
- **Email Integration**: Automated email notifications
- **Admin Dashboard**: Comprehensive management interface
- **Role-Based Access**: Different permissions for students, supervisors, admins, HDC

---

## Management Commands

### Create Test Data
```bash
# All test data with --clean flag (removes old data first)
python manage.py inject_test_data_comprehensive --clean
python manage.py inject_test_data_intent --clean
python manage.py inject_test_data_nomination

# Or individually without cleaning
python manage.py inject_test_data_comprehensive
python manage.py inject_test_data_intent
python manage.py inject_test_data_nomination
```

### Create Basic Users
```bash
python manage.py create_test_users --clean
```

### Populate Disciplines
```bash
python manage.py populate_disciplines
```

---

## Database

- **Local**: SQLite (development)
- **Production (Render)**: PostgreSQL
  - Host: `dpg-d6phcdngi27c738f02sg-a.oregon-postgres.render.com`
  - Database: `mba_ieux`

---

## Tech Stack

- **Backend**: Django 5.2.3
- **Database**: PostgreSQL (Render) / SQLite (Local)
- **Server**: Gunicorn (Render) / Django Dev Server (Local)
- **Static Files**: WhiteNoise
- **Email**: Gmail SMTP
- **Task Queue**: Celery (optional)

---

## Environment Variables

Create `.env` file with:
```
DJANGO_SETTINGS_MODULE=mysite.settings
PYTHONUNBUFFERED=true

# Database (Online - Render)
DB_NAME=mba_ieux
DB_USER_NAME=mba_ieux_user
DB_PASSWORD=<your_password>
DB_HOST=dpg-d6phcdngi27c738f02sg-a.oregon-postgres.render.com
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=lads22359@gmail.com
EMAIL_HOST_PASSWORD=<your_app_password>
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
```

---

## Common Issues

### Database Connection Refused
Ensure `.env` points to the correct database and it's accessible.

### Static Files Not Loading
Run: `python manage.py collectstatic --noinput`

### Missing Dependencies
Run: `pip install -r requirements.txt`

---

## Support

For issues or questions, check the logs or run: `python manage.py shell`

---

**Last Updated**: March 12, 2026
**Version**: 1.0.0
**Status**: Production Ready ✅




