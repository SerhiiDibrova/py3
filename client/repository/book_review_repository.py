

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://user:password@host:port/dbname')
Base = declarative_base()

class BookReview(Base):
    __tablename__ = 'book_reviews'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    patron_id = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=False)
    review_date = Column(DateTime, default=func.current_timestamp())
    status = Column(String, default='PENDING')

class BookReviewRepository:
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def insert_book_review(self, book_id, patron_id, rating, review_text):
        if book_id is None or patron_id is None or rating is None or review_text is None:
            raise Exception('Invalid input parameters')
        new_review = BookReview(book_id=book_id, patron_id=patron_id, rating=rating, review_text=review_text)
        session = self.Session()
        session.add(new_review)
        session.commit()
        return 'Review added successfully'