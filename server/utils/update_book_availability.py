

from server import db
from server.models import Book

def update_book_availability(book_id, availability):
    book = Book.query.get(book_id)
    if book is None:
        raise Exception('Book not found')
    book.availability = availability
    if availability == 1:
        book.status = 'AVAILABLE'
    else:
        book.status = 'NOT AVAILABLE'
    db.session.commit()