

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///library.db')
Base = declarative_base()

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id')
    borrower_id = Column(Integer, ForeignKey('borrowers.id'))
    due_date = Column(DateTime)
    status = Column(String)

class Fine(Base):
    __tablename__ = 'fines'
    id = Column(Integer, primary_key=True)
    loan_id = Column(Integer, ForeignKey('loans.id'))
    amount = Column(Float)
    status = Column(String)

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    message = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class LoanRepository:
    def process_overdue_items(self):
        loans = session.query(Loan).filter(Loan.due_date < datetime.now(), Loan.status == 'ACTIVE').all()

        for loan in loans:
            days_overdue = (datetime.now() - loan.due_date).days
            fine_amount = days_overdue * 0.50

            fine = Fine(loan_id=loan.id, amount=fine_amount, status='PENDING')
            session.add(fine)

            loan.status = 'OVERDUE'
            session.add(loan)

            notification_message = f'Dear {loan.borrower.name}, the book "{loan.book.title}" is overdue by {days_overdue} days. A fine of ${fine_amount} has been issued.'
            notification = Notification(message=notification_message)
            session.add(notification)

        notifications = session.query(Notification).all()
        for notification in notifications:
            print(notification.message)