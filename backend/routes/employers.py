from flask import Blueprint, request, jsonify, session
from models import Employer, Application, Candidate, Job
from database import db
import os
from werkzeug.utils import secure_filename

employers_bp = Blueprint('employers', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@employers_bp.route('/profile', methods=['GET'])
def get_profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    employer = Employer.query.filter_by(user_id=user_id).first()
    if not employer:
        return jsonify({'error': 'Employer profile not found'}), 404

    return jsonify({'employer': employer.to_dict()}), 200


@employers_bp.route('/profile', methods=['PUT'])
def update_profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    employer = Employer.query.filter_by(user_id=user_id).first()
    if not employer:
        return jsonify({'error': 'Employer profile not found'}), 404

    data = request.get_json()

    if 'company_name' in data:
        employer.company_name = data['company_name']
    if 'company_info' in data:
        employer.company_info = data['company_info']

    db.session.commit()

    return jsonify({'message': 'Profile updated', 'employer': employer.to_dict()}), 200


@employers_bp.route('/upload-logo', methods=['POST'])
def upload_logo():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    employer = Employer.query.filter_by(user_id=user_id).first()
    if not employer:
        return jsonify({'error': 'Employer profile not found'}), 404

    if 'logo' not in request.files:
        return jsonify({'error': 'No logo file in request'}), 400

    logo = request.files['logo']
    if logo.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if logo and allowed_file(logo.filename):
        filename = secure_filename(f"logo_{user_id}_{logo.filename}")
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        logo.save(os.path.join(UPLOAD_FOLDER, filename))
        employer.logo_filename = filename
        db.session.commit()
        return jsonify({'message': 'Logo uploaded', 'filename': filename}), 200

    return jsonify({'error': 'File type not allowed'}), 400


@employers_bp.route('/applicants', methods=['GET'])
def get_applicants():
    # returns all candidates who applied to this employer's jobs
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    employer = Employer.query.filter_by(user_id=user_id).first()
    if not employer:
        return jsonify({'error': 'Employer profile not found'}), 404

    # get all jobs by this employer
    job_ids = [job.id for job in employer.jobs]

    # get all applications for those jobs
    applications = Application.query.filter(Application.job_id.in_(job_ids)).all()

    result = []
    for app in applications:
        candidate = Candidate.query.get(app.candidate_id)
        result.append({
            'application': app.to_dict(),
            'candidate': candidate.to_dict() if candidate else None
        })

    return jsonify({'applicants': result}), 200


@employers_bp.route('/<int:employer_id>', methods=['GET'])
def get_employer_by_id(employer_id):
    # candidates can view an employer's profile
    employer = Employer.query.get(employer_id)
    if not employer:
        return jsonify({'error': 'Employer not found'}), 404

    return jsonify({'employer': employer.to_dict()}), 200
