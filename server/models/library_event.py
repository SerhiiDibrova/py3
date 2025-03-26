

from sqlalchemy import Column, Integer, Date, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LibraryEvent(Base):
    __tablename__ = 'library_events'
    event_id = Column(Integer, primary_key=True)
    event_date = Column(Date)
    event_type = Column(String)
    participant_count = Column(Integer)
    capacity_utilization = Column(Integer)