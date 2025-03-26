

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models import Staff

class StaffRepository:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_staff_member_by_id(self, staff_id):
        return self.session.query(Staff).filter(Staff.id == staff_id).first()

    def commit_changes_to_database(self):
        self.session.commit()