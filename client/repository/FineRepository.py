

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

Base = declarative_base()

class Fine(Base):
    __tablename__ = 'fines'
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    status = Column(String)
    payment_date = Column(DateTime)

class FineRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def process_fine_payment(self, fine_id, amount_paid):
        fine = self.db_session.query(Fine).filter_by(id=fine_id, status='PENDING').first()
        if fine is None:
            raise Exception('Valid unpaid fine not found')

        if amount_paid < fine.amount:
            remaining_amount = fine.amount - amount_paid
            raise Exception('Partial payments not supported')

        fine.status = 'PAID'
        fine.payment_date = datetime.now()
        self.db_session.commit()

        return 'Fine payment processed successfully'