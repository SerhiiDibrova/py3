

from flask import Blueprint, request, jsonify
from server import db
from server.models import Loans, Fines
from server.services import loan_service
from server.utils import update_book_availability
from datetime import date

loan_controller = Blueprint('loan_controller', __name__)

class LoanController:
    def extend_loan_period(self, p_loan_id, p_extension_days):
        loan_service.extend_loan(p_loan_id, p_extension_days)
        return {'message': 'Loan extended successfully'}

    def process_book_return(self, loan_id):
        loan = Loans.query.filter_by(loan_id=loan_id, status='ACTIVE').first()
        if loan is None:
            raise Exception('Loan not found')
        days_overdue = (date.today() - loan.due_date).days
        if days_overdue > 0:
            fine_amount = days_overdue * 0.50
        fine = Fines(patron_id=loan.patron_id, loan_id=loan.loan_id, amount=fine_amount, issue_date=date.today(), due_date=date.today(), status='PENDING')
        db.session.add(fine)
        loan.status = 'RETURNED'
        loan.return_date = date.today()
        db.session.commit()
        update_book_availability(loan.book_id, 1)

@loan_controller.route('/extend_loan_period', methods=['POST'])
def extend_loan_period():
    data = request.get_json()
    p_loan_id = data['loan_id']
    p_extension_days = data['extension_days']
    loan_controller = LoanController()
    return jsonify(loan_controller.extend_loan_period(p_loan_id, p_extension_days))

@loan_controller.route('/process_book_return', methods=['POST'])
def process_book_return():
    data = request.get_json()
    loan_id = data['loan_id']
    loan_controller = LoanController()
    loan_controller.process_book_return(loan_id)
    return jsonify({'message': 'Book returned successfully'})