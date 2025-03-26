

from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, Enum
from sqlalchemy.exc import IntegrityError

engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Loans(Base):
    __tablename__ = 'loans'
    loan_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer)
    book_id = Column(Integer)
    status = Column(Enum('ACTIVE', 'RETURNED'))
    due_date = Column(Date)
    return_date = Column(Date)
    extensions_count = Column(Integer)

class Reservations(Base):
    __tablename__ = 'reservations'
    reservation_id = Column(Integer, primary_key=True)
    book_id = Column(Integer)
    status = Column(Enum('PENDING', 'CANCELLED'))

class Fines(Base):
    __tablename__ = 'fines'
    fine_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer)
    loan_id = Column(Integer)
    amount = Column(Float)
    issue_date = Column(Date)
    due_date = Column(Date)
    status = Column(Enum('PENDING', 'PAID'))

Base.metadata.create_all(engine)

class LoanRepository:
    def get_loan(self, loan_id):
        loan = session.query(Loans).filter_by(loan_id=loan_id).first()
        return loan

    def update_loan_status(self, loan_id, status):
        loan = session.query(Loans).filter_by(loan_id=loan_id).first()
        loan.status = status
        session.commit()

    def extend_loan_period(self, p_loan_id, p_extension_days=7):
        loan_details = session.query(Loans).filter_by(loan_id=p_loan_id, status='ACTIVE').first()
        if loan_details is None:
            raise Exception('Active loan not found')
        if loan_details.extensions_count >= 2:
            raise Exception('Maximum extensions reached')
        pending_reservations = session.query(Reservations).filter_by(book_id=loan_details.book_id, status='PENDING').all()
        if pending_reservations:
            raise Exception('Book has pending reservations')
        loan_details.due_date += timedelta(days=p_extension_days)
        loan_details.extensions_count += 1
        session.commit()

    def process_book_return(self, loan_id):
        loan_details = session.query(Loans).filter_by(loan_id=loan_id, status='ACTIVE').first()
        if loan_details is None:
            raise Exception('Loan not found')
        days_overdue = (datetime.now().date() - loan_details.due_date).days
        if days_overdue > 0:
            fine_amount = days_overdue * 0.50
            fine = Fines(patron_id=loan_details.patron_id, loan_id=loan_id, amount=fine_amount, issue_date=datetime.now().date(), due_date=datetime.now().date() + timedelta(days=30), status='PENDING')
            session.add(fine)
        loan_details.status = 'RETURNED'
        loan_details.return_date = datetime.now().date()
        session.commit()

def update_book_availability(book_id, availability):
    # This function should be implemented according to the actual database schema and requirements
    pass