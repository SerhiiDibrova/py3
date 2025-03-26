

from datetime import date
from models.patron import Patron
from db import db

class PatronService:
    def create_patron(self, first_name, last_name, email, phone, birth_date):
        if not first_name or not last_name or not email or not phone or not birth_date:
            raise ValueError('Invalid input parameters')
        patron = Patron(first_name, last_name, email, phone, birth_date, date.today(), 'ACTIVE')
        db.session.add(patron)
        db.session.commit()
        return 'Patron created successfully'