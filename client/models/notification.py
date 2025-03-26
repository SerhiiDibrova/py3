

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Notification(db.Model):
    notification_id = db.Column(db.Integer, primary_key=True)
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.patron_id'))
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.loan_id'))
    message = db.Column(db.String(200))