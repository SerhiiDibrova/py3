

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BookReview(Base):
    __tablename__ = 'book_reviews'
    review_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer)
    book_id = Column(Integer, ForeignKey('books.book_id'))
    rating = Column(Integer)
    review_text = Column(String)

    def __init__(self, review_id, patron_id, book_id, rating, review_text):
        self.review_id = review_id
        self.patron_id = patron_id
        self.book_id = book_id
        self.rating = rating
        self.review_text = review_text