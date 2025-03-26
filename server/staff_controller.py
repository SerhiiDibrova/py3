

from server.staff_service import StaffService

class StaffController:
    def update_staff_status(self, staff_id, new_status):
        staff_service = StaffService()
        return staff_service.update_staff_status(staff_id, new_status)