

package server.utils

def generate_notification(attendance_status):
    if attendance_status == 'PRESENT':
        return 'Attendance confirmed'
    elif attendance_status == 'ABSENT':
        return 'Attendance not confirmed'