from flask import Blueprint, request, jsonify, session
from models import Offer, Employer, Candidate, Job
from database import db

offers_bp = Blueprint('offers', __name__)


@offers_bp.route('/', methods=['GET'])
def get_offers():
    """Candidate gets all offers sent to them."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    candidate = Candidate.query.filter_by(user_id=user_id).first()
    if not candidate:
        return jsonify({'error': 'Candidate profile not found'}), 404

    offers = Offer.query.filter_by(candidate_id=candidate.id).all()

    result = []
    for offer in offers:
        offer_data = offer.to_dict()
        job = Job.query.get(offer.job_id)
        employer = Employer.query.get(offer.employer_id)
        offer_data['job_title'] = job.job_title if job else ''
        offer_data['company_name'] = employer.company_name if employer else ''
        result.append(offer_data)

    return jsonify({'offers': result}), 200


@offers_bp.route('/send', methods=['POST'])
def send_offer():
    """Employer sends an interview offer to a candidate."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    employer = Employer.query.filter_by(user_id=user_id).first()
    if not employer:
        return jsonify({'error': 'Only employers can send offers'}), 403

    data = request.get_json()
    candidate_id = data.get('candidate_id')
    job_id = data.get('job_id')
    interview_date = data.get('interview_date')
    interview_time = data.get('interview_time')
    message = data.get('message', '')

    if not candidate_id or not job_id:
        return jsonify({'error': 'candidate_id and job_id are required'}), 400

    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404

    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404

    offer = Offer(
        employer_id=employer.id,
        candidate_id=candidate_id,
        job_id=job_id,
        interview_date=interview_date,
        interview_time=interview_time,
        message=message
    )
    db.session.add(offer)
    db.session.commit()

    return jsonify({'message': 'Offer sent', 'offer': offer.to_dict()}), 201


@offers_bp.route('/<int:offer_id>/respond', methods=['PUT'])
def respond_to_offer(offer_id):
    """Candidate accepts or rejects an offer."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    candidate = Candidate.query.filter_by(user_id=user_id).first()
    if not candidate:
        return jsonify({'error': 'Candidate profile not found'}), 404

    offer = Offer.query.get(offer_id)
    if not offer:
        return jsonify({'error': 'Offer not found'}), 404

    if offer.candidate_id != candidate.id:
        return jsonify({'error': 'This offer is not for you'}), 403

    data = request.get_json()
    response = data.get('status')

    if response not in ['accepted', 'rejected']:
        return jsonify({'error': 'Status must be accepted or rejected'}), 400

    offer.status = response
    db.session.commit()

    return jsonify({'message': f'Offer {response}', 'offer': offer.to_dict()}), 200


@offers_bp.route('/employer', methods=['GET'])
def get_employer_offers():
    """Employer sees all offers they have sent."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    employer = Employer.query.filter_by(user_id=user_id).first()
    if not employer:
        return jsonify({'error': 'Employer profile not found'}), 404

    offers = Offer.query.filter_by(employer_id=employer.id).all()

    result = []
    for offer in offers:
        offer_data = offer.to_dict()
        candidate = Candidate.query.get(offer.candidate_id)
        job = Job.query.get(offer.job_id)
        offer_data['candidate_name'] = candidate.full_name if candidate else ''
        offer_data['job_title'] = job.job_title if job else ''
        result.append(offer_data)

    return jsonify({'offers': result}), 200
