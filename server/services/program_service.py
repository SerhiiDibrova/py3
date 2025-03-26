

from flask import current_app
from server import db
from server.models.program import Program
from server.models.registration import Registration
from server.services.attendance_service import AttendanceService
from server.services.email_service import EmailService
from server.services.session_service import SessionService
from server.services.statistics_service import StatisticsService
from server.services.waitlist_service import WaitlistService

class ProgramService:
    def get_program_status(self, program_id):
        program_data = Program.query.get(program_id)
        if program_data.status not in ['PUBLISHED', 'IN_PROGRESS', 'COMPLETED']:
            raise Exception('Invalid program status')
        return program_data.status

    def validate_program_status(self, program_id):
        program_data = Program.query.get(program_id)
        if program_data.status not in ['PUBLISHED', 'IN_PROGRESS', 'COMPLETED']:
            raise Exception('Invalid program status')

    def retrieve_registration_status(self, program_id):
        registration_data = Registration.query.get(program_id)
        return registration_data.status

    def calculate_completion_statistics(self, program_id):
        statistics_service = StatisticsService()
        return statistics_service.calculate_completion_statistics(program_id)

    def generate_attendance_notifications(self, program_id):
        attendance_service = AttendanceService()
        return attendance_service.generate_attendance_notifications(program_id)

    def create_waitlist_notification_batch(self, program_id):
        waitlist_service = WaitlistService()
        return waitlist_service.create_waitlist_notification_batch(program_id)

    def start_program(self, program_id):
        program_data = Program.query.get(program_id)
        if program_data.status != 'PUBLISHED':
            raise Exception('Program is not in PUBLISHED status')
        if program_data.paid_registrations < program_data.min_required_registrations:
            waitlist_service = WaitlistService()
            waitlist_service.create_waitlist_notification_batch(program_id)
            program_data.status = 'CANCELLED'
            db.session.commit()
            return
        session_service = SessionService()
        session_service.initialize_session_schedule(program_id)
        program_data.status = 'IN_PROGRESS'
        db.session.commit()

    def record_attendance(self, program_id):
        program_data = Program.query.get(program_id)
        if program_data.status != 'IN_PROGRESS':
            raise Exception('Program is not in IN_PROGRESS status')
        attendance_service = AttendanceService()
        attendance_service.create_temporary_attendance_table(program_id)
        attendance_service.update_attendance_logs(program_id)
        attendance_service.generate_attendance_notifications(program_id)

    def complete_program(self, program_id):
        program_data = Program.query.get(program_id)
        if program_data.status != 'IN_PROGRESS':
            raise Exception('Program is not in IN_PROGRESS status')
        statistics_service = StatisticsService()
        statistics_service.calculate_completion_statistics(program_id)
        program_data.status = 'COMPLETED'
        db.session.commit()