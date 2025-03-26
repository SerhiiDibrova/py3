

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Fine(db.Model):
    fine_id = db.Column(db.Integer, primary_key=True)
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.patron_id'))
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.loan_id'))
    amount = db.Column(db.Float, nullable=False)
    issue_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(50), nullable=False, default='PENDING')
    payment_date = db.Column(db.Date, nullable=True)

    def update_status(self, status, payment_date):
        self.status = status
        self.payment_date = payment_date