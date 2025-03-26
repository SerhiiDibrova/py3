

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

class EventRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('library_event.id'), nullable=False)
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.id'), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    attendance_status = db.Column(db.String(20), nullable=False, default='REGISTERED')

class LibraryEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    max_participants = db.Column(db.Integer, nullable=False)
    current_participants = db.Column(db.Integer, nullable=False, default=0)

class EventRegistrationController:
    def __init__(self, event_id, patron_id):
        self.event_id = event_id
        self.patron_id = patron_id

    def check_registration(self):
        v_is_registered = EventRegistration.query.filter_by(event_id=self.event_id, patron_id=self.patron_id).first()
        if v_is_registered:
            raise Exception('Patron is already registered for this event')

    def get_event_capacity(self):
        v_max_participants = LibraryEvent.query.get(self.event_id).max_participants
        v_current_participants = LibraryEvent.query.get(self.event_id).current_participants
        return v_max_participants, v_current_participants

    def register_patron(self):
        v_max_participants, v_current_participants = self.get_event_capacity()
        if v_current_participants >= v_max_participants:
            raise Exception('Event is full')
        self.register_for_event(self.event_id, self.patron_id)

    def register_for_event(self, event_id, patron_id):
        event_registration = EventRegistration(event_id=event_id, patron_id=patron_id, registration_date=datetime.now(), attendance_status='REGISTERED')
        db.session.add(event_registration)
        db.session.commit()
        library_event = LibraryEvent.query.get(event_id)
        library_event.current_participants += 1
        db.session.commit()

@app.route('/register', methods=['POST'])
def register():
    event_id = request.json['event_id']
    patron_id = request.json['patron_id']
    controller = EventRegistrationController(event_id, patron_id)
    try:
        controller.check_registration()
        controller.register_patron()
        return jsonify({'message': 'Patron registered successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)