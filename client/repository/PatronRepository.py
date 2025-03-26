

from datetime import date
from sqlalchemy import create_engine, Column, String, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///library.db')
Base = declarative_base()

class Patron(Base):
    __tablename__ = 'patrons'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    birth_date = Column(Date)
    membership_date = Column(Date)
    status = Column(Enum('ACTIVE', 'INACTIVE'))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class PatronRepository:
    def create_patron(self, first_name, last_name, email, phone, birth_date):
        if not all([first_name, last_name, email, phone, birth_date]):
            raise ValueError('Invalid input parameters')
        patron = Patron(first_name=first_name, last_name=last_name, email=email, phone=phone, birth_date=birth_date, membership_date=date.today(), status='ACTIVE')
        session.add(patron)
        session.commit()
        return 'Patron created successfully'