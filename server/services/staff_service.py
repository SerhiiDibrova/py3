

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.staff import Staff

class StaffService:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def update_staff_status(self, staff_id, new_status):
        session = self.Session()
        staff = session.query(Staff).filter_by(staff_id=staff_id).first()
        if staff:
            staff.status = new_status
            session.commit()
        else:
            raise ValueError('Staff not found')