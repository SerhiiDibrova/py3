

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    category = Column(String)
    publication_date = Column(Date)
    review_date = Column(Date)
    available_copies = Column(Integer)
    status = Column(String)

    def calculate_score(self, patron_reading_history, patron_preferences):
        score = 0
        if self.category in patron_preferences:
            score += 1
        if self.author in patron_reading_history:
            score += 1
        # Add more conditions to calculate score based on the algorithm
        return score

    def update_availability(self, new_availability):
        self.available_copies = new_availability
        db.session.commit()

    def get_book_details(self):
        query = 'SELECT * FROM books WHERE book_id = :book_id'
        result = db.session.execute(query, {'book_id': self.book_id})
        return result