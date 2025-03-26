

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Patrons(Base):
    __tablename__ = 'patrons'
    patron_id = Column(Integer, primary_key=True)
    patron_name = Column(String)
    patron_email = Column(String)
    registrations = relationship('EventRegistrations', backref='patrons')