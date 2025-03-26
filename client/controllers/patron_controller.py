

from client.services import PatronService

class PatronController:
    def create_patron(self, first_name, last_name, email, phone, birth_date):
        patron_service = PatronService()
        return patron_service.create_patron(first_name, last_name, email, phone, birth_date)