

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer)
    patron_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    reservation_date = db.Column(db.DateTime)
    pickup_date = db.Column(db.DateTime)
    reservation_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50))

    def __init__(self, id, patron_id, book_id, reservation_date, pickup_date, reservation_id, status):
        self.id = id
        self.patron_id = patron_id
        self.book_id = book_id
        self.reservation_date = reservation_date
        self.pickup_date = pickup_date
        self.reservation_id = reservation_id
        self.status = status