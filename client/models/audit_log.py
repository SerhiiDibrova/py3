

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AuditLog(db.Model):
    log_id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(50))
    record_id = db.Column(db.Integer)
    action_type = db.Column(db.String(50))
    action_timestamp = db.Column(db.DateTime)
    new_values = db.Column(db.JSON)