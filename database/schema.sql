-- ============================================================
-- Talent Matching Platform - Database Schema
-- Run this in MySQL before starting the backend
-- ============================================================

CREATE DATABASE IF NOT EXISTS talent_matching;
USE talent_matching;

-- Users table (shared login for both roles)
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('candidate', 'employer') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Candidate profiles
CREATE TABLE IF NOT EXISTS candidate (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    full_name VARCHAR(100),
    job_title VARCHAR(100),
    bio TEXT,
    skills TEXT,
    education VARCHAR(200),
    experience_years VARCHAR(50),
    location VARCHAR(100),
    work_mode VARCHAR(50),
    resume_filename VARCHAR(200),
    photo_filename VARCHAR(200),
    subscription ENUM('free', 'basic', 'premium') DEFAULT 'free',
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Employer profiles
CREATE TABLE IF NOT EXISTS employer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    company_name VARCHAR(100),
    company_info TEXT,
    logo_filename VARCHAR(200),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Job postings
CREATE TABLE IF NOT EXISTS job (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employer_id INT NOT NULL,
    job_title VARCHAR(100) NOT NULL,
    job_description TEXT,
    required_skills TEXT,
    required_education VARCHAR(200),
    experience_years VARCHAR(50),
    work_mode VARCHAR(50),
    location VARCHAR(100),
    salary VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employer_id) REFERENCES employer(id)
);

-- Applications (candidate applies to a job)
CREATE TABLE IF NOT EXISTS application (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT NOT NULL,
    job_id INT NOT NULL,
    status ENUM('pending', 'reviewed', 'accepted', 'rejected') DEFAULT 'pending',
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    match_score FLOAT DEFAULT 0.0,
    matched_keywords TEXT,
    FOREIGN KEY (candidate_id) REFERENCES candidate(id),
    FOREIGN KEY (job_id) REFERENCES job(id)
);

-- Bookmarks (candidate saves a job)
CREATE TABLE IF NOT EXISTS bookmark (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT NOT NULL,
    job_id INT NOT NULL,
    saved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidate(id),
    FOREIGN KEY (job_id) REFERENCES job(id)
);

-- Messages between users
CREATE TABLE IF NOT EXISTS message (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_user_id INT NOT NULL,
    receiver_user_id INT NOT NULL,
    content TEXT NOT NULL,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (sender_user_id) REFERENCES user(id),
    FOREIGN KEY (receiver_user_id) REFERENCES user(id)
);

-- Interview offers from employers to candidates
CREATE TABLE IF NOT EXISTS offer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employer_id INT NOT NULL,
    candidate_id INT NOT NULL,
    job_id INT NOT NULL,
    status ENUM('pending', 'accepted', 'rejected') DEFAULT 'pending',
    interview_date VARCHAR(100),
    interview_time VARCHAR(50),
    message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employer_id) REFERENCES employer(id),
    FOREIGN KEY (candidate_id) REFERENCES candidate(id),
    FOREIGN KEY (job_id) REFERENCES job(id)
);

-- Pre-computed recommendations
CREATE TABLE IF NOT EXISTS recommendation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT NOT NULL,
    job_id INT NOT NULL,
    score FLOAT NOT NULL,
    matched_keywords TEXT,
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidate(id),
    FOREIGN KEY (job_id) REFERENCES job(id)
);
