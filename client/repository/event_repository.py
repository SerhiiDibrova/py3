

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///library.db')
Base = declarative_base()

class EventRegistration(Base):
    __tablename__ = 'event_registrations'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    patron_id = Column(Integer)
    registration_date = Column(DateTime)
    attendance_status = Column(String)

class LibraryEvent(Base):
    __tablename__ = 'library_events'
    id = Column(Integer, primary_key=True)
    max_participants = Column(Integer)
    current_participants = Column(Integer)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
db = Session()

def register_for_event(event_id, patron_id):
    registration = EventRegistration(event_id=event_id, patron_id=patron_id, registration_date=datetime.now(), attendance_status='REGISTERED')
    db.add(registration)
    db.commit()
    event = db.query(LibraryEvent).get(event_id)
    event.current_participants += 1
    db.commit()

def register_patron_for_event(event_id, patron_id):
    v_is_registered = db.query(EventRegistration).filter_by(event_id=event_id, patron_id=patron_id).count()
    if v_is_registered > 0:
        raise Exception('Patron is already registered for the event.')
    event = db.query(LibraryEvent).get(event_id)
    if event.current_participants >= event.max_participants:
        raise Exception('Event is full.')
    register_for_event(event_id, patron_id)