

from flask import Blueprint, request, jsonify
from datetime import date
from ..models import Loan, Fine
from .. import db

loan_controller = Blueprint('loan_controller', __name__)

@loan_controller.route('/active_loans', methods=['GET'])
def get_active_loans():
    loans = Loan.query.filter(Loan.due_date < date.today(), Loan.fine == None).all()
    return jsonify([loan.to_dict() for loan in loans])

@loan_controller.route('/fine_records', methods=['POST'])
def create_fine_record():
    data = request.get_json()
    fine = Fine(loan_id=data['loan_id'], amount=data['fine_amount'], status='PENDING')
    db.session.add(fine)
    db.session.commit()
    return jsonify(fine.to_dict())

@loan_controller.route('/loan_status', methods=['PUT'])
def update_loan_status():
    data = request.get_json()
    loan = Loan.query.get(data['loan_id'])
    loan.status = 'OVERDUE'
    db.session.commit()
    return jsonify(loan.to_dict())