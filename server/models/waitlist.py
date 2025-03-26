

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Waitlist(db.Model):
    __tablename__ = 'waitlist'
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'))
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.id'))