

from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date

engine = create_engine('sqlite:///fine.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Fine(Base):
    __tablename__ = 'fines'
    fine_id = Column(Integer, primary_key=True)
    amount = Column(Float)
    status = Column(String)
    payment_date = Column(Date)

Base.metadata.create_all(engine)

class FineService:
    def process_fine_payment(self, fine_id, amount_paid):
        fine = session.query(Fine).filter_by(fine_id=fine_id, status='PENDING').first()
        if fine is None:
            raise Exception('Valid unpaid fine not found')
        if amount_paid < fine.amount:
            remaining_amount = fine.amount - amount_paid
            raise Exception('Partial payments not supported')
        fine.status = 'PAID'
        fine.payment_date = date.today()
        session.commit()
        return 'Fine payment processed successfully'