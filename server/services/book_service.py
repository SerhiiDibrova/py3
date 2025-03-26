

from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from server.repositories.book_repository import BookRepository
from server.repositories.patron_repository import PatronRepository
from server.models.loan import Loan
from server.config import MAX_LOANS, DEFAULT_LOAN_DAYS

class BookService:
    def __init__(self):
        self.engine = create_engine('sqlite:///library.db')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def process_book_loan(self, book_id, patron_id):
        book_repository = BookRepository(self.session)
        patron_repository = PatronRepository(self.session)

        book = book_repository.get_book(book_id)
        patron = patron_repository.get_patron(patron_id)

        if book.available_copies <= 0:
            raise Exception('Book is not available for loan')

        if patron.status != 'active':
            raise Exception('Patron account is not active')

        active_loans = self.session.query(Loan).filter_by(patron_id=patron_id, status='active').count()
        if active_loans >= MAX_LOANS:
            raise Exception('Patron has reached the maximum number of loans')

        loan = Loan(patron_id=patron_id, book_id=book_id, loan_date=date.today(), due_date=date.today() + timedelta(days=DEFAULT_LOAN_DAYS), status='active')
        self.session.add(loan)
        self.session.commit()

        book.available_copies -= 1
        self.session.commit()