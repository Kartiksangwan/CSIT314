from flask import Blueprint, request, jsonify, session
from models import Bookmark, Candidate, Job, Employer
from database import db

bookmarks_bp = Blueprint('bookmarks', __name__)


@bookmarks_bp.route('/', methods=['GET'])
def get_bookmarks():
    """Get all bookmarked jobs for the logged in candidate."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    candidate = Candidate.query.filter_by(user_id=user_id).first()
    if not candidate:
        return jsonify({'error': 'Candidate profile not found'}), 404

    bookmarks = Bookmark.query.filter_by(candidate_id=candidate.id).all()

    result = []
    for b in bookmarks:
        job = db.session.get(Job, b.job_id)
        if job:
            job_data = job.to_dict()
            employer = db.session.get(Employer, job.employer_id)
            if employer:
                job_data['company_name'] = employer.company_name
            result.append({
                'bookmark_id': b.id,
                'saved_at': str(b.saved_at),
                'job': job_data
            })

    return jsonify({'bookmarks': result}), 200


@bookmarks_bp.route('/add', methods=['POST'])
def add_bookmark():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    candidate = Candidate.query.filter_by(user_id=user_id).first()
    if not candidate:
        return jsonify({'error': 'Candidate profile not found'}), 404

    data = request.get_json()
    job_id = data.get('job_id')

    if not job_id:
        return jsonify({'error': 'job_id is required'}), 400

    job = db.session.get(Job, job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404

    # check if already bookmarked
    existing = Bookmark.query.filter_by(candidate_id=candidate.id, job_id=job_id).first()
    if existing:
        return jsonify({'error': 'Already bookmarked'}), 400

    bookmark = Bookmark(candidate_id=candidate.id, job_id=job_id)
    db.session.add(bookmark)
    db.session.commit()

    return jsonify({'message': 'Job bookmarked', 'bookmark': bookmark.to_dict()}), 201


@bookmarks_bp.route('/remove/<int:job_id>', methods=['DELETE'])
def remove_bookmark(job_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    candidate = Candidate.query.filter_by(user_id=user_id).first()
    if not candidate:
        return jsonify({'error': 'Candidate profile not found'}), 404

    bookmark = Bookmark.query.filter_by(candidate_id=candidate.id, job_id=job_id).first()
    if not bookmark:
        return jsonify({'error': 'Bookmark not found'}), 404

    db.session.delete(bookmark)
    db.session.commit()

    return jsonify({'message': 'Bookmark removed'}), 200


@bookmarks_bp.route('/employer', methods=['GET'])
def get_employer_bookmarks():
    """Employer bookmarks candidates they are interested in."""
    # For the employer side - they bookmark candidates
    # Using the same Bookmark table but we store candidate_id and a job_id of 0 or similar
    # Actually for simplicity let's just use a query param approach
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    return jsonify({'message': 'Use /api/employers/applicants to see interested candidates'}), 200
