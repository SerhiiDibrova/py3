

package server.controllers

import logging
import notification_service
import patron_service
import registration_service

class PatronController:
    def manage_patron_account(self, patron_id, action, params):
        patron_summary = patron_service.get_patron_summary(patron_id)
        if action == 'SUSPEND':
            if patron_summary.status == 'SUSPENDED':
                raise Exception('Account is already suspended')
            active_loans = patron_service.get_active_loans(patron_id)
            if active_loans:
                raise Exception('Account has active loans')
            if patron_summary.unpaid_fines > 0:
                raise Exception('Account has unpaid fines')
            if patron_summary.overdue_items > 0:
                raise Exception('Account has overdue items')
            patron_service.update_patron_status(patron_id, 'SUSPENDED')
            registration_service.cancel_active_registrations(patron_id)
            notification_text = notification_service.generate_notification(patron_summary, params)
            logging.log_suspension(patron_id, patron_summary, notification_text, params)
        elif action == 'REACTIVATE':
            if patron_summary.status != 'SUSPENDED':
                raise Exception('Account is not suspended')
            patron_service.update_patron_status(patron_id, 'ACTIVE')
        elif action == 'AUDIT':
            logging.log_audit(patron_id, patron_summary, params)
        else:
            raise Exception('Invalid action')