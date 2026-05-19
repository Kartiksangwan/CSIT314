from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('candidate', 'employer'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    candidate = db.relationship('Candidate', backref='user', uselist=False)
    employer = db.relationship('Employer', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'created_at': str(self.created_at)
        }


class Candidate(db.Model):
    __tablename__ = 'candidate'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    bio = db.Column(db.Text)
    skills = db.Column(db.Text)          # comma-separated eg "Python, SQL, Git"
    education = db.Column(db.String(200))
    experience_years = db.Column(db.String(50))
    location = db.Column(db.String(100))
    work_mode = db.Column(db.String(50))  # Remote / Hybrid / On-site
    resume_filename = db.Column(db.String(200))
    photo_filename = db.Column(db.String(200))
    subscription = db.Column(db.Enum('free', 'basic', 'premium'), default='free')

    bookmarks = db.relationship('Bookmark', backref='candidate', lazy=True)
    applications = db.relationship('Application', backref='candidate', lazy=True)
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_user_id', backref='sender', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'job_title': self.job_title,
            'bio': self.bio,
            'skills': self.skills,
            'education': self.education,
            'experience_years': self.experience_years,
            'location': self.location,
            'work_mode': self.work_mode,
            'resume_filename': self.resume_filename,
            'photo_filename': self.photo_filename,
            'subscription': self.subscription
        }


class Employer(db.Model):
    __tablename__ = 'employer'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100))
    company_info = db.Column(db.Text)
    logo_filename = db.Column(db.String(200))

    jobs = db.relationship('Job', backref='employer', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'company_name': self.company_name,
            'company_info': self.company_info,
            'logo_filename': self.logo_filename
        }


class Job(db.Model):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text)
    required_skills = db.Column(db.Text)    # comma-separated
    required_education = db.Column(db.String(200))
    experience_years = db.Column(db.String(50))
    work_mode = db.Column(db.String(50))
    location = db.Column(db.String(100))
    salary = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship('Application', backref='job', lazy=True)
    bookmarks = db.relationship('Bookmark', backref='job', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'employer_id': self.employer_id,
            'job_title': self.job_title,
            'job_description': self.job_description,
            'required_skills': self.required_skills,
            'required_education': self.required_education,
            'experience_years': self.experience_years,
            'work_mode': self.work_mode,
            'location': self.location,
            'salary': self.salary,
            'is_active': self.is_active,
            'created_at': str(self.created_at)
        }


class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.Enum('pending', 'reviewed', 'accepted', 'rejected'), default='pending')
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    match_score = db.Column(db.Float, default=0.0)
    matched_keywords = db.Column(db.Text)   # comma-separated matched keywords

    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'job_id': self.job_id,
            'status': self.status,
            'applied_at': str(self.applied_at),
            'match_score': self.match_score,
            'matched_keywords': self.matched_keywords
        }


class Bookmark(db.Model):
    __tablename__ = 'bookmark'

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'job_id': self.job_id,
            'saved_at': str(self.saved_at)
        }


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    sender_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    receiver = db.relationship('User', foreign_keys=[receiver_user_id], backref='received_messages')

    def to_dict(self):
        return {
            'id': self.id,
            'sender_user_id': self.sender_user_id,
            'receiver_user_id': self.receiver_user_id,
            'content': self.content,
            'sent_at': str(self.sent_at),
            'is_read': self.is_read
        }


class Offer(db.Model):
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.Enum('pending', 'accepted', 'rejected'), default='pending')
    interview_date = db.Column(db.String(100))
    interview_time = db.Column(db.String(50))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employer = db.relationship('Employer', backref='offers')
    candidate = db.relationship('Candidate', backref='offers')
    job = db.relationship('Job', backref='offers')

    def to_dict(self):
        return {
            'id': self.id,
            'employer_id': self.employer_id,
            'candidate_id': self.candidate_id,
            'job_id': self.job_id,
            'status': self.status,
            'interview_date': self.interview_date,
            'interview_time': self.interview_time,
            'message': self.message,
            'created_at': str(self.created_at)
        }


class Recommendation(db.Model):
    __tablename__ = 'recommendation'

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    matched_keywords = db.Column(db.Text)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

    candidate = db.relationship('Candidate', backref='recommendations')
    job = db.relationship('Job', backref='recommendations')

    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'job_id': self.job_id,
            'score': self.score,
            'matched_keywords': self.matched_keywords,
            'generated_at': str(self.generated_at)
        }
