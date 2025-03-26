

from sqlalchemy import Column, Integer, Date, ForeignKey, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Fine(Base):
    __tablename__ = 'fines'
    fine_id = Column(Integer, primary_key=True)
    loan_id = Column(Integer, ForeignKey('loans.loan_id'))
    fine_amount = Column(Integer)
    paid_date = Column(Date)
    issue_date = Column(Date)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    amount = Column(Float)
    due_date = Column(Date)
    status = Column(String(50))

    patron = relationship('Patron', backref=backref('fines', lazy=True))
    loan = relationship('Loan', backref=backref('fines', lazy=True))

    def __init__(self, fine_id, patron_id, amount):
        self.fine_id = fine_id
        self.patron_id = patron_id
        self.amount = amount

    def get_fine_details(self, session):
        return session.query(Fine).filter(Fine.fine_id == self.fine_id).first()

    def update_fine_status(self, session, status):
        self.status = status
        session.commit()

def execute_query(query, params, session):
    return session.execute(query, params)

def create_session():
    engine = create_engine('sqlite:///example.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()