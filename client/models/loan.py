

from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Loan(db.Model):
    loan_id = db.Column(db.Integer, primary_key=True)
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.patron_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))
    due_date = db.Column(db.Date)
    status = db.Column(db.String(50))

    def __init__(self, patron_id, book_id, due_date, status):
        self.patron_id = patron_id
        self.book_id = book_id
        self.due_date = due_date
        self.status = status

    def calculate_fine_amount(self):
        days_overdue = (date.today() - self.due_date).days
        fine_amount = days_overdue * 0.50
        return fine_amount

    @classmethod
    def get_active_loans(cls):
        loans = cls.query.filter(cls.due_date < date.today(), cls.fine == None).all()
        return loans

    def create_fine_record(self, fine_amount):
        fine = Fine(loan_id=self.loan_id=self.loan_id, amount=fine_amount, status='PENDING')
        db.session.add(fine)
        db.session.commit()

    def update_loan_status(self):
        self.status = 'OVERDUE'
        db.session.commit()

    def prepare_notification_message(self, fine_amount):
        days_overdue = (date.today() - self.due_date).days
        notification_message = f'Dear {self.patron.name}, the book "{self.book.title}" is overdue by {days_overdue} days. A fine of ${fine_amount} has been issued.'
        return notification_message