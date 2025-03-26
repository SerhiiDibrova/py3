

from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()

class Program(Base):
    __tablename__ = 'programs'
    program_id = Column(Integer, primary_key=True)
    status = Column(String(50), nullable=False)
    session_schedule = Column(JSONB, nullable=False)
    min_participants = Column(Integer, nullable=False)

    def __init__(self, program_id, status, session_schedule, min_participants):
        self.program_id = program_id
        self.status = status
        self.session_schedule = session_schedule
        self.min_participants = min_participants

    def __repr__(self):
        return f'Program(program_id={self.program_id}, status={self.status}, session_schedule={self.session_schedule}, min_participants={self.min_participants})'

    def start_program(self):
        # Call start_program method from program controller
        program_controller.start_program(self.program_id)

    def record_attendance(self):
        # Call record_attendance method from program controller
        program_controller.record_attendance(self.program_id)

    def complete_program(self):
        # Call complete_program method from program controller
        program_controller.complete_program(self.program_id)