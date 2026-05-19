from flask import Blueprint, request, jsonify, session
from models import Recommendation, Candidate, Job, Employer
from database import db

recommendations_bp = Blueprint('recommendations', __name__)


def compute_score(candidate, job):
    """
    Simple Top-K style matching algorithm.
    Compares candidate skills vs job required skills.
    Returns score 0-100 and list of matched keywords.
    """
    score = 0
    matched = []

    if not candidate.skills or not job.required_skills:
        return 0.0, []

    candidate_skills = [s.strip().lower() for s in candidate.skills.split(',')]
    job_skills = [s.strip().lower() for s in job.required_skills.split(',')]

    # skill match - most important (up to 60 points)
    for skill in job_skills:
        if skill in candidate_skills:
            matched.append(skill)

    if len(job_skills) > 0:
        skill_score = (len(matched) / len(job_skills)) * 60
        score += skill_score

    # location match (up to 20 points)
    if candidate.location and job.location:
        if candidate.location.lower() in job.location.lower() or job.location.lower() in candidate.location.lower():
            score += 20

    # work mode match (up to 20 points)
    if candidate.work_mode and job.work_mode:
        if candidate.work_mode.lower() == job.work_mode.lower():
            score += 20
        elif 'remote' in candidate.work_mode.lower() or 'remote' in job.work_mode.lower():
            score += 10  # partial credit for remote flexibility

    return round(score, 1), matched


@recommendations_bp.route('/today', methods=['GET'])
def get_todays_recommendations():
    """
    Returns Top-N job recommendations for the logged in candidate.
    Scores all active jobs and returns the best matches.
    """
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    candidate = Candidate.query.filter_by(user_id=user_id).first()
    if not candidate:
        return jsonify({'error': 'Candidate profile not found'}), 404

    # how many to return - default 10 (Top-N)
    n = request.args.get('n', 10, type=int)

    jobs = Job.query.filter_by(is_active=True).all()

    scored_jobs = []
    for job in jobs:
        score, matched = compute_score(candidate, job)
        if score > 0:
            job_data = job.to_dict()
            employer = Employer.query.get(job.employer_id)
            if employer:
                job_data['company_name'] = employer.company_name
            job_data['match_score'] = score
            job_data['matched_keywords'] = matched
            scored_jobs.append(job_data)

    # sort descending by score and return top N
    scored_jobs.sort(key=lambda x: x['match_score'], reverse=True)
    top_n = scored_jobs[:n]

    return jsonify({'recommendations': top_n, 'total_found': len(scored_jobs)}), 200


@recommendations_bp.route('/top-candidates/<int:job_id>', methods=['GET'])
def get_top_candidates(job_id):
    """
    Returns Top-K candidates for a given job. For employers.
    """
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    employer = Employer.query.filter_by(user_id=user_id).first()
    if not employer:
        return jsonify({'error': 'Only employers can use this'}), 403

    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404

    k = request.args.get('k', 10, type=int)

    candidates = Candidate.query.all()
    scored = []

    for c in candidates:
        if not c.full_name:
            continue
        score, matched = compute_score(c, job)
        if score > 0:
            c_data = c.to_dict()
            c_data['match_score'] = score
            c_data['matched_keywords'] = matched
            scored.append(c_data)

    scored.sort(key=lambda x: x['match_score'], reverse=True)
    top_k = scored[:k]

    return jsonify({'top_candidates': top_k, 'total_found': len(scored)}), 200


@recommendations_bp.route('/generate', methods=['POST'])
def generate_recommendations():
    """
    Pre-computes and stores recommendations for the current candidate.
    Can be run once to populate the recommendations table.
    """
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    candidate = Candidate.query.filter_by(user_id=user_id).first()
    if not candidate:
        return jsonify({'error': 'Candidate profile not found'}), 404

    # delete old recommendations for this candidate
    Recommendation.query.filter_by(candidate_id=candidate.id).delete()

    jobs = Job.query.filter_by(is_active=True).all()
    new_recs = []

    for job in jobs:
        score, matched = compute_score(candidate, job)
        if score > 0:
            rec = Recommendation(
                candidate_id=candidate.id,
                job_id=job.id,
                score=score,
                matched_keywords=', '.join(matched)
            )
            db.session.add(rec)
            new_recs.append({'job_id': job.id, 'score': score})

    db.session.commit()

    return jsonify({'message': f'Generated {len(new_recs)} recommendations', 'recommendations': new_recs}), 200
