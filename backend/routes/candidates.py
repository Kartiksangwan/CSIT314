from flask import Blueprint, request, jsonify, session
from models import Candidate, User
from database import db
import os
from werkzeug.utils import secure_filename

candidates_bp = Blueprint('candidates', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_candidate_or_401():
    user_id = session.get('user_id')
    if not user_id:
        return None, jsonify({'error': 'Not logged in'}), 401

    candidate = Candidate.query.filter_by(user_id=user_id).first()
    if not candidate:
        return None, jsonify({'error': 'No candidate profile found'}), 404

    return candidate, None, None


@candidates_bp.route('/profile', methods=['GET'])
def get_profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    candidate = Candidate.query.filter_by(user_id=user_id).first()
    if not candidate:
        return jsonify({'error': 'Profile not found'}), 404

    return jsonify({'candidate': candidate.to_dict()}), 200


@candidates_bp.route('/profile', methods=['PUT'])
def update_profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    candidate = Candidate.query.filter_by(user_id=user_id).first()
    if not candidate:
        return jsonify({'error': 'Profile not found'}), 404

    data = request.get_json()

    # update only the fields that are sent
    if 'full_name' in data:
        candidate.full_name = data['full_name']
    if 'job_title' in data:
        candidate.job_title = data['job_title']
    if 'bio' in data:
        candidate.bio = data['bio']
    if 'skills' in data:
        candidate.skills = data['skills']
    if 'education' in data:
        candidate.education = data['education']
    if 'experience_years' in data:
        candidate.experience_years = data['experience_years']
    if 'location' in data:
        candidate.location = data['location']
    if 'work_mode' in data:
        candidate.work_mode = data['work_mode']

    db.session.commit()

    return jsonify({'message': 'Profile updated', 'candidate': candidate.to_dict()}), 200


@candidates_bp.route('/upload-photo', methods=['POST'])
def upload_photo():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    candidate = Candidate.query.filter_by(user_id=user_id).first()
    if not candidate:
        return jsonify({'error': 'Profile not found'}), 404

    if 'photo' not in request.files:
        return jsonify({'error': 'No photo file in request'}), 400

    photo = request.files['photo']
    if photo.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if photo and allowed_file(photo.filename):
        filename = secure_filename(f"candidate_{user_id}_{photo.filename}")
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        photo.save(os.path.join(UPLOAD_FOLDER, filename))
        candidate.photo_filename = filename
        db.session.commit()
        return jsonify({'message': 'Photo uploaded', 'filename': filename}), 200

    return jsonify({'error': 'File type not allowed'}), 400


@candidates_bp.route('/upload-resume', methods=['POST'])
def upload_resume():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    candidate = Candidate.query.filter_by(user_id=user_id).first()
    if not candidate:
        return jsonify({'error': 'Profile not found'}), 404

    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file in request'}), 400

    resume = request.files['resume']
    if resume.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if resume and allowed_file(resume.filename):
        filename = secure_filename(f"resume_{user_id}_{resume.filename}")
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        resume.save(os.path.join(UPLOAD_FOLDER, filename))
        candidate.resume_filename = filename
        db.session.commit()
        return jsonify({'message': 'Resume uploaded', 'filename': filename}), 200

    return jsonify({'error': 'File type not allowed'}), 400


@candidates_bp.route('/subscription', methods=['PUT'])
def update_subscription():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    candidate = Candidate.query.filter_by(user_id=user_id).first()
    if not candidate:
        return jsonify({'error': 'Profile not found'}), 404

    data = request.get_json()
    plan = data.get('plan')

    if plan not in ['free', 'basic', 'premium']:
        return jsonify({'error': 'Invalid plan. Must be free, basic, or premium'}), 400

    candidate.subscription = plan
    db.session.commit()

    return jsonify({'message': f'Subscription updated to {plan}'}), 200


@candidates_bp.route('/<int:candidate_id>', methods=['GET'])
def get_candidate_by_id(candidate_id):
    # employers can look up a candidate's info
    candidate = db.session.get(Candidate, candidate_id)
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404

    return jsonify({'candidate': candidate.to_dict()}), 200
