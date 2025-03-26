

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FinePayment(db.Model):
    fine_id = db.Column(db.Integer, db.ForeignKey('fine.fine_id'), primary_key=True)
    amount_paid = db.Column(db.Float, nullable=False)