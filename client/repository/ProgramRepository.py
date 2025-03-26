

package repository

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Program, Registration, ProgramStatus, AuditLog

class ProgramRepository:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def calculate_completion_statistics(self, program_id):
        program_data = self.session.query(Program).filter_by(program_id=program_id).first()
        registration_data = self.session.query(Registration).filter_by(program_id=program_id).all()
        completion_rate = (len([r for r in registration_data if r.attendance_log is not None]) / len(registration_data)) * 100
        program_status = self.session.query(ProgramStatus).filter_by(program_id=program_id).first()
        program_status.completion_rate = completion_rate
        self.session.commit()
        audit_log = AuditLog(table_name='program_status', record_id=program_id, action_type='UPDATE', action_timestamp=datetime.datetime.now(), new_values={'completion_rate': completion_rate})
        self.session.add(audit_log)
        self.session.commit()