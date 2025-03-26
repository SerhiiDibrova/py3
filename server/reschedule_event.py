

from models import LibraryEvent, EventRegistration, Patron, AuditLog
from sqlalchemy import create_engine
from flask import current_app

def reschedule_event(event_id, new_date):
    db = create_engine(current_app.config['DATABASE_URI'])
    event = LibraryEvent.query.get(event_id)
    registrations = EventRegistration.query.filter_by(event_id=event_id).all()

    event.event_status = 'RESCHEDULED'
    event.event_date = new_date
    db.session.add(event)

    for registration in registrations:
        patron = Patron.query.get(registration.patron_id)
        # Send notification to patron
        # Assuming you have a function to send notifications
        # send_notification(patron, event)

    audit_log = AuditLog(event_id=event_id, log_message='Event rescheduled')
    db.session.add(audit_log)
    db.session.commit()