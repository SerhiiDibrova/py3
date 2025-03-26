

from sqlalchemy import Column, Integer, ForeignKey, JSON, String
from sqlalchemy.orm import relationship
from .base import BaseModel

class Registration(BaseModel):
    __tablename__ = 'registrations'
    registration_id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('programs.program_id'), nullable=False)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'), nullable=False)
    attendance_log = Column(JSON, nullable=False)
    payment_status = Column(String(50), nullable=False)

    program = relationship("Program", backref="registrations")
    patron = relationship("Patron", backref="registrations")