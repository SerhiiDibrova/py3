

from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Loan(Base):
    __tablename__ = 'loans'
    loan_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    loan_date = Column(Date)
    due_date = Column(Date)
    return_date = Column(Date)
    status = Column(String(50))
    extensions_count = Column(Integer)

    patron = relationship('Patron', backref='loans')
    book = relationship('Book', backref='loans')

    def __init__(self, loan_id, patron_id, book_id, loan_date, due_date, return_date, status, extensions_count):
        self.loan_id = loan_id
        self.patron_id = patron_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.due_date = due_date
        self.return_date = return_date
        self.status = status
        self.extensions_count = extensions_count

    def create_loan(self, db):
        db.session.add(self)
        db.session.commit()

    def update_due_date_and_extensions(self, new_due_date, new_extensions_count):
        self.due_date = new_due_date
        self.extensions_count = new_extensions_count

    def get_loan_details(self, db):
        query = 'SELECT * FROM loans WHERE loan_id = :loan_id'
        result = db.session.execute(query, {'loan_id': self.loan_id})
        return result

    def update_due_date(self, p_extension_days):
        self.due_date = self.due_date + timedelta(days=p_extension_days)
        self.extensions_count += 1

engine = create_engine('sqlite:///library.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db = Session()