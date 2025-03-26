

from datetime import date
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

class Patron(BaseModel):
    __tablename__ = 'patrons'
    patron_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100))
    phone = Column(String(20))
    birth_date = Column(Date)
    membership_date = Column(Date, default=date.today)
    status = Column(String(10), default='ACTIVE')

    def __init__(self, first_name, last_name, email, phone, birth_date):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.birth_date = birth_date