

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Book, Patron, Loan
from datetime import date, timedelta

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)

def process_book_loan(book_id, patron_id):
    session = Session()
    book = session.query(Book).get(book_id)
    patron = session.query(Patron).get(patron_id)

    if book.available_copies <= 0:
        raise Exception('Book is not available for loan.')

    if patron.status != 'active':
        raise Exception('Patron account is not active.')

    if patron.active_loans >= 5:
        raise Exception('Patron has reached the maximum number of loans.')

    loan = Loan(patron_id=patron_id, book_id=book_id, loan_date=date.today(), due_date=date.today() + timedelta(days=14), status='ACTIVE')
    session.add(loan)
    session.commit()

    book.available_copies -= 1
    session.commit()