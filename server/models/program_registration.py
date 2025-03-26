

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ProgramRegistration(Base):
    __tablename__ = 'program_registrations'
    registration_id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('programs.program_id'))
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    attendance_log = Column(String)
    payment_status = Column(String)

    program = relationship("Program", backref="program_registrations")
    patron = relationship("Patron", backref="program_registrations")

    def __init__(self, registration_id, program_id, patron_id, attendance_log, payment_status):
        self.registration_id = registration_id
        self.program_id = program_id
        self.patron_id = patron_id
        self.attendance_log = attendance_log
        self.payment_status = payment_status

    def __repr__(self):
        return f'ProgramRegistration(registration_id={self.registration_id}, program_id={self.program_id}, patron_id={self.patron_id}, attendance_log={self.attendance_log}, payment_status={self.payment_status})'

    def is_valid(self):
        if self.registration_id and self.program_id and self.patron_id and self.attendance_log and self.payment_status:
            return True
        return False