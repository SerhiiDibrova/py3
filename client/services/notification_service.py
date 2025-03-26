

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///notifications.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    message = Column(String)

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    table_name = Column(String)
    record_id = Column(Integer)
    action_type = Column(String)
    action_timestamp = Column(String)
    new_values = Column(String)

Base.metadata.create_all(engine)

class NotificationService:
    def queue_notification(self, notification_message):
        notification = Notification(message=notification_message)
        session.add(notification)
        session.commit()

    def log_notification_in_audit_log(self, notification):
        audit_log = AuditLog(table_name='notifications', record_id=notification.id, action_type='CREATE', action_timestamp=str(datetime.now()), new_values=str({'message': notification.message}))
        session.add(audit_log)
        session.commit()