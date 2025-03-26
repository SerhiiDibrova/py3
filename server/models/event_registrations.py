

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class EventRegistrations(Base):
    __tablename__ = 'event_registrations'
    registration_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('library_events.event_id'))
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    registration_status = Column(String)
    library_events = relationship('LibraryEvents', backref='event_registrations')