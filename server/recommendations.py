

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Patron, Book, Loan, BookReview

def generate_book_recommendations(patron_id):
    engine = create_engine('postgresql://user:password@host:port/dbname')
    Session = sessionmaker(bind=engine)
    session = Session()

    patron = session.query(Patron).filter_by(patron_id=patron_id).first()
    reading_history = patron.reading_history
    preferences = patron.preferences

    similar_patrons = session.query(Patron).filter_by(reading_history=reading_history).all()

    recommended_books = []
    for book in session.query(Book).all():
        score = 0
        if book.category in reading_history:
            score += 2
        if book.author in reading_history:
            score += 1.5
        if book.category in preferences:
            score += 1
        if book.author in preferences:
            score += 0.5

        similar_patrons_borrowing_count = 0
        for similar_patron in similar_patrons:
            if similar_patron.reading_history.contains(book.book_id):
                similar_patrons_borrowing_count += 1
        score += similar_patrons_borrowing_count * 0.1

        if book.available_copies > 0 and book.book_id not in reading_history:
            recommended_books.append((book, score))

    recommended_books.sort(key=lambda x: x[1], reverse=True)
    return recommended_books[:10]