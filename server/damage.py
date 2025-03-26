

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class BranchInventory(Base):
    __tablename__ = 'branch_inventory'
    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer)
    damaged_copies = Column(Integer)
    available_copies = Column(Integer)
    status = Column(String)

def process_damages(branch_id, damaged_count):
    session.execute(text(f'UPDATE branch_inventory SET damaged_copies = damaged_copies + {damaged_count}, available_copies = available_copies - {damaged_count} WHERE branch_id = {branch_id}'))

    critical_threshold = 5
    damaged_copies = session.query(BranchInventory).filter(BranchInventory.branch_id == branch_id).first().damaged_copies
    if damaged_copies >= critical_threshold:
        session.execute(text(f"UPDATE branch_inventory SET status = 'DISCONTINUED' WHERE branch_id = {branch_id}"))