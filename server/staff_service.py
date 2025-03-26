

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///staff.db')
Base = declarative_base()

class Staff(Base):
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True)
    status = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class StaffService:
    def update_staff_status(self, staff_id, new_status):
        if staff_id is None or staff_id == "":
            return "Error: Staff ID is required"
        if new_status is None or new_status == "":
            return "Error: New status is required"
        staff_member = session.query(Staff).filter_by(id=staff_id).first()
        if staff_member is None:
            return "Error: Staff member not found"
        staff_member.status = new_status
        session.commit()
        return "Staff status updated successfully"