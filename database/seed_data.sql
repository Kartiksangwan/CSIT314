-- ============================================================
-- Talent Matching Platform - Sample Data
-- Run this AFTER schema.sql
-- All passwords are: password123
-- ============================================================

USE talent_matching;

-- ============================================================
-- USERS
-- ============================================================

-- Candidate users (password: password123)
INSERT INTO user (email, password_hash, role) VALUES
('lucas@example.com',   'pbkdf2:sha256:260000$abc1$placeholder_hash_1', 'candidate'),
('sophia@example.com',  'pbkdf2:sha256:260000$abc2$placeholder_hash_2', 'candidate'),
('liam@example.com',    'pbkdf2:sha256:260000$abc3$placeholder_hash_3', 'candidate'),
('mia@example.com',     'pbkdf2:sha256:260000$abc4$placeholder_hash_4', 'candidate'),
('ryan@example.com',    'pbkdf2:sha256:260000$abc5$placeholder_hash_5', 'candidate');

-- Employer users (password: password123)
INSERT INTO user (email, password_hash, role) VALUES
('hr@brightnova.com',   'pbkdf2:sha256:260000$abc6$placeholder_hash_6', 'employer'),
('hr@flyhigh.com',      'pbkdf2:sha256:260000$abc7$placeholder_hash_7', 'employer'),
('hr@skycompany.com',   'pbkdf2:sha256:260000$abc8$placeholder_hash_8', 'employer');

-- ============================================================
-- CANDIDATE PROFILES
-- ============================================================

INSERT INTO candidate (user_id, full_name, job_title, bio, skills, education, experience_years, location, work_mode, subscription) VALUES
(1, 'Lucas Johnson',  'Frontend Developer',
 'I have experience in Java, Python, and mobile app development. Worked on team projects involving UI/UX design and database integration.',
 'JavaScript, HTML/CSS, React, Git, UI/UX Design, Communication',
 'Bachelor of Computer Science', '2 years', 'Brisbane, QLD', 'Hybrid', 'basic'),

(2, 'Sophia Turner',  'Frontend Developer',
 'Passionate about responsive web design and clean UI. Strong background in JavaScript frameworks.',
 'JavaScript, HTML/CSS, UI/UX Design, Git, Communication',
 'Bachelor of Information Technology', '2 years', 'Brisbane, QLD', 'Remote', 'free'),

(3, 'Liam Carter',    'Junior Web Developer',
 'Fresh graduate with solid fundamentals in web development and a team-first mindset.',
 'JavaScript, HTML/CSS, Git, Team Collaboration, Communication',
 'Bachelor of IT', '1-2 years', 'Sydney, NSW', 'Remote', 'free'),

(4, 'Mia Chen',       'Full Stack Developer',
 'Full stack developer comfortable with Python and JavaScript. Enjoys building end-to-end features.',
 'Python, JavaScript, SQL, Git, React, Django',
 'Bachelor of Software Engineering', '3 years', 'Melbourne, VIC', 'On-site', 'premium'),

(5, 'Ryan Chen',      'Junior Web Developer',
 'Team player with solid Git skills and growing JavaScript experience.',
 'JavaScript, Git, HTML/CSS, Team Collaboration',
 'Bachelor of Computer Science', '1-2 years', 'Brisbane, QLD', 'Remote', 'free');

-- ============================================================
-- EMPLOYER PROFILES
-- ============================================================

INSERT INTO employer (user_id, company_name, company_info) VALUES
(6, 'BrightNova Digital',
 'BrightNova Digital is a technology company specializing in responsive web applications and modern UI development for startups and business clients.'),

(7, 'Fly High Company',
 'Fly High is a growing tech startup focused on mobile and web products for the aviation industry.'),

(8, 'Sky Company',
 'Sky Company builds cloud-based SaaS tools for SMBs across Australia.');

-- ============================================================
-- JOB POSTINGS
-- ============================================================

INSERT INTO job (employer_id, job_title, job_description, required_skills, required_education, experience_years, work_mode, location, salary, is_active) VALUES
(1, 'Frontend Web Developer',
 'Develop and maintain responsive web interfaces using JavaScript and collaborate with designers to improve user experience and application performance.',
 'JavaScript, HTML/CSS, Git, UI/UX Design, Communication',
 'Bachelor in Computer Science, IT, or related field',
 '1-2 years', 'Remote', 'Brisbane, QLD', '$65,000 - $80,000', TRUE),

(1, 'React Developer',
 'Build and maintain modern React components. Work closely with backend team on API integration.',
 'JavaScript, React, HTML/CSS, Git, Communication',
 'Bachelor in Computer Science or IT',
 '1-3 years', 'Hybrid', 'Brisbane, QLD', '$70,000 - $90,000', TRUE),

(2, 'Junior Mobile Developer',
 'Help build and test Android/iOS applications for our aviation platform. Good teamwork skills required.',
 'JavaScript, Git, Team Collaboration, Communication',
 'Bachelor in IT or Software Engineering',
 '0-1 years', 'Hybrid', 'Melbourne, VIC', '$55,000 - $65,000', TRUE),

(3, 'Full Stack Developer',
 'Work across the stack building features for our SaaS product. Python backend and JavaScript frontend.',
 'Python, JavaScript, SQL, Git, React',
 'Bachelor in Software Engineering or Computer Science',
 '2-4 years', 'On-site', 'Sydney, NSW', '$85,000 - $100,000', TRUE),

(3, 'Backend Developer',
 'Build and maintain REST APIs using Python/Django. Write clean, testable code.',
 'Python, SQL, Git, Django',
 'Bachelor in Computer Science',
 '1-3 years', 'Remote', 'Sydney, NSW', '$75,000 - $90,000', TRUE);

-- ============================================================
-- APPLICATIONS
-- ============================================================

INSERT INTO application (candidate_id, job_id, status, match_score, matched_keywords) VALUES
(1, 1, 'pending',   80.0, 'JavaScript, HTML/CSS, Git, Communication'),
(2, 1, 'reviewed',  85.0, 'JavaScript, HTML/CSS, UI/UX Design, Git, Communication'),
(3, 1, 'pending',   60.0, 'JavaScript, HTML/CSS, Git, Communication'),
(1, 3, 'pending',   40.0, 'JavaScript, Git, Team Collaboration'),
(4, 4, 'accepted',  90.0, 'Python, JavaScript, SQL, Git, React'),
(5, 1, 'pending',   60.0, 'JavaScript, Git, HTML/CSS');

-- ============================================================
-- BOOKMARKS
-- ============================================================

INSERT INTO bookmark (candidate_id, job_id) VALUES
(1, 2),
(1, 4),
(2, 2),
(3, 3),
(4, 5);

-- ============================================================
-- MESSAGES
-- ============================================================

INSERT INTO message (sender_user_id, receiver_user_id, content, is_read) VALUES
(6, 1, 'Dear Lucas, Thank you so much for applying to the Frontend Developer position at BrightNova Digital. We were impressed with your profile and would love to schedule an interview.', TRUE),
(1, 6, 'Hi, thank you so much! I would love to discuss this further. I am available most mornings next week.', TRUE),
(6, 1, 'Great, let us lock in Sep 9 at 10:00 AM. We will send you a calendar invite.', FALSE),

(7, 2, 'Dear Sophia, Thank you so much for applying to our Junior Mobile Developer role. We think your skills are a great fit.', TRUE),
(8, 3, 'Dear Liam, We would love to chat further about the Backend Developer position. Are you available for a quick call this week?', FALSE);

-- ============================================================
-- OFFERS (Interview Offers)
-- ============================================================

INSERT INTO offer (employer_id, candidate_id, job_id, status, interview_date, interview_time, message) VALUES
(1, 1, 1, 'accepted', 'Sep 9',  '10:00 AM', 'We would love to have you in for an interview. Please confirm the time works for you.'),
(1, 2, 1, 'pending',  'Sep 12', '10:00 AM', 'Hi Sophia, we were impressed by your application and would love to meet.'),
(3, 4, 4, 'accepted', 'Sep 10', '2:00 PM',  'Looking forward to meeting you Mia. The interview will be on-site.');

-- ============================================================
-- PRE-COMPUTED RECOMMENDATIONS
-- ============================================================

INSERT INTO recommendation (candidate_id, job_id, score, matched_keywords) VALUES
(1, 1, 80.0, 'JavaScript, HTML/CSS, Git, Communication'),
(1, 2, 75.0, 'JavaScript, HTML/CSS, Git, Communication'),
(1, 3, 40.0, 'JavaScript, Git, Team Collaboration'),
(2, 1, 85.0, 'JavaScript, HTML/CSS, UI/UX Design, Git, Communication'),
(2, 2, 80.0, 'JavaScript, HTML/CSS, Git, Communication'),
(3, 1, 60.0, 'JavaScript, HTML/CSS, Git, Communication'),
(3, 3, 50.0, 'JavaScript, Git, Team Collaboration'),
(4, 4, 90.0, 'Python, JavaScript, SQL, Git, React'),
(4, 5, 70.0, 'Python, SQL, Git'),
(5, 1, 60.0, 'JavaScript, HTML/CSS, Git');
