from flask import Blueprint, request, jsonify, session
from models import Job, Employer, Application, Candidate
from database import db

jobs_bp = Blueprint('jobs', __name__)


@jobs_bp.route('/', methods=['GET'])
def get_all_jobs():
    # get all active jobs
    jobs = Job.query.filter_by(is_active=True).all()
    result = []
    for job in jobs:
        job_data = job.to_dict()
        employer = db.session.get(Employer, job.employer_id)
        if employer:
            job_data['company_name'] = employer.company_name
        result.append(job_data)
    return jsonify({'jobs': result}), 200


# FIX: /my-jobs MUST be declared before /<int:job_id> or Flask treats "my-jobs" as an integer
@jobs_bp.route('/my-jobs', methods=['GET'])
def get_my_jobs():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    employer = Employer.query.filter_by(user_id=user_id).first()
    if not employer:
        return jsonify({'error': 'Employer not found'}), 404

    jobs = Job.query.filter_by(employer_id=employer.id).all()
    return jsonify({'jobs': [j.to_dict() for j in jobs]}), 200


@jobs_bp.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = db.session.get(Job, job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404

    job_data = job.to_dict()
    employer = db.session.get(Employer, job.employer_id)
    if employer:
        job_data['company_name'] = employer.company_name
        job_data['company_info'] = employer.company_info

    return jsonify({'job': job_data}), 200


@jobs_bp.route('/', methods=['POST'])
def create_job():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    employer = Employer.query.filter_by(user_id=user_id).first()
    if not employer:
        return jsonify({'error': 'Only employers can post jobs'}), 403

    data = request.get_json()

    if not data.get('job_title'):
        return jsonify({'error': 'Job title is required'}), 400

    job = Job(
        employer_id=employer.id,
        job_title=data.get('job_title'),
        job_description=data.get('job_description'),
        required_skills=data.get('required_skills'),
        required_education=data.get('required_education'),
        experience_years=data.get('experience_years'),
        work_mode=data.get('work_mode'),
        location=data.get('location'),
        salary=data.get('salary')
    )

    db.session.add(job)
    db.session.commit()

    return jsonify({'message': 'Job posted', 'job': job.to_dict()}), 201


@jobs_bp.route('/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    employer = Employer.query.filter_by(user_id=user_id).first()
    if not employer:
        return jsonify({'error': 'Only employers can update jobs'}), 403

    job = db.session.get(Job, job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404

    if job.employer_id != employer.id:
        return jsonify({'error': 'You can only edit your own jobs'}), 403

    data = request.get_json()

    if 'job_title' in data:
        job.job_title = data['job_title']
    if 'job_description' in data:
        job.job_description = data['job_description']
    if 'required_skills' in data:
        job.required_skills = data['required_skills']
    if 'required_education' in data:
        job.required_education = data['required_education']
    if 'experience_years' in data:
        job.experience_years = data['experience_years']
    if 'work_mode' in data:
        job.work_mode = data['work_mode']
    if 'location' in data:
        job.location = data['location']
    if 'salary' in data:
        job.salary = data['salary']
    if 'is_active' in data:
        job.is_active = data['is_active']

    db.session.commit()

    return jsonify({'message': 'Job updated', 'job': job.to_dict()}), 200


@jobs_bp.route('/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    employer = Employer.query.filter_by(user_id=user_id).first()
    if not employer:
        return jsonify({'error': 'Only employers can delete jobs'}), 403

    job = db.session.get(Job, job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404

    if job.employer_id != employer.id:
        return jsonify({'error': 'You can only delete your own jobs'}), 403

    job.is_active = False
    db.session.commit()

    return jsonify({'message': 'Job removed'}), 200


@jobs_bp.route('/<int:job_id>/apply', methods=['POST'])
def apply_to_job(job_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    candidate = Candidate.query.filter_by(user_id=user_id).first()
    if not candidate:
        return jsonify({'error': 'Only candidates can apply to jobs'}), 403

    job = db.session.get(Job, job_id)
    if not job or not job.is_active:
        return jsonify({'error': 'Job not found or no longer active'}), 404

    existing = Application.query.filter_by(candidate_id=candidate.id, job_id=job_id).first()
    if existing:
        return jsonify({'error': 'You have already applied to this job'}), 400

    score, matched = calculate_match(candidate, job)

    application = Application(
        candidate_id=candidate.id,
        job_id=job_id,
        match_score=score,
        matched_keywords=matched
    )
    db.session.add(application)
    db.session.commit()

    return jsonify({'message': 'Application submitted', 'match_score': score, 'matched_keywords': matched}), 201


def calculate_match(candidate, job):
    """Simple keyword matching to calculate match score."""
    if not candidate.skills or not job.required_skills:
        return 0.0, ''

    candidate_skills = [s.strip().lower() for s in candidate.skills.split(',')]
    job_skills = [s.strip().lower() for s in job.required_skills.split(',')]

    matched = [skill for skill in job_skills if skill in candidate_skills]

    if len(job_skills) == 0:
        return 0.0, ''

    score = round((len(matched) / len(job_skills)) * 100, 1)
    matched_str = ', '.join(matched)

    return score, matched_str
