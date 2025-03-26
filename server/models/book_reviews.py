

from sqlalchemy import Column, Integer, ForeignKey, Date, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BookReviews(Base):
    __tablename__ = 'book_reviews'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    patron_id = Column(Integer, ForeignKey('patrons.id'))
    review_date = Column(Date)
    rating = Column(Integer)
    review = Column(String)

    def __init__(self, id, book_id, patron_id, rating, review, review_date=None):
        self.id = id
        self.book_id = book_id
        self.patron_id = patron_id
        self.rating = rating
        self.review = review
        self.review_date = review_date