

import logging
from server.models.program import Program
from server.models.registration import Registration
from server.services.email_service import EmailService
from server.services.program_service import ProgramService

class ProgramController:
    def get_program_status(self, program_id):
        program = Program.query.get(program_id)
        return program.status

    def calculate_completion_statistics(self, program_id):
        program = Program.query.get(program_id)
        completion_statistics = ProgramService.calculate_completion_statistics(program)
        return completion_statistics

    def generate_attendance_notifications(self, program_id):
        program = Program.query.get(program_id)
        attendance_notifications = ProgramService.generate_attendance_notifications(program)
        EmailService.send_attendance_notifications(attendance_notifications)

    def create_waitlist_notification_batch(self, program_id):
        program = Program.query.get(program_id)
        waitlist_notifications = ProgramService.create_waitlist_notification_batch(program)
        EmailService.send_waitlist_notifications(waitlist_notifications(waitlist_notifications)

    def start_program(self, program_id):
        program = Program.query.get(program_id)
        if program.status != 'PUBLISHED':
            raise Exception('Program is not in PUBLISHED status')
        if len(Registration.query.filter_by(program_id=program_id, paid=True).all()) < program.min_participants:
            self.create_waitlist_notification_batch(program_id)
            program.status = 'CANCELLED'
            program.save()
            raise Exception('Insufficient registrations')
        ProgramService.initialize_session_schedule(program)
        program.status = 'IN_PROGRESS'
        program.save()

    def record_attendance(self, program_id):
        program = Program.query.get(program_id)
        if program.status != 'IN_PROGRESS':
            raise Exception('Program is not in IN_PROGRESS status')
        ProgramService.create_temporary_table_for_attendance_data(program)
        ProgramService.update_attendance_logs(program)
        self.generate_attendance_notifications(program_id)

    def complete_program(self, program_id):
        program = Program.query.get(program_id)
        if program.status != 'IN_PROGRESS':
            raise Exception('Program is not in IN_PROGRESS status')
        self.calculate_completion_statistics(program_id)
        ProgramService.update_completion_status(program)
        program.status = 'COMPLETED'
        program.save()

    def log_program_state_change(self, program_id, action, params):
        logging.info(f'Program {program_id} state changed: {action} with params {params}')