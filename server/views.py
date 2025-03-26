

from django.shortcuts import render
from .models import Program, Registration, Patron, AttendanceRecord
from .utils import generate_notification

def generate_attendance_notifications(request, program_id):
    try:
        program_data = Program.objects.get(program_id=program_id)
        attendance_data = AttendanceRecord.objects.filter(registration_id=program_id)
        for attendance_record in attendance_data:
            notification = generate_notification(attendance_record.attendance_status)
            attendance_record.attendance_log = notification
            attendance_record.save()
    except Program.DoesNotExist:
        print(f"Program with id {program_id} does not exist")
    except Exception as e:
        print(f"An error occurred: {str(e)}")