

from server import db

class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_records'
    attendance_id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registrations.registration_id'))
    attendance_status = db.Column(db.String(50))
    program_id = db.Column(db.Integer, db.ForeignKey('programs.program_id'))