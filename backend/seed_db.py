"""
Run this script once to set up the database with sample data.
It handles password hashing properly using Werkzeug.

Usage:
    cd backend
    python seed_db.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app
from database import db
from models import User, Candidate, Employer, Job, Application, Bookmark, Message, Offer, Recommendation


def seed():
    with app.app_context():
        # Drop and recreate all tables
        db.drop_all()
        db.create_all()
        print("Tables created.")

        # ---- USERS ----
        # Candidates
        u1 = User(email='lucas@example.com', role='candidate')
        u1.set_password('password123')

        u2 = User(email='sophia@example.com', role='candidate')
        u2.set_password('password123')

        u3 = User(email='liam@example.com', role='candidate')
        u3.set_password('password123')

        u4 = User(email='mia@example.com', role='candidate')
        u4.set_password('password123')

        u5 = User(email='ryan@example.com', role='candidate')
        u5.set_password('password123')

        # Employers
        u6 = User(email='hr@brightnova.com', role='employer')
        u6.set_password('password123')

        u7 = User(email='hr@flyhigh.com', role='employer')
        u7.set_password('password123')

        u8 = User(email='hr@skycompany.com', role='employer')
        u8.set_password('password123')

        db.session.add_all([u1, u2, u3, u4, u5, u6, u7, u8])
        db.session.flush()
        print("Users created.")

        # ---- CANDIDATE PROFILES ----
        c1 = Candidate(user_id=u1.id, full_name='Lucas Johnson', job_title='Frontend Developer',
                       bio='I have experience in Java, Python, and mobile app development. Worked on team projects involving UI/UX design and database integration.',
                       skills='JavaScript, HTML/CSS, React, Git, UI/UX Design, Communication',
                       education='Bachelor of Computer Science', experience_years='2 years',
                       location='Brisbane, QLD', work_mode='Hybrid', subscription='basic')

        c2 = Candidate(user_id=u2.id, full_name='Sophia Turner', job_title='Frontend Developer',
                       bio='Passionate about responsive web design and clean UI.',
                       skills='JavaScript, HTML/CSS, UI/UX Design, Git, Communication',
                       education='Bachelor of Information Technology', experience_years='2 years',
                       location='Brisbane, QLD', work_mode='Remote', subscription='free')

        c3 = Candidate(user_id=u3.id, full_name='Liam Carter', job_title='Junior Web Developer',
                       bio='Fresh graduate with solid fundamentals in web development.',
                       skills='JavaScript, HTML/CSS, Git, Team Collaboration, Communication',
                       education='Bachelor of IT', experience_years='1-2 years',
                       location='Sydney, NSW', work_mode='Remote', subscription='free')

        c4 = Candidate(user_id=u4.id, full_name='Mia Chen', job_title='Full Stack Developer',
                       bio='Full stack developer comfortable with Python and JavaScript.',
                       skills='Python, JavaScript, SQL, Git, React, Django',
                       education='Bachelor of Software Engineering', experience_years='3 years',
                       location='Melbourne, VIC', work_mode='On-site', subscription='premium')

        c5 = Candidate(user_id=u5.id, full_name='Ryan Chen', job_title='Junior Web Developer',
                       bio='Team player with solid Git skills and growing JavaScript experience.',
                       skills='JavaScript, Git, HTML/CSS, Team Collaboration',
                       education='Bachelor of Computer Science', experience_years='1-2 years',
                       location='Brisbane, QLD', work_mode='Remote', subscription='free')

        db.session.add_all([c1, c2, c3, c4, c5])
        db.session.flush()
        print("Candidate profiles created.")

        # ---- EMPLOYER PROFILES ----
        e1 = Employer(user_id=u6.id, company_name='BrightNova Digital',
                      company_info='BrightNova Digital is a technology company specializing in responsive web applications and modern UI development for startups.')

        e2 = Employer(user_id=u7.id, company_name='Fly High Company',
                      company_info='Fly High is a growing tech startup focused on mobile and web products for the aviation industry.')

        e3 = Employer(user_id=u8.id, company_name='Sky Company',
                      company_info='Sky Company builds cloud-based SaaS tools for SMBs across Australia.')

        db.session.add_all([e1, e2, e3])
        db.session.flush()
        print("Employer profiles created.")

        # ---- JOBS ----
        j1 = Job(employer_id=e1.id, job_title='Frontend Web Developer',
                 job_description='Develop and maintain responsive web interfaces using JavaScript and collaborate with designers.',
                 required_skills='JavaScript, HTML/CSS, Git, UI/UX Design, Communication',
                 required_education='Bachelor in Computer Science, IT, or related field',
                 experience_years='1-2 years', work_mode='Remote', location='Brisbane, QLD',
                 salary='$65,000 - $80,000', is_active=True)

        j2 = Job(employer_id=e1.id, job_title='React Developer',
                 job_description='Build and maintain modern React components. Work closely with backend team on API integration.',
                 required_skills='JavaScript, React, HTML/CSS, Git, Communication',
                 required_education='Bachelor in Computer Science or IT',
                 experience_years='1-3 years', work_mode='Hybrid', location='Brisbane, QLD',
                 salary='$70,000 - $90,000', is_active=True)

        j3 = Job(employer_id=e2.id, job_title='Junior Mobile Developer',
                 job_description='Help build and test Android/iOS applications for our aviation platform.',
                 required_skills='JavaScript, Git, Team Collaboration, Communication',
                 required_education='Bachelor in IT or Software Engineering',
                 experience_years='0-1 years', work_mode='Hybrid', location='Melbourne, VIC',
                 salary='$55,000 - $65,000', is_active=True)

        j4 = Job(employer_id=e3.id, job_title='Full Stack Developer',
                 job_description='Work across the stack building features for our SaaS product.',
                 required_skills='Python, JavaScript, SQL, Git, React',
                 required_education='Bachelor in Software Engineering or Computer Science',
                 experience_years='2-4 years', work_mode='On-site', location='Sydney, NSW',
                 salary='$85,000 - $100,000', is_active=True)

        j5 = Job(employer_id=e3.id, job_title='Backend Developer',
                 job_description='Build and maintain REST APIs using Python/Django. Write clean, testable code.',
                 required_skills='Python, SQL, Git, Django',
                 required_education='Bachelor in Computer Science',
                 experience_years='1-3 years', work_mode='Remote', location='Sydney, NSW',
                 salary='$75,000 - $90,000', is_active=True)

        db.session.add_all([j1, j2, j3, j4, j5])
        db.session.flush()
        print("Jobs created.")

        # ---- APPLICATIONS ----
        apps = [
            Application(candidate_id=c1.id, job_id=j1.id, status='pending',   match_score=80.0, matched_keywords='JavaScript, HTML/CSS, Git, Communication'),
            Application(candidate_id=c2.id, job_id=j1.id, status='reviewed',  match_score=85.0, matched_keywords='JavaScript, HTML/CSS, UI/UX Design, Git, Communication'),
            Application(candidate_id=c3.id, job_id=j1.id, status='pending',   match_score=60.0, matched_keywords='JavaScript, HTML/CSS, Git, Communication'),
            Application(candidate_id=c1.id, job_id=j3.id, status='pending',   match_score=40.0, matched_keywords='JavaScript, Git, Team Collaboration'),
            Application(candidate_id=c4.id, job_id=j4.id, status='accepted',  match_score=90.0, matched_keywords='Python, JavaScript, SQL, Git, React'),
            Application(candidate_id=c5.id, job_id=j1.id, status='pending',   match_score=60.0, matched_keywords='JavaScript, Git, HTML/CSS'),
        ]
        db.session.add_all(apps)
        print("Applications created.")

        # ---- BOOKMARKS ----
        bms = [
            Bookmark(candidate_id=c1.id, job_id=j2.id),
            Bookmark(candidate_id=c1.id, job_id=j4.id),
            Bookmark(candidate_id=c2.id, job_id=j2.id),
            Bookmark(candidate_id=c3.id, job_id=j3.id),
            Bookmark(candidate_id=c4.id, job_id=j5.id),
        ]
        db.session.add_all(bms)
        print("Bookmarks created.")

        # ---- MESSAGES ----
        msgs = [
            Message(sender_user_id=u6.id, receiver_user_id=u1.id,
                    content='Dear Lucas, Thank you so much for applying to the Frontend Developer position at BrightNova Digital. We were impressed with your profile and would love to schedule an interview.',
                    is_read=True),
            Message(sender_user_id=u1.id, receiver_user_id=u6.id,
                    content='Hi, thank you so much! I would love to discuss this further. I am available most mornings next week.',
                    is_read=True),
            Message(sender_user_id=u6.id, receiver_user_id=u1.id,
                    content='Great, let us lock in Sep 9 at 10:00 AM. We will send you a calendar invite.',
                    is_read=False),
            Message(sender_user_id=u7.id, receiver_user_id=u2.id,
                    content='Dear Sophia, Thank you so much for applying to our Junior Mobile Developer role. We think your skills are a great fit.',
                    is_read=True),
            Message(sender_user_id=u8.id, receiver_user_id=u3.id,
                    content='Dear Liam, We would love to chat further about the Backend Developer position. Are you available for a quick call this week?',
                    is_read=False),
        ]
        db.session.add_all(msgs)
        print("Messages created.")

        # ---- OFFERS ----
        offers = [
            Offer(employer_id=e1.id, candidate_id=c1.id, job_id=j1.id, status='accepted',
                  interview_date='Sep 9', interview_time='10:00 AM',
                  message='We would love to have you in for an interview. Please confirm the time works for you.'),
            Offer(employer_id=e1.id, candidate_id=c2.id, job_id=j1.id, status='pending',
                  interview_date='Sep 12', interview_time='10:00 AM',
                  message='Hi Sophia, we were impressed by your application and would love to meet.'),
            Offer(employer_id=e3.id, candidate_id=c4.id, job_id=j4.id, status='accepted',
                  interview_date='Sep 10', interview_time='2:00 PM',
                  message='Looking forward to meeting you Mia. The interview will be on-site.'),
        ]
        db.session.add_all(offers)
        print("Offers created.")

        # ---- RECOMMENDATIONS ----
        recs = [
            Recommendation(candidate_id=c1.id, job_id=j1.id, score=80.0, matched_keywords='JavaScript, HTML/CSS, Git, Communication'),
            Recommendation(candidate_id=c1.id, job_id=j2.id, score=75.0, matched_keywords='JavaScript, HTML/CSS, Git, Communication'),
            Recommendation(candidate_id=c1.id, job_id=j3.id, score=40.0, matched_keywords='JavaScript, Git, Team Collaboration'),
            Recommendation(candidate_id=c2.id, job_id=j1.id, score=85.0, matched_keywords='JavaScript, HTML/CSS, UI/UX Design, Git, Communication'),
            Recommendation(candidate_id=c2.id, job_id=j2.id, score=80.0, matched_keywords='JavaScript, HTML/CSS, Git, Communication'),
            Recommendation(candidate_id=c3.id, job_id=j1.id, score=60.0, matched_keywords='JavaScript, HTML/CSS, Git, Communication'),
            Recommendation(candidate_id=c3.id, job_id=j3.id, score=50.0, matched_keywords='JavaScript, Git, Team Collaboration'),
            Recommendation(candidate_id=c4.id, job_id=j4.id, score=90.0, matched_keywords='Python, JavaScript, SQL, Git, React'),
            Recommendation(candidate_id=c4.id, job_id=j5.id, score=70.0, matched_keywords='Python, SQL, Git'),
            Recommendation(candidate_id=c5.id, job_id=j1.id, score=60.0, matched_keywords='JavaScript, HTML/CSS, Git'),
        ]
        db.session.add_all(recs)
        print("Recommendations created.")

        db.session.commit()
        print("\n✅ Database seeded successfully!")
        print("\nTest accounts (all passwords: password123):")
        print("  Candidates: lucas@example.com, sophia@example.com, liam@example.com, mia@example.com, ryan@example.com")
        print("  Employers:  hr@brightnova.com, hr@flyhigh.com, hr@skycompany.com")


if __name__ == '__main__':
    seed()
