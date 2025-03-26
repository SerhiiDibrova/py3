

from flask import Blueprint, request, jsonify
from server import db
from server.models import Book, Patron, Loan
from datetime import date, timedelta

book_loan_controller = Blueprint('book_loan_controller', __name__)

MAX_LOANS = 5
DEFAULT_LOAN_DAYS = 14

@book_loan_controller.route('/process_book_loan', methods=['POST'])
def process_book_loan():
    data = request.get_json()
    book_id = data['book_id']
    patron_id = data['patron_id']

    book = Book.query.get(book_id)
    if book.available_copies <= 0:
        return jsonify({'error': 'Book is not available for loan'}), 400

    patron = Patron.query.get(patron_id)
    if patron.status != 'active':
        return jsonify({'error': 'Patron account is not active'}), 400

    active_loans = Loan.query.filter_by(patron_id=patron_id, status='active').count()
    if active_loans >= MAX_LOANS:
        return jsonify({'error': 'Patron has reached the maximum number of loans'}), 400

    loan = Loan(patron_id=patron_id, book_id=book_id, loan_date=date.today(), due_date=date.today() + timedelta(days=DEFAULT_LOAN_DAYS), status='active')
    db.session.add(loan)
    db.session.commit()

    book.available_copies -= 1
    db.session.commit()

    return jsonify({'message': 'Book loan processed successfully'}), 200