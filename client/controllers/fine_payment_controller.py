

from client.services.fine_service import FineService

class FinePaymentController:
    def process_fine_payment(self, fine_id, amount_paid):
        fine_service = FineService()
        return fine_service.process_fine_payment(fine_id, amount_paid)