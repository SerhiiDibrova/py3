

from flask import request, jsonify
from models import Patron, PatronMembership, MembershipPlan, Loan, InterlibraryLoan, Fine, AuditLog
from datetime import date, timedelta
from app import db

def process_interlibrary_loan_request():
    patron = Patron.query.get(request.json['patron_id'])
    if patron.status != 'active':
        raise Exception('Patron account is not active')
    if Fine.query.filter_by(patron_id=patron.id, status='unpaid').first():
        raise Exception('Patron has pending fines')
    expected_arrival = date.today() + timedelta(days=7)
    cost = 15.00
    ill_request = InterlibraryLoan(requesting_branch_id=request.json['requesting_branch_id'], patron_id=patron.id, book_title=request.json['book_title'], isbn=request.json['isbn'], providing_institution=request.json['providing_institution'], expected_arrival=expected_arrival, cost=cost)
    db.session.add(ill_request)
    db.session.commit()
    audit_log = AuditLog(table_name='interlibrary_loans', record_id=ill_request.id, action_type='insert')
    db.session.add(audit_log)
    db.session.commit()
    return jsonify({'message': 'Interlibrary loan request processed successfully'})