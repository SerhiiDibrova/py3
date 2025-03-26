

from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Patron(Base):
    __tablename__ = 'patrons'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    due_date = Column(String)
    status = Column(String)
    fine = Column(Float)
    patron = relationship('Patron')
    book = relationship('Book')

class Fine(Base):
    __tablename__ = 'fines'
    id = Column(Integer, primary_key=True)
    loan_id = Column(Integer, ForeignKey('loans.id'))
    amount = Column(Float)
    status = Column(String)

Base.metadata.create_all(engine)

class LoanService:
    def get_active_loans(self):
        loans = session.query(Loan).filter(Loan.due_date < date.today().isoformat(), Loan.fine == None).all()
        return loans

    def calculate_fine_amount(self, loan):
        days_overdue = (date.today() - date.fromisoformat(loan.due_date)).days
        fine_amount = days_overdue * 0.50
        return fine_amount

    def create_fine_record(self, loan, fine_amount):
        fine = Fine(loan_id=loan.id, amount=fine_amount, status='PENDING')
        session.add(fine)
        session.commit()

    def update_loan_status(self, loan):
        loan.status = 'OVERDUE'
        session.commit()

    def prepare_notification_message(self, loan, fine_amount):
        days_overdue = (date.today() - date.fromisoformat(loan.due_date)).days
        notification_message = f'Dear {loan.patron.name}, the book "{loan.book.title}" is overdue by {days_overdue} days. A fine of ${fine_amount} has been issued.'
        return notification_message