

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class BranchInventory(Base):
    __tablename__ = 'branch_inventory'
    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer)
    book_id = Column(Integer)
    available_copies = Column(Integer)
    discrepancy = Column(Integer)

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer)
    book_id = Column(Integer)
    action = Column(String)
    timestamp = Column(DateTime)

def audit_inventory(branch_id):
    temp_table = 'temp_audit_results'
    session.execute(text(f'CREATE TEMPORARY TABLE {temp_table} (id SERIAL PRIMARY KEY, inventory_id INTEGER, discrepancy INTEGER)'))

    discrepancies = session.query(BranchInventory).filter(BranchInventory.branch_id == branch_id).all()
    for discrepancy in discrepancies:
        session.execute(text(f'UPDATE branch_inventory SET available_copies = available_copies - {discrepancy.discrepancy} WHERE inventory_id = {discrepancy.id}'))
        session.execute(text(f'INSERT INTO audit_log (branch_id, book_id, action, timestamp) VALUES ({branch_id}, {discrepancy.book_id}, \'AUDIT_INVENTORY\', \'{datetime.now()}\')'))

    session.execute(text(f'DROP TABLE {temp_table}'))