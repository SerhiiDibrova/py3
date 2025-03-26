

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models import Books

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)

def update_book_availability(book_id, availability):
    session = Session()
    book = session.query(Books).filter_by(book_id=book_id).first()
    if book is None:
        raise Exception('Book not found')

    book.availability = availability

    if availability == 1:
        book.status = 'AVAILABLE'
    elif availability == 0:
        book.status = 'NOT AVAILABLE'

    session.commit()