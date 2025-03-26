

from flask import Blueprint, request, jsonify
from server import db
from server.models import Program, Registration, Waitlist

waitlist_controller = Blueprint('waitlist_controller', __name__)

@waitlist_controller.route('/create_waitlist_notification_batch', methods=['POST'])
def create_waitlist_notification_batch():
    program_id = request.json['program_id']
    program = Program.query.get(program_id)
    if program.status != 'PUBLISHED':
        raise Exception('Program is not in PUBLISHED status')
    paid_registrations = Registration.query.filter_by(program_id=program_id, payment_status='PAID').count()
    if paid_registrations < program.min_participants:
        waitlist = Waitlist(program_id=program_id)
        db.session.add(waitlist)
        db.session.commit()
    return jsonify({'message': 'Waitlist notification batch created successfully'})