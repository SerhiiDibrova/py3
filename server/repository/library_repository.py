

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, DateTime, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum

engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Status(PyEnum):
    PUBLISHED_STATUS = 'published'
    UNPUBLISHED_STATUS = 'unpublished'

class Program(Base):
    __tablename__ = 'programs'
    id = Column(Integer, primary_key=True)
    status = Column(Enum(Status))
    session_schedule = Column(DateTime)
    min_participants = Column(Integer)

class Registration(Base):
    __tablename__ = 'registrations'
    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('programs.id'))
    patron_id = Column(Integer, ForeignKey('patrons.id'))
    attendance_log = Column(String)
    payment_status = Column(String)
    program = relationship("Program", backref="registrations")
    patron = relationship("Patron", backref="registrations")

class Patron(Base):
    __tablename__ = 'patrons'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)

Base.metadata.create_all(engine)

class LibraryRepository:
    def get_program_data(self, program_id):
        program = session.query(Program).get(program_id)
        return program

    def get_registration_data(self, program_id):
        registrations = session.query(Registration).filter_by(program_id=program_id).all()
        return registrations

    def get_patron_data(self, patron_id):
        patron = session.query(Patron).get(patron_id)
        return patron

def create_waitlist_notification_batch(program_id):
    library_repository = LibraryRepository()
    program_data = library_repository.get_program_data(program_id)
    if program_data.status != Status.PUBLISHED_STATUS:
        raise Exception('Program is not in PUBLISHED status')
    paid_registrations = len([registration for registration in library_repository.get_registration_data(program_id) if registration.payment_status == 'PAID'])
    if paid_registrations < program_data.min_participants:
        create_waitlist_notification(program_id)
        cancel_program(program_id)

def create_waitlist_notification(program_id):
    # Create waitlist notification batch
    pass

def cancel_program(program_id):
    # Cancel program
    pass