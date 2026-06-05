from flask import Blueprint, request, jsonify, session
from models import Recommendation, Candidate, Job, Employer
from database import db

recommendations_bp = Blueprint('recommendations', __name__)

FREE_LIMIT = 10   # max recommendations for non-members


def compute_score(candidate, job):
    score = 0
    matched = []

    if not candidate.skills or not job.required_skills:
        return 0.0, []

    candidate_skills = [s.strip().lower() for s in candidate.skills.split(',')]
    job_skills = [s.strip().lower() for s in job.required_skills.split(',')]

    for skill in job_skills:
        if skill in candidate_skills:
            matched.append(skill)

    if len(job_skills) > 0:
        skill_score = (len(matched) / len(job_skills)) * 60
        score += skill_score

    if candidate.location and job.location:
        if candidate.location.lower() in job.location.lower() or job.location.lower() in candidate.location.lower():
            score += 20

    if candidate.work_mode and job.work_mode:
        if candidate.work_mode.lower() == job.work_mode.lower():
            score += 20
        elif 'remote' in candidate.work_mode.lower() or 'remote' in job.work_mode.lower():
            score += 10

    return round(score, 1), matched


@recommendations_bp.route('/today', methods=['GET'])
def get_todays_recommendations():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    candidate = Candidate.query.filter_by(user_id=user_id).first()
    if not candidate:
        return jsonify({'error': 'Candidate profile not found'}), 404

    # MEMBERSHIP: premium/basic = unlimited, free = top 10
    is_member = candidate.subscription in ('basic', 'premium')
    n = request.args.get('n', None, type=int)

    jobs = Job.query.filter_by(is_active=True).all()
    scored_jobs = []

    for job in jobs:
        score, matched = compute_score(candidate, job)
        if score > 0:
            job_data = job.to_dict()
            employer = db.session.get(Employer, job.employer_id)
            if employer:
                job_data['company_name'] = employer.company_name
            job_data['match_score'] = score
            job_data['matched_keywords'] = matched
            scored_jobs.append(job_data)

    scored_jobs.sort(key=lambda x: x['match_score'], reverse=True)

    if n:
        top_n = scored_jobs[:n]
    elif is_member:
        top_n = scored_jobs          # unlimited for members
    else:
        top_n = scored_jobs[:FREE_LIMIT]   # cap at 10 for free

    return jsonify({
        'recommendations': top_n,
        'total_found': len(scored_jobs),
        'is_member': is_member,
        'subscription': candidate.subscription,
        'limit_applied': not is_member and len(scored_jobs) > FREE_LIMIT
    }), 200


@recommendations_bp.route('/top-candidates/<int:job_id>', methods=['GET'])
def get_top_candidates(job_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    employer = Employer.query.filter_by(user_id=user_id).first()
    if not employer:
        return jsonify({'error': 'Only employers can use this'}), 403

    job = db.session.get(Job, job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404

    # MEMBERSHIP: check employer subscription
    is_member = employer.subscription in ('basic', 'premium')
    k = request.args.get('k', None, type=int)

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

    if k:
        top_k = scored[:k]
    elif is_member:
        top_k = scored
    else:
        top_k = scored[:FREE_LIMIT]

    return jsonify({
        'top_candidates': top_k,
        'total_found': len(scored),
        'is_member': is_member
    }), 200


@recommendations_bp.route('/generate', methods=['POST'])
def generate_recommendations():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    candidate = Candidate.query.filter_by(user_id=user_id).first()
    if not candidate:
        return jsonify({'error': 'Candidate profile not found'}), 404

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
