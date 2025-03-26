

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StaffRepository:
    def update_staff_status(self, staff_id, new_status):
        if not staff_id or not new_status:
            return 'Error: Staff ID and new status are required'

        staff_member = self.get_staff_member_by_id(staff_id)
        if not staff_member:
            return 'Error: Staff member not found'

        staff_member.status = new_status
        db.session.commit()
        return 'Staff status updated successfully'

    def get_staff_member_by_id(self, staff_id):
        return Staff.query.filter_by(id=staff_id).first()

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), nullable=False)