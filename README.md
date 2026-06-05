# Talent Matching Platform

A job-matching web platform with candidate and employer roles.
Built with Flask (Python) backend, MySQL database, and plain HTML/JS frontend.

---

## Project Structure

```
CSIT314/
├── backend/
│   ├── app.py                  ← main Flask app, run this to start the server
│   ├── database.py             ← SQLAlchemy setup
│   ├── models.py               ← all database models
│   ├── seed_db.py              ← run once to fill database with sample data
│   ├── requirements.txt        ← Python dependencies
│   └── routes/
│       ├── auth.py             ← login, register, logout
│       ├── candidates.py       ← candidate profile, photo/resume upload
│       ├── employers.py        ← employer profile, view applicants, membership
│       ├── jobs.py             ← post jobs, apply to jobs
│       ├── search.py           ← search candidates/jobs by keyword + filters
│       ├── messages.py         ← messaging between users
│       ├── bookmarks.py        ← candidate saves jobs
│       ├── offers.py           ← employer sends interview offers
│       └── recommendations.py  ← Top-K/Top-N matching (membership-aware)
├── database/
│   ├── schema.sql              ← run this first to create all tables
│   └── seed_data.sql           ← optional sample data
└── frontend/
    ├── api.js                  ← shared API helper (all fetch calls go here)
    ├── employers/              ← employer HTML pages
    └── candidates/             ← candidate HTML pages
```

---

## Prerequisites

Make sure you have these installed before starting:

- **Python 3.10+** - https://www.python.org/downloads/
- **MySQL 8+** - https://dev.mysql.com/downloads/mysql/
- **MySQL Workbench** (recommended) - https://dev.mysql.com/downloads/workbench/
- **VS Code** with the **Live Server** extension (by Ritwick Dey)

---

## Setup Instructions

### Step 1 - Create the database

Open MySQL Workbench, connect to your local server, and run:

```sql
CREATE DATABASE IF NOT EXISTS talent_matching;
```

Then open `database/schema.sql` in Workbench and run it.
This creates all the tables.

Optionally run `database/seed_data.sql` the same way to load sample data.

---

### Step 2 - Configure your database password

Open `backend/app.py` and find this line:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/talent_matching'
```

Change `root:root` to `YOUR_USERNAME:YOUR_PASSWORD` to match your MySQL login.

---

### Step 3 - Install Python dependencies

Open a terminal in the `backend/` folder and run:

```bash
pip install -r requirements.txt
```

---

### Step 4 - Start the backend server

Still inside `backend/`, run:

```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

**Leave this terminal running** - do not close it.

---

### Step 5 - Serve the frontend

The frontend must be served over HTTP (not opened as a file) so cookies work.

**Option A - VS Code Live Server (recommended)**
- Open the `frontend/` folder in VS Code
- Right-click `candidates/loginnC.html` → **Open with Live Server**
- Browser opens at `http://127.0.0.1:5500`

**Option B - Python**
```bash
cd frontend
python -m http.server 5500
```
Then open `http://127.0.0.1:5500/candidates/loginnC.html` in your browser.

---

## Key Pages

| Role | Page | URL |
|------|------|-----|
| Candidate | Login | `candidates/loginnC.html` |
| Candidate | Sign Up | `candidates/signup1C.html` |
| Candidate | My Page | `candidates/mypageC.html` |
| Candidate | Job Search | `candidates/jobsearch2C.html` |
| Candidate | Recommendations | `candidates/recomendationC.html` |
| Candidate | Subscription | `candidates/subcriptionC.html` |
| Employer | Login | `employers/companylogin.html` |
| Employer | Register | `employers/Companyinformation.html` |
| Employer | My Page | `employers/mypage.html` |
| Employer | Applicants | `employers/applicant.html` |
| Employer | Search Candidates | `employers/searchfrom.html` |
| Employer | Membership | `employers/membership.html` |
| Employer | Messages | `employers/message.html` |

---

## Test Accounts (if seed data was loaded)

All passwords are `password123`

| Role | Email |
|------|-------|
| Candidate | lucas@example.com |
| Candidate | sophia@example.com |
| Candidate | liam@example.com |
| Employer | hr@brightnova.com |
| Employer | hr@flyhigh.com |
| Employer | hr@skycompany.com |

---

## Features

### Candidate
- Register / Login / Logout
- Edit profile - name, job title, skills, education, location, work mode, bio
- Today's Recommendations - Top-N job matches scored by skills, location, work mode
- Search jobs - by keyword, location, work mode filter
- Apply to jobs
- Bookmark / save jobs
- View and respond to interview offers (accept / reject)
- Message employers
- Subscription plans - Free (top 10 recommendations) or Premium (unlimited)

### Employer
- Register with company info and first job posting
- Edit company profile
- Post new jobs
- View applicants with match scores
- Send interview offers to candidates
- Search candidates by skill keyword
- Message candidates directly from Applicant or Search page
- Membership plans - Free (top 10 candidate recommendations) or Premium (unlimited)

### Matching Algorithm
- Skill keyword matching (60 points max)
- Location match (20 points)
- Work mode match (20 points)
- Membership-aware: free users see top 10, premium users see all matches

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Not logged in" on every page | Open via `http://` not `file://` - use Live Server |
| MySQL connection error | Check username/password in `backend/app.py` |
| Port 5000 already in use | Change `port=5000` in `app.py` and `BASE_URL` in `frontend/api.js` |
| Module not found | Run `pip install -r requirements.txt` again |
| Tables don't exist | Run `database/schema.sql` in MySQL Workbench first |

---

## API Overview

| Area | Base Path |
|------|-----------|
| Auth | `/api/auth/` |
| Candidates | `/api/candidates/` |
| Employers | `/api/employers/` |
| Jobs | `/api/jobs/` |
| Search | `/api/search/` |
| Messages | `/api/messages/` |
| Bookmarks | `/api/bookmarks/` |
| Offers | `/api/offers/` |
| Recommendations | `/api/recommendations/` |

Full API runs at `http://127.0.0.1:5000`mode)
