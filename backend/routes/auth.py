from flask import Blueprint, request, jsonify, session
from models import User, Candidate, Employer
from database import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    role = data.get('role')  # 'candidate' or 'employer'

    if not email or not password or not role:
        return jsonify({'error': 'Email, password and role are required'}), 400

    if role not in ['candidate', 'employer']:
        return jsonify({'error': 'Role must be candidate or employer'}), 400

    existing = User.query.filter_by(email=email).first()
    if existing:
        return jsonify({'error': 'Email already registered'}), 400

    new_user = User(email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.flush()  # get the user id before commit

    if role == 'candidate':
        profile = Candidate(user_id=new_user.id)
        db.session.add(profile)
    else:
        profile = Employer(user_id=new_user.id)
        db.session.add(profile)

    db.session.commit()

    session['user_id'] = new_user.id
    session['role'] = new_user.role

    return jsonify({'message': 'Account created successfully', 'user': new_user.to_dict()}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    session['user_id'] = user.id
    session['role'] = user.role

    return jsonify({'message': 'Logged in', 'user': user.to_dict()}), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'}), 200


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    # FIX: use db.session.get() instead of deprecated User.query.get()
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'user': user.to_dict()}), 200
