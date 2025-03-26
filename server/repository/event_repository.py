

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from datetime import datetime

Base = declarative_base()

class LibraryEvent(Base):
    __tablename__ = 'library_events'
    id = Column(Integer, primary_key=True)
    event_date = Column(DateTime)
    event_status = Column(Enum('SCHEDULED', 'CANCELLED', 'RESCHEDULED'))

class EventRegistration(Base):
    __tablename__ = 'event_registrations'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    patron_id = Column(Integer)
    registration_status = Column(Enum('REGISTERED', 'NO_SHOW'))

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    registrant_id = Column(Integer)
    notification_status = Column(Enum('SENT', 'FAILED'))

engine = create_engine('postgresql://user:password@host:port/dbname')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def send_notification(patron_id, message):
    # Implement notification sending logic here
    pass

def validate_date(date):
    # Implement date validation logic here
    return True

def cancel_event(event_id):
    affected_registrants = session.query(EventRegistration).filter_by(event_id=event_id).all()
    event = session.query(LibraryEvent).filter_by(id=event_id).first()
    event.event_status = 'CANCELLED'
    session.commit()
    for registrant in affected_registrants:
        registrant.registration_status = 'NO_SHOW'
        session.commit()
    for registrant in affected_registrants:
        send_notification(registrant.patron_id, 'Event cancelled')
    for registrant in affected_registrants:
        audit_log = AuditLog(event_id=event_id, registrant_id=registrant.id, notification_status='SENT')
        session.add(audit_log)
        session.commit()

def reschedule_event(event_id, new_date):
    if not validate_date(new_date):
        raise ValueError('Invalid date')
    schedule_conflicts = session.query(EventRegistration).filter_by(event_id=event_id, event_date=new_date).all()
    if schedule_conflicts:
        for registrant in schedule_conflicts:
            send_notification(registrant.patron_id, 'Scheduling conflict')
            audit_log = AuditLog(event_id=event_id, notification='Conflict notification sent')
            session.add(audit_log)
            session.commit()
    event = session.query(LibraryEvent).filter_by(id=event_id).first()
    event.event_date = new_date
    session.commit()
    affected_registrants = session.query(EventRegistration).filter_by(event_id=event_id).all()
    for registrant in affected_registrants:
        send_notification(registrant.patron_id, 'Event rescheduled')
    for registrant in affected_registrants:
        audit_log = AuditLog(event_id=event_id, registrant_id=registrant.id, notification_status='SENT')
        session.add(audit_log)
        session.commit()