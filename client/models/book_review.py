

from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BookReview(Base):
    __tablename__ = 'book_reviews'

    book_id = Column(Integer, nullable=False)
    patron_id = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=False)
    review_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='PENDING')

    def __init__(self, book_id, patron_id, rating, review_text):
        self.book_id = book_id
        self.patron_id = patron_id
        self.rating = rating
        self.review_text = review_text