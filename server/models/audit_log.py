

from sqlalchemy import Column, Integer, String, ForeignKey, JSON, JSONB, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    action = Column(String)
    collection_id = Column(Integer, ForeignKey('book_collections.id'))
    recommendations = Column(JSON)
    log_id = Column(Integer)
    event_id = Column(Integer, ForeignKey('library_events.event_id'))
    log_message = Column(String)
    table_name = Column(String)
    record_id = Column(Integer)
    action_type = Column(String)
    action_timestamp = Column(DateTime)
    new_values = Column(JSONB)
    library_events = relationship('LibraryEvents', backref='audit_log')

    def __init__(self, id, action, collection_id, recommendations, log_id, event_id, log_message, table_name, record_id, action_type, action_timestamp, new_values):
        self.id = id
        self.action = action
        self.collection_id = collection_id
        self.recommendations = recommendations
        self.log_id = log_id
        self.event_id = event_id
        self.log_message = log_message
        self.table_name = table_name
        self.record_id = record_id
        self.action_type = action_type
        self.action_timestamp = action_timestamp
        self.new_values = new_values

    def get_audit_log_details(self):
        # Execute query to get audit log details
        query = 'SELECT * FROM audit_logs WHERE audit_log_id = :audit_log_id'
        result = execute_query(query, {'audit_log_id': self.id})
        return result