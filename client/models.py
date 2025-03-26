

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class EventRegistration(db.Model):
    event_registration_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('library_event.event_id'))
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.patron_id'))
    registration_date = db.Column(db.DateTime, default=datetime.now)
    attendance_status = db.Column(db.String(50), default='REGISTERED')

class LibraryEvent(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    max_participants = db.Column(db.Integer)
    current_participants = db.Column(db.Integer, default=0)

class PatronMembership(db.Model):
    membership_id = db.Column(db.Integer, primary_key=True)
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.patron_id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('membership_plan.plan_id'))
    end_date = db.Column(db.Date)
    auto_renewal = db.Column(db.Boolean)
    price = db.Column(db.Float)
    duration_months = db.Column(db.Integer)

class MembershipPlan(db.Model):
    plan_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

class Patron(db.Model):
    patron_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

class Fine(db.Model):
    fine_id = db.Column(db.Integer, primary_key=True)
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.patron_id'))
    amount = db.Column(db.Float)

class Loan(db.Model):
    loan_id = db.Column(db.Integer, primary_key=True)
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.patron_id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'))
    due_date = db.Column(db.Date)

class AuditLog(db.Model):
    log_id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String)
    record_id = db.Column(db.Integer)
    action_type = db.Column(db.String)
    action_timestamp = db.Column(db.DateTime)
    new_values = db.Column(db.JSON)