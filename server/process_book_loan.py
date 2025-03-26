

from flask import current_app as app
from flask import jsonify
from models import Patrons, Books, Loans, db
from datetime import date, timedelta

def process_book_loan(patron_id, book_id, loan_days):
    patron = Patrons.query.get(patron_id)
    book = Books.query.get(book_id)
    if patron and book:
        if patron.status == 'active':
            if len(patron.loans) < 5:
                loan = Loans(patron_id=patron_id, book_id=book_id, loan_date=date.today(), due_date=date.today() + timedelta(days=loan_days), status='active')
                db.session.add(loan)
                db.session.commit()
                update_book_availability(book_id, -1)
                return jsonify({'message': 'Book loan processed successfully'}), 200
            else:
                return jsonify({'message': 'Patron has reached the maximum number of loans'}), 400
        else:
            return jsonify({'message': 'Patron\'s account is not active'}), 400
    else:
        return jsonify({'message': 'Book not found'}), 404

def update_book_availability(book_id, availability):
    book = Books.query.get(book_id)
    if book:
        book.availability += availability
        db.session.commit()
    else:
        raise Exception('Book not found')