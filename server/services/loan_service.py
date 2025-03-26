

from flask import current_app
from server import db
from server.models import Loan, Reservation

class LoanService:
    def get_loan_details(self, loan_id):
        return Loan.query.get(loan_id)

    def check_maximum_extensions(self, loan_details):
        if loan_details.extensions_count >= 2:
            raise Exception('Maximum extensions reached')

    def check_for_reservations(self, book_id):
        reservations = Reservation.query.filter_by(book_id=book_id, status='PENDING').all()
        if reservations:
            raise Exception('Book has pending reservations')

    def extend_loan(self, loan_id, new_due_date, new_extensions_count):
        loan = self.get_loan_details(loan_id)
        if loan.status == 'ACTIVE':
            self.check_maximum_extensions(loan)
            self.check_for_reservations(loan.book_id)
            loan.due_date = new_due_date
            loan.extensions_count = new_extensions_count
            db.session.commit()