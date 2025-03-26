

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from server.models import Program, Registration, Waitlist, Loans, Fines, AuditLog

app = Flask(__name__)

# Create engine and session
engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)
db = Session()

class LibraryService:
    def create_waitlist_notification_batch(program_id):
        # Create waitlist notification batch
        waitlist = Waitlist(program_id=program_id)
        db.session.add(waitlist)
        db.session.commit()

    def ensure_data_integrity(program_id):
        # Ensure data integrity by updating program and registration records consistently
        program = Program.query.get(program_id)
        registrations = Registration.query.filter_by(program_id=program_id).all()
        # Update program and registration records
        program.status = 'COMPLETED'
        for registration in registrations:
            registration.payment_status = 'PAID'
        db.session.commit()

    def log_errors(error):
        # Log errors in the audit log table
        audit_log = AuditLog(error=error)
        db.session.add(audit_log)
        db.session.commit()

    def process_book_return(loan_id):
        session = Session()
        loan = session.query(Loans).filter_by(loan_id=loan_id, status='ACTIVE').first()
        if loan is None:
            raise Exception('Loan not found')

        due_date = loan.due_date
        current_date = date.today()
        days_overdue = (current_date - due_date).days

        if days_overdue > 0:
            fine_amount = days_overdue * 0.50
            fine = Fines(patron_id=loan.patron_id, loan_id=loan.loan_id, amount=fine_amount, issue_date=current_date, due_date=current_date, status='PENDING')
            session.add(fine)

        loan.status = 'RETURNED'
        loan.return_date = current_date

        update_book_availability(loan.book_id, 1)

        session.commit()

def update_book_availability(book_id, quantity):
    # Update book availability
    book = Book.query.get(book_id)
    book.quantity += quantity
    db.session.commit()

@app.route('/create_waitlist_notification_batch', methods=['POST'])
def create_waitlist_notification_batch():
    # Retrieve program data
    program_id = request.json['program_id']
    program = Program.query.get(program_id)

    # Check if program is in PUBLISHED status
    if program.status != 'PUBLISHED':
        return jsonify({'error': 'Program is not in PUBLISHED status'}), 400

    # Check if number of paid registrations meets minimum required
    paid_registrations = Registration.query.filter_by(program_id=program_id, payment_status='PAID').count()
    if paid_registrations < program.min_participants:
        # Create waitlist notification batch
        waitlist = Waitlist(program_id=program_id, patron_id=patron_id)
        db.session.add(waitlist)
        db.session.commit()

        # Cancel program
        program.status = 'COMPLETED'
        db.session.commit()

    return jsonify({'message': 'Waitlist notification batch created successfully'}), 201