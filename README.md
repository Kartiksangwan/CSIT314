# Talent Matching Platform

A job-matching web app with candidate and employer roles.
Built with Flask (Python) backend and MySQL database.

---

## Project Structure

```
project/
├── backend/
│   ├── app.py              ← main Flask app, run this
│   ├── database.py         ← SQLAlchemy setup
│   ├── models.py           ← all database models
│   ├── seed_db.py          ← run once to fill database with sample data
│   ├── requirements.txt
│   └── routes/
│       ├── auth.py         ← login, register, logout
│       ├── candidates.py   ← candidate profile, photo/resume upload
│       ├── employers.py    ← employer profile, view applicants
│       ├── jobs.py         ← post jobs, apply to jobs
│       ├── search.py       ← search candidates/jobs by keyword
│       ├── messages.py     ← messaging between users
│       ├── bookmarks.py    ← candidate saves jobs
│       ├── offers.py       ← employer sends interview offers
│       └── recommendations.py ← Top-K/Top-N matching algorithm
├── database/
│   ├── schema.sql          ← create tables manually (optional)
│   └── seed_data.sql       ← sample data reference (use seed_db.py instead)
└── frontend/
    ├── employers/          ← employer HTML pages
    └── candidates/         ← candidate HTML pages
```

---

## Setup Instructions

### 1. MySQL

Make sure MySQL is running. Create the database:

```bash
mysql -u root -p
```

```sql
CREATE DATABASE talent_matching;
EXIT;
```

### 2. Backend Setup

```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Database Connection

Open `backend/app.py` and update this line with your MySQL password:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:YOUR_PASSWORD@localhost/talent_matching'
```

### 4. Seed the Database

```bash
cd backend
python seed_db.py
```

This creates all tables and adds sample data.

### 5. Run the Backend

```bash
python app.py
```

The API runs at: http://localhost:5000

---

## Test Accounts

All passwords are `password123`

| Role      | Email                  |
|-----------|------------------------|
| Candidate | lucas@example.com      |
| Candidate | sophia@example.com     |
| Candidate | liam@example.com       |
| Candidate | mia@example.com        |
| Candidate | ryan@example.com       |
| Employer  | hr@brightnova.com      |
| Employer  | hr@flyhigh.com         |
| Employer  | hr@skycompany.com      |

---

## API Endpoints

### Auth
| Method | Endpoint             | Description          |
|--------|----------------------|----------------------|
| POST   | /api/auth/register   | Create account       |
| POST   | /api/auth/login      | Login                |
| POST   | /api/auth/logout     | Logout               |
| GET    | /api/auth/me         | Get logged in user   |

### Candidates
| Method | Endpoint                          | Description            |
|--------|-----------------------------------|------------------------|
| GET    | /api/candidates/profile           | Get my profile         |
| PUT    | /api/candidates/profile           | Update my profile      |
| POST   | /api/candidates/upload-photo      | Upload profile photo   |
| POST   | /api/candidates/upload-resume     | Upload resume PDF      |
| PUT    | /api/candidates/subscription      | Change subscription    |
| GET    | /api/candidates/<id>              | View a candidate       |

### Employers
| Method | Endpoint                          | Description            |
|--------|-----------------------------------|------------------------|
| GET    | /api/employers/profile            | Get my employer profile |
| PUT    | /api/employers/profile            | Update profile         |
| POST   | /api/employers/upload-logo        | Upload company logo    |
| GET    | /api/employers/applicants         | View all applicants    |
| GET    | /api/employers/<id>               | View an employer       |

### Jobs
| Method | Endpoint                          | Description            |
|--------|-----------------------------------|------------------------|
| GET    | /api/jobs/                        | List all active jobs   |
| GET    | /api/jobs/<id>                    | View a job             |
| POST   | /api/jobs/                        | Post a new job         |
| PUT    | /api/jobs/<id>                    | Edit a job             |
| DELETE | /api/jobs/<id>                    | Deactivate a job       |
| POST   | /api/jobs/<id>/apply              | Apply to a job         |
| GET    | /api/jobs/my-jobs                 | Employer's own jobs    |

### Search
| Method | Endpoint                          | Description                    |
|--------|-----------------------------------|--------------------------------|
| GET    | /api/search/candidates?keyword=x  | Employer searches candidates   |
| GET    | /api/search/jobs?keyword=x        | Candidate searches jobs        |
| GET    | /api/search/keywords-from-job     | Get keywords from a job post   |

### Messages
| Method | Endpoint                          | Description            |
|--------|-----------------------------------|------------------------|
| GET    | /api/messages/                    | Get all conversations  |
| GET    | /api/messages/thread/<partner_id> | Get a conversation     |
| POST   | /api/messages/send                | Send a message         |

### Bookmarks
| Method | Endpoint                          | Description            |
|--------|-----------------------------------|------------------------|
| GET    | /api/bookmarks/                   | Get saved jobs         |
| POST   | /api/bookmarks/add                | Save a job             |
| DELETE | /api/bookmarks/remove/<job_id>    | Remove a bookmark      |

### Offers
| Method | Endpoint                          | Description            |
|--------|-----------------------------------|------------------------|
| GET    | /api/offers/                      | Candidate views offers |
| POST   | /api/offers/send                  | Employer sends offer   |
| PUT    | /api/offers/<id>/respond          | Accept/reject offer    |
| GET    | /api/offers/employer              | Employer views offers  |

### Recommendations
| Method | Endpoint                                   | Description                   |
|--------|--------------------------------------------|-------------------------------|
| GET    | /api/recommendations/today                 | Top-N jobs for candidate      |
| GET    | /api/recommendations/top-candidates/<job_id> | Top-K candidates for job   |
| POST   | /api/recommendations/generate              | Pre-compute recommendations   |

---

## Frontend

Open any HTML file in the `frontend/` folder directly in your browser.
The frontend pages are static and are not yet wired to the backend API 
to connect them, update the JavaScript in each page to call `http://localhost:5000/api/...`

---

## Notes

- Sessions are used for auth (Flask sessions with cookie)
- Passwords are hashed with Werkzeug `pbkdf2:sha256`
- Match scoring is keyword-based (skills + location + work mode)
- File uploads go to `backend/uploads/`
