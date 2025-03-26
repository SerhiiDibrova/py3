

from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Loans(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    patron_id = Column(Integer, ForeignKey('patrons.id'))
    loan_date = Column(Date)
    return_date = Column(Date)

    def __init__(self, id, book_id, patron_id, loan_date, return_date):
        self.id = id
        self.book_id = book_id
        self.patron_id = patron_id
        self.loan_date = loan_date
        self.return_date = return_date