

from sqlalchemy import create_engine, Column, Integer, String, Date, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Patron(Base):
    __tablename__ = 'patron'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

class PatronStatus(Base):
    __tablename__ = 'patron_status'
    id = Column(Integer, primary_key=True)
    patron_id = Column(Integer)
    status = Column(Enum('active', 'inactive'))

class Fine(Base):
    __tablename__ = 'fine'
    id = Column(Integer, primary_key=True)
    patron_id = Column(Integer)
    amount = Column(Float)
    status = Column(Enum('paid', 'unpaid'))

class InterlibraryLoan(Base):
    __tablename__ = 'interlibrary_loans'
    id = Column(Integer, primary_key=True)
    requesting_branch_id = Column(Integer)
    patron_id = Column(Integer)
    book_title = Column(String)
    isbn = Column(String)
    providing_institution = Column(String)
    expected_arrival = Column(Date)
    cost = Column(Float)
    status = Column(Enum('active', 'inactive'))

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    table_name = Column(String)
    record_id = Column(Integer)
    action_type = Column(Enum('insert', 'update', 'delete'))

class InterlibraryLoanRepository:
    def __init__(self):
        self.session = session

    def retrieve_patron_record(self, patron_id):
        patron = self.session.query(Patron).get(patron_id)
        if patron is None:
            raise Exception('Patron not found')
        return patron

    def insert_request_into_database(self, request):
        patron_status = self.session.query(PatronStatus).filter_by(patron_id=request.patron_id, status='active').first()
        if patron_status is None:
            raise Exception('Patron account is not active')

        fines = self.session.query(Fine).filter_by(patron_id=request.patron_id, status='unpaid').all()
        if len(fines) > 0:
            raise Exception('Patron has pending fines')

        active_loans = self.session.query(InterlibraryLoan).filter_by(patron_id=request.patron_id, status='active').all()
        if len(active_loans) >= 2:
            raise Exception('Patron has exceeded maximum active interlibrary loan requests')

        expected_arrival = date.today() + timedelta(days=7)
        cost = 15.00

        interlibrary_loan = InterlibraryLoan(requesting_branch_id=request.requesting_branch_id, patron_id=request.patron_id, book_title=request.book_title, isbn=request.isbn, providing_institution=request.providing_institution, expected_arrival=expected_arrival, cost=cost)
        self.session.add(interlibrary_loan)
        self.session.commit()

        audit_log = AuditLog(table_name='interlibrary_loans', record_id=interlibrary_loan.id, action_type='insert')
        self.session.add(audit_log)
        self.session.commit()

        return interlibrary_loan.id

    def create_tracking_record(self, request):
        audit_log = AuditLog(table_name='interlibrary_loans', record_id=request.id, action_type='insert')
        self.session.add(audit_log)
        self.session.commit()
        return audit_log.id