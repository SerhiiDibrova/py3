

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///fines.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Fine(Base):
    __tablename__ = 'fines'
    id = Column(Integer, primary_key=True)
    fine_id = Column(String)
    details = Column(String)

Base.metadata.create_all(engine)

class FineRepository:
    def get_fine(self, fine_id):
        fine = session.query(Fine).filter_by(fine_id=fine_id).first()
        return fine