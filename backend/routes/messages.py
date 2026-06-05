from flask import Blueprint, request, jsonify, session
from models import Message, User
from database import db

messages_bp = Blueprint('messages', __name__)


@messages_bp.route('/', methods=['GET'])
def get_messages():
    """Get all conversations for the logged in user."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    # get messages sent to or from this user
    sent = Message.query.filter_by(sender_user_id=user_id).all()
    received = Message.query.filter_by(receiver_user_id=user_id).all()

    # group by conversation partner
    conversations = {}

    for msg in sent + received:
        partner_id = msg.receiver_user_id if msg.sender_user_id == user_id else msg.sender_user_id
        if partner_id not in conversations:
            conversations[partner_id] = []
        conversations[partner_id].append(msg.to_dict())

    # sort each conversation by time
    for partner_id in conversations:
        conversations[partner_id].sort(key=lambda x: x['sent_at'])

    result = []
    for partner_id, msgs in conversations.items():
        partner = db.session.get(User, partner_id)
        result.append({
            'partner_id': partner_id,
            'partner_email': partner.email if partner else '',
            'messages': msgs,
            'latest': msgs[-1] if msgs else None
        })

    return jsonify({'conversations': result}), 200


@messages_bp.route('/thread/<int:partner_id>', methods=['GET'])
def get_thread(partner_id):
    """Get all messages between current user and a specific user."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    messages = Message.query.filter(
        ((Message.sender_user_id == user_id) & (Message.receiver_user_id == partner_id)) |
        ((Message.sender_user_id == partner_id) & (Message.receiver_user_id == user_id))
    ).order_by(Message.sent_at.asc()).all()

    # mark received messages as read
    for msg in messages:
        if msg.receiver_user_id == user_id and not msg.is_read:
            msg.is_read = True
    db.session.commit()

    return jsonify({'messages': [m.to_dict() for m in messages]}), 200


@messages_bp.route('/send', methods=['POST'])
def send_message():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    data = request.get_json()
    receiver_id = data.get('receiver_user_id')
    content = data.get('content')

    if not receiver_id or not content:
        return jsonify({'error': 'receiver_user_id and content are required'}), 400

    # check receiver exists
    receiver = db.session.get(User, receiver_id)
    if not receiver:
        return jsonify({'error': 'Receiver not found'}), 404

    msg = Message(
        sender_user_id=user_id,
        receiver_user_id=receiver_id,
        content=content
    )
    db.session.add(msg)
    db.session.commit()

    return jsonify({'message': 'Message sent', 'data': msg.to_dict()}), 201
