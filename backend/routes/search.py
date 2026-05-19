from flask import Blueprint, request, jsonify, session
from models import Candidate, Job, Employer
from database import db

search_bp = Blueprint('search', __name__)


@search_bp.route('/candidates', methods=['GET'])
def search_candidates():
    """Employer searches for candidates by keywords/skills."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    keyword = request.args.get('keyword', '').lower().strip()
    location = request.args.get('location', '').lower().strip()
    work_mode = request.args.get('work_mode', '').lower().strip()

    candidates = Candidate.query.all()
    results = []

    for c in candidates:
        if not c.full_name:
            continue  # skip incomplete profiles

        matched_keywords = []
        score = 0

        # check keyword match in skills
        if keyword and c.skills:
            candidate_skills = [s.strip().lower() for s in c.skills.split(',')]
            for skill in candidate_skills:
                if keyword in skill:
                    matched_keywords.append(skill)
                    score += 20

        # check keyword in job title
        if keyword and c.job_title and keyword in c.job_title.lower():
            score += 10

        # check location filter
        if location and c.location:
            if location not in c.location.lower():
                continue  # skip if location doesn't match

        # check work mode filter
        if work_mode and c.work_mode:
            if work_mode not in c.work_mode.lower():
                continue  # skip if work mode doesn't match

        # if there's no keyword filter, just include everyone
        if not keyword:
            score = 50

        if score > 0 or not keyword:
            candidate_data = c.to_dict()
            candidate_data['match_score'] = min(score, 100)
            candidate_data['matched_keywords'] = matched_keywords
            results.append(candidate_data)

    # sort by match score highest first
    results.sort(key=lambda x: x['match_score'], reverse=True)

    return jsonify({'candidates': results}), 200


@search_bp.route('/jobs', methods=['GET'])
def search_jobs():
    """Candidate searches for jobs by keyword."""
    keyword = request.args.get('keyword', '').lower().strip()
    location = request.args.get('location', '').lower().strip()
    work_mode = request.args.get('work_mode', '').lower().strip()

    jobs = Job.query.filter_by(is_active=True).all()
    results = []

    for job in jobs:
        score = 0
        matched = []

        if keyword:
            # check title
            if job.job_title and keyword in job.job_title.lower():
                score += 30
                matched.append(job.job_title)

            # check required skills
            if job.required_skills:
                job_skills = [s.strip().lower() for s in job.required_skills.split(',')]
                for skill in job_skills:
                    if keyword in skill:
                        score += 15
                        matched.append(skill)

            # check description
            if job.job_description and keyword in job.job_description.lower():
                score += 10

        # apply filters
        if location and job.location:
            if location not in job.location.lower():
                continue

        if work_mode and job.work_mode:
            if work_mode not in job.work_mode.lower():
                continue

        if not keyword:
            score = 50

        if score > 0 or not keyword:
            job_data = job.to_dict()
            employer = Employer.query.get(job.employer_id)
            if employer:
                job_data['company_name'] = employer.company_name
            job_data['match_score'] = min(score, 100)
            job_data['matched_keywords'] = list(set(matched))
            results.append(job_data)

    results.sort(key=lambda x: x['match_score'], reverse=True)

    return jsonify({'jobs': results}), 200


@search_bp.route('/keywords-from-job', methods=['GET'])
def get_keywords_from_job():
    """Employer gets keywords extracted from their job posting to refine search."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    job_id = request.args.get('job_id')
    if not job_id:
        return jsonify({'error': 'job_id is required'}), 400

    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404

    keywords = []
    if job.required_skills:
        keywords = [s.strip() for s in job.required_skills.split(',')]

    return jsonify({'keywords': keywords}), 200
