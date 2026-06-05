# Capapool — Intelligent Talent Matching Platform

Capapool is a Django-based recruitment web application developed for the **CSIT314 Software Development Methodologies Group Project**. The system is designed to improve the recruitment process by supporting two-way matching between **candidates looking for jobs** and **employers looking for suitable candidates**.

The application allows candidates to create detailed profiles, search for jobs, and receive recommended job postings. Employers can create job postings, browse/search candidate profiles, and receive recommended candidates for their job vacancies. The system also supports membership-based recommendation limits, improved search filters, and basic fuzzy matching.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Main Features](#main-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [PostgreSQL Database Setup](#postgresql-database-setup)
- [Running the Application](#running-the-application)
- [Creating Test Data](#creating-test-data)
- [User Roles](#user-roles)
- [Important URLs](#important-urls)
- [Membership Feature](#membership-feature)
- [Search and Filtering](#search-and-filtering)
- [Recommendation System](#recommendation-system)
- [Testing Checklist](#testing-checklist)
- [Git and Version Control](#git-and-version-control)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [Team Notes](#team-notes)

---

## Project Overview

Traditional recruitment platforms often require candidates and employers to manually search through large amounts of information. This can be time-consuming and may lead to poor matches between job requirements and candidate qualifications.

Capapool aims to solve this problem by providing an intelligent talent matching platform where:

- Candidates can create profiles and receive job recommendations.
- Employers can create job postings and receive candidate recommendations.
- Search and filtering features help users find relevant results more quickly.
- Membership users receive unlimited recommendations, while non-members receive a maximum of 10 recommendations.

The project follows a simple but functional full-stack structure using Django, PostgreSQL, HTML, CSS, and JavaScript.

---

## Main Features

### Candidate Features

- Candidate registration and login
- Candidate profile creation and editing
- Candidate profile fields include:
  - Full name
  - Contact email
  - Phone number
  - Education level
  - Major/field of study
  - Years of experience
  - Work experience
  - Skills
  - Preferred working mode
  - Preferred location
  - Resume upload
  - Membership status
- Browse available jobs
- Search and filter jobs
- View recommended jobs
- Membership-based recommendation limits

### Employer Features

- Employer registration and login
- Employer/company profile creation
- Create job postings
- Edit own job postings
- View own job postings through **My Jobs**
- Browse candidate profiles
- Search and filter candidates
- View recommended candidates for own job postings
- Membership-based recommendation limits

### Admin Features

- Manage users
- Manage candidate profiles
- Manage employer profiles
- Manage skills
- Manage job postings
- Toggle membership status for candidates and employers

---

## Technology Stack

| Area | Technology |
|---|---|
| Backend | Python, Django |
| Database | PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| Version Control | Git and GitHub |
| Development Methodology | Agile/Scrum-inspired workflow |

---

## Project Structure

The project follows a Django app-based structure:

```text
capapool/
│
├── accounts/              # Login, logout, registration, dashboard
├── candidates/            # Candidate profiles, candidate search, candidate forms
├── employers/             # Employer/company profiles
├── jobs/                  # Job postings, job search, employer job management
├── recommendations/       # Recommendation scoring logic and recommendation views
├── templates/             # HTML templates
├── static/                # CSS, JavaScript, images and frontend assets
├── media/                 # Uploaded files such as resumes, if enabled locally
├── capapool/              # Main Django project settings and URLs
├── manage.py
└── README.md
```

---

## Prerequisites

Before running the project, make sure the following are installed:

### Required

- Python 3.10 or newer
- pip
- Git
- PostgreSQL
- A code editor such as VS Code

### Recommended

- pgAdmin or another PostgreSQL database viewer
- Virtual environment for Python dependencies

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/starkiller08/capapool.git
cd capapool
```

If you need a specific branch:

```bash
git checkout main
```

---

### 2. Create a Virtual Environment

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Dependencies

If the project has a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

If dependencies need to be installed manually, install Django and PostgreSQL driver:

```bash
pip install django psycopg2-binary
```

---

## PostgreSQL Database Setup

This project uses PostgreSQL as the database.

### 1. Create a PostgreSQL Database

Open the PostgreSQL shell or pgAdmin and create a database:

```sql
CREATE DATABASE capapool_db;
```

You can use another database name, but make sure it matches the database settings in `settings.py`.

---

### 2. Configure Django Database Settings

Open:

```text
capapool/settings.py
```

Check the `DATABASES` section. It should look similar to this:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'capapool_db',
        'USER': 'postgres',
        'PASSWORD': 'your_postgres_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Replace:

```text
your_postgres_password
```

with your actual PostgreSQL password.

> Important: Do not commit real passwords to a public repository in production. For this university prototype, local settings may be used, but environment variables are recommended for a real deployment.

---

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the required database tables in PostgreSQL.

---

### 4. Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

---

## Running the Application

Start the Django development server:

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

Open the Django admin panel:

```text
http://127.0.0.1:8000/admin/
```

---

## Creating Test Data

To properly test the system, create sample data using the Django admin panel.

Recommended test data:

### Users

Create at least:

- 1 admin/superuser
- 2 candidate users
- 2 employer users

### Skills

Create skills such as:

- Python
- Django
- SQL
- JavaScript
- Cybersecurity
- Data Analysis
- Communication
- Project Management

### Candidate Profiles

Each candidate should have:

- Education level
- Major
- Years of experience
- Work experience
- Skills
- Preferred location
- Preferred work mode
- Membership status

### Employer Profiles

Each employer should have:

- Company name
- Company description
- Contact details
- Membership status

### Job Postings

Each job should include:

- Job title
- Job description
- Required education level
- Required skills
- Required years of experience
- Work mode
- Job location
- Active status

---

## User Roles

### Candidate

Candidates can:

- Register and log in
- View their dashboard
- View and edit their own profile
- Browse and search jobs
- View recommended jobs

Candidates cannot:

- Create job postings
- Edit employer job postings
- View employer-only recommendation pages

---

### Employer

Employers can:

- Register and log in
- View their dashboard
- Create job postings
- View their own jobs
- Edit their own jobs
- Search candidates
- View recommended candidates for their own jobs

Employers cannot:

- Edit candidate profiles
- View candidate-only recommendation pages
- Edit jobs owned by other employers

---

### Admin

Admins can:

- Access the Django admin panel
- Manage users
- Manage candidate and employer profiles
- Manage job postings
- Manage skills
- Toggle membership status

---

## Important URLs

| Page | URL |
|---|---|
| Home | `/` |
| Dashboard | `/dashboard/` |
| Admin Panel | `/admin/` |
| Candidate Registration | `/accounts/register/candidate/` |
| Employer Registration | `/accounts/register/employer/` |
| Login | `/accounts/login/` |
| Logout | `/accounts/logout/` |
| Job List | `/jobs/` |
| Job Search | `/jobs/search/` |
| Create Job | `/jobs/create/` |
| My Jobs | `/jobs/my-jobs/` |
| Candidate List | `/candidates/` |
| Candidate Search | `/candidates/search/` |
| My Candidate Profile | `/candidates/my-profile/` |
| Edit My Candidate Profile | `/candidates/my-profile/edit/` |
| Recommended Jobs | `/recommendations/jobs/` |
| Recommended Candidates | `/recommendations/candidates/<job_id>/` |

---

## Membership Feature

The system supports membership for both candidates and employers.

### Candidate Membership

- Member candidates receive unlimited recommended jobs.
- Non-member candidates receive a maximum of 10 recommended jobs.

### Employer Membership

- Member employers receive unlimited recommended candidates.
- Non-member employers receive a maximum of 10 recommended candidates.

Membership status can be managed through the Django admin panel using the `is_member` field.

---

## Search and Filtering

The application includes improved search functionality for both jobs and candidates.

### Job Search

Job search supports:

- Keyword search
- Location filter
- Work mode filter
- Education filter
- Experience filter
- Keyword + filter combination
- Basic fuzzy matching for typo tolerance

Search considers fields such as:

- Job title
- Job description
- Job location
- Work mode
- Employer/company name
- Employer/company description
- Required skills

---

### Candidate Search

Candidate search supports:

- Keyword search
- Skill filter
- Education filter
- Experience filter
- Preferred location filter
- Preferred work mode filter
- Keyword + filter combination
- Basic fuzzy matching for typo tolerance

Search considers fields such as:

- Candidate name
- Email
- Major
- Work experience
- Preferred location
- Preferred work mode
- Skills

---

## Recommendation System

The recommendation system uses a simple weighted scoring method.

The score considers:

- Skill match
- Education match
- Years of experience
- Location match
- Work mode match

The result is sorted by match score, with the most relevant jobs/candidates appearing first.

### Candidate Recommendations

Candidates can view recommended jobs at:

```text
/recommendations/jobs/
```

### Employer Recommendations

Employers can view recommended candidates for a job at:

```text
/recommendations/candidates/<job_id>/
```

Example:

```text
/recommendations/candidates/1/
```

---

## Testing Checklist

Before submission or demo, test the following:

### General

- Home page loads
- Login works
- Logout works
- Dashboard loads correctly
- PostgreSQL is connected

### Candidate Flow

- Candidate can register
- Candidate can log in
- Candidate dashboard shows candidate options
- Candidate can view own profile
- Candidate can edit own profile
- Candidate cannot edit another candidate's profile
- Candidate can search jobs
- Candidate can view recommended jobs

### Employer Flow

- Employer can register
- Employer can log in
- Employer dashboard shows employer options
- Employer can create job postings
- Employer can view own jobs
- Employer can edit own jobs
- Employer cannot edit other employers' jobs
- Employer can search candidates
- Employer can view recommended candidates

### Admin Flow

- Admin can log in
- Admin can access `/admin/`
- Admin can manage users
- Admin can toggle membership
- Admin can manage job and candidate data

### Requirement Change Tests

- Candidate work experience is stored and displayed
- Candidate preferred location is stored and displayed
- Candidate preferred work mode is stored and displayed
- Candidate skills are stored and used in matching
- Candidate membership affects number of recommendations
- Employer membership affects number of recommendations
- Search supports keywords
- Search supports filters
- Search supports keyword + filter combination
- Fuzzy search handles simple typos

---

## Git and Version Control

Useful Git commands:

### Check current branch

```bash
git branch
```

### Check status

```bash
git status
```

### Add and commit changes

```bash
git add .
git commit -m "Your commit message"
```

### Push changes

```bash
git push
```

### View commit history

```bash
git log --oneline
```

### View branch graph

```bash
git log --oneline --graph --all --decorate
```

---

## Troubleshooting

### PostgreSQL connection error

Check that PostgreSQL is running and the database settings in `settings.py` are correct.

Common things to check:

- Database name
- Username
- Password
- Host
- Port

---

### Login redirects to `/accounts/profile/`

Make sure these settings are uppercase in `settings.py`:

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'
```

Django settings are case-sensitive.

---

### CSRF error on logout

Make sure logout uses a POST form with CSRF token:

```html
<form action="{% url 'logout' %}" method="post">
    {% csrf_token %}
    <button type="submit">Logout</button>
</form>
```

---

### Test users cannot log in

If test users were created without passwords, set their passwords properly:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

user = User.objects.get(username='candidate1')
user.set_password('test12345')
user.is_active = True
user.save()
```

---

### No recommendations appear

Check that:

- Candidate profiles exist
- Job postings exist
- Job postings are active
- Skills are assigned to candidates and jobs
- The logged-in user has the correct candidate/employer profile

---

### Static files not loading

Make sure `settings.py` has:

```python
STATIC_URL = 'static/'
```

If using a custom static folder, also check:

```python
STATICFILES_DIRS = [BASE_DIR / 'static']
```

---

## Future Improvements

Possible improvements for future development:

- Better frontend styling and responsive design
- Better fuzzy search using PostgreSQL trigram similarity
- Resume text parsing
- Job application workflow
- Employer shortlisting workflow
- Candidate saved jobs
- Email notifications
- Membership payment simulation
- More advanced recommendation algorithm
- Unit tests and integration tests
- Deployment to a cloud platform

---

## Team Notes

This project was developed as part of the CSIT314 Software Development Methodologies group project. The system demonstrates a full-stack Django web application with database-backed user roles, search, filtering, recommendations, and requirement-change handling.

---

## License

This project is for academic purposes.
