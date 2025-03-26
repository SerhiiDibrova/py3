

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, timedelta

engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    category = Column(String)
    availability = Column(Integer)
    status = Column(String)

class Patron(Base):
    __tablename__ = 'patrons'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    account_status = Column(String)

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    loan_date = Column(DateTime)
    due_date = Column(DateTime)
    status = Column(String)
    patron = relationship('Patron', backref='loans')
    book = relationship('Book', backref='loans')

class BookReview(Base):
    __tablename__ = 'book_reviews'
    id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    rating = Column(Integer)
    category = Column(String)
    patron = relationship('Patron', backref='book_reviews')
    book = relationship('Book', backref='book_reviews')

Base.metadata.create_all(engine)

class BookRepository:
    def __init__(self):
        self.books = session.query(Book).all()

    def retrieve_books(self):
        return self.books

    def store_books(self, books):
        for book in books:
            session.add(book)
        session.commit()

    def get_book(self, book_id):
        return session.query(Book).filter_by(id=book_id).first()

    def update_book_availability(self, book_id, availability):
        book = session.query(Book).filter_by(id=book_id).first()
        book.availability = availability
        if availability == 1:
            book.status = 'AVAILABLE'
        else:
            book.status = 'NOT AVAILABLE'
        session.commit()

def generate_book_recommendations(patron_id):
    reading_history = session.query(Loan).filter(Loan.patron_id == patron_id).all()
    preferences = session.query(BookReview).filter(BookReview.patron_id == patron_id).all()
    scores = {}
    for book in session.query(Book).all():
        score = 0
        if book.category in [p.category for p in preferences]:
            score += 2
        if book.author in [p.author for p in preferences]:
            score += 1.5
        score += session.query(BookReview.rating).filter(BookReview.patron_id == patron_id, BookReview.category == book.category).first()[0]
        score += session.query(Loan.id).filter(Loan.patron_id.in_([p.patron_id for p in session.query(Patron).filter(Patron.category == book.category).all()]), Loan.book_id == book.id).count() * 0.1
        scores[book.id] = score
    recommended_books = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
    return [session.query(Book).filter_by(id=book[0]).first() for book in recommended_books]

def process_book_loan(patron_id, book_id, loan_days):
    book_availability = session.query(Book).filter(Book.id == book_id).first().availability
    patron_account_status = session.query(Patron).filter(Patron.id == patron_id).first().account_status
    patron_loan_count = session.query(Loan).filter(Loan.patron_id == patron_id).count()
    if book_availability == 1 and patron_account_status == 'Active' and patron_loan_count < 5:
        new_loan = Loan(patron_id=patron_id, book_id=book_id, loan_date=date.today(), due_date=date.today() + timedelta(days=loan_days), status='Checked Out')
        session.add(new_loan)
        session.commit()
        book = session.query(Book).filter_by(id=book_id).first()
        book.availability = 0
        session.commit()
        return 'Loan processed successfully.'
    else:
        raise Exception('Loan cannot be processed.')

def update_book_availability(book_id, change):
    book = session.query(Book).filter_by(id=book_id).first()
    book.availability += change
    session.commit()
    return 'Book availability updated successfully.'