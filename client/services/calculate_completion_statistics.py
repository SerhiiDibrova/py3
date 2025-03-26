

from datetime import datetime
from client.models import Program, Registration, ProgramStatus, AuditLog

def calculate_completion_statistics(program_id: int):
    program = Program.get(program_id)
    registrations = Registration.filter(program_id=program_id)
    completions = [registration for registration in registrations if registration.is_completed]
    completion_rate = (len(completions) / len(registrations)) * 100 if registrations else 0
    program_status = ProgramStatus.get(program_id)
    program_status.completion_rate = completion_rate
    program_status.save()
    audit_log = AuditLog.create(table_name='program_status', record_id=program_id, action_type='UPDATE', action_timestamp=datetime.now(), new_values={'completion_rate': completion_rate})