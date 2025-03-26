

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import AuditLog

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)

def create_audit_log_entry(patron_id, action, timestamp):
    session = Session()
    audit_log_entry = AuditLog(patron_id=patron_id, action=action, timestamp=timestamp)
    session.add(audit_log_entry)
    session.commit()

def update_audit_log_entry(audit_log_id, patron_id, action, timestamp):
    session = Session()
    audit_log_entry = session.query(AuditLog).filter_by(audit_log_id=audit_log_id).first()
    audit_log_entry.patron_id = patron_id
    audit_log_entry.action = action
    audit_log_entry.timestamp = timestamp
    session.commit()

def get_audit_log_entries(patron_id):
    session = Session()
    audit_log_entries = session.query(AuditLog).filter_by(patron_id=patron_id).all()
    return audit_log_entries