

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Patron(Base):
    __tablename__ = 'patrons'
    patron_id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    reading_history = Column(String)
    preferences = Column(String)
    status = Column(String(50), default='active')
    active_loans = Column(Integer, default=0))

    def __init__(self, patron_id, email, first_name, last_name):
        self.patron_id = patron_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def retrieve_reading_history(self):
        return self.reading_history

    def retrieve_preferences(self):
        return self.preferences

    def check_status(self):
        if self.status != 'active':
            raise Exception('Patron account is not active')

    def check_active_loans(self):
        MAX_LOANS = 5
        if self.active_loans >= MAX_LOANS:
            raise Exception('Patron has reached the maximum number of loans')

    def get_patron_summary(self):
        engine = create_engine('sqlite:///patron.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        query = session.query(Patron).filter(Patron.patron_id == self.patron_id).first()
        return query

    def __repr__(self):
        return f'Patron(patron_id={self.patron_id}, email={self.email}, first_name={self.first_name}, last_name={self.last_name})'