

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Patron, Loan, Fine, EventRegistration, AuditLog
from datetime import datetime

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)

def suspend_patron_account(patron_id):
    session = Session()
    patron = session.query(Patron).filter_by(patron_id=patron_id).first()
    if patron.status == 'SUSPENDED':
        raise Exception('Patron account is already suspended')
    patron.status = 'SUSPENDED'
    session.commit()

def reactivate_patron_account(patron_id):
    session = Session()
    patron = session.query(Patron).filter_by(patron_id=patron_id).first()
    if patron.status == 'ACTIVE':
        raise Exception('Patron account is already active')
    patron.status = 'ACTIVE'
    session.commit()

def audit_patron_account(patron_id):
    session = Session()
    patron = session.query(Patron).filter_by(patron_id=patron_id).first()
    audit_log_entry = AuditLog(patron_id=patron_id, action='AUDIT_ACTIVITY', timestamp=datetime.now())
    session.add(audit_log_entry)
    session.commit()