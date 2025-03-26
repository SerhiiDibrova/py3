

from services.patron_service import PatronService

class PatronEndpoint:
    def create_patron(self, first_name, last_name, email, phone, birth_date):
        patron_service = PatronService()
        patron_service.create_patron(first_name, last_name, email, phone, birth_date)