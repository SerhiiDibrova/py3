

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Numeric, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Patron(Base):
    __tablename__ = 'patrons'
    patron_id = Column(Integer, primary_key=True)
    status = Column(String)
    email = Column(String)
    name = Column(String)
    reading_history = Column(String)
    preferences = Column(String)
    loans = relationship("Loan", backref="patron")
    book_reviews = relationship("BookReview", backref="patron")
    patron_memberships = relationship("PatronMembership", backref="patron")
    interlibrary_loans = relationship("InterlibraryLoan", backref="patron")
    fines = relationship("Fine", backref="patron")
    registrations = relationship("Registration", backref="patron")
    waitlists = relationship("Waitlist", backref="patron")
    event_registrations = relationship("EventRegistration", backref="patron")

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    publication_date = Column(Date)
    available_copies = Column(Integer)
    category = Column(String)
    isbn = Column(String)
    loans = relationship("Loan", backref="book")
    book_reviews = relationship("BookReview", backref="book")
    branch_inventory = relationship("BranchInventory", backref="book")

class Loan(Base):
    __tablename__ = 'loans'
    loan_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    loan_date = Column(Date)
    due_date = Column(Date)
    status = Column(String)

class BookReview(Base):
    __tablename__ = 'book_reviews'
    review_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    review_date = Column(Date)
    rating = Column(Integer)

class MembershipPlan(Base):
    __tablename__ = 'membership_plans'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Numeric)
    loan_limit = Column(Integer)
    max_loans = Column(Integer)
    patron_memberships = relationship("PatronMembership", backref="membership_plan")

class PatronMembership(Base):
    __tablename__ = 'patron_memberships'
    id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    membership_plan_id = Column(Integer, ForeignKey('membership_plans.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String)

class InterlibraryLoan(Base):
    __tablename__ = 'interlibrary_loans'
    id = Column(Integer, primary_key=True)
    requesting_branch_id = Column(Integer, ForeignKey('branch.branch_id'))
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    book_title = Column(String)
    isbn = Column(String)
    providing_institution = Column(String)
    expected_arrival = Column(Date)
    cost = Column(Float)

class Fine(Base):
    __tablename__ = 'fines'
    fine_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    amount = Column(Float)
    status = Column(String)

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    action = Column(String)
    parameters = Column(JSON)
    results = Column(JSON)
    timestamp = Column(DateTime)

class Program(Base):
    __tablename__ = 'programs'
    program_id = Column(Integer, primary_key=True)
    status = Column(String)
    session_schedule = Column(JSON)
    min_participants = Column(Integer)
    registrations = relationship("Registration", backref="program")
    waitlists = relationship("Waitlist", backref="program")

class Registration(Base):
    __tablename__ = 'registrations'
    registration_id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('programs.program_id'))
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    attendance_log = Column(JSON)
    payment_status = Column(String)
    attendance_records = relationship("AttendanceRecord", backref="registration")

class Waitlist(Base):
    __tablename__ = 'waitlists'
    waitlist_id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('programs.program_id'))
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))

class BranchInventory(Base):
    __tablename__ = 'branch_inventory'
    inventory_id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, ForeignKey('branch.branch_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    available_copies = Column(Integer)
    damaged_copies = Column(Integer)
    status = Column(String)

class LibraryEvent(Base):
    __tablename__ = 'library_events'
    event_id = Column(Integer, primary_key=True)
    event_name = Column(String)
    event_date = Column(Date)
    event_status = Column(String)
    event_registrations = relationship("EventRegistration", backref="library_event")

class EventRegistration(Base):
    __tablename__ = 'event_registrations'
    registration_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('library_events.event_id'))
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    registration_status = Column(String)

class AttendanceRecord(Base):
    __tablename__ = 'attendance_records'
    attendance_id = Column(Integer, primary_key=True)
    registration_id = Column(Integer, ForeignKey('registrations.registration_id'))
    attendance_status = Column(String)