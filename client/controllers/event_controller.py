

from PyQt5.QtCore import QObject, QDateTime
from client.models import EventRegistration, LibraryEvent

class EventController(QObject):
    def register_for_event(self, event_id, patron_id):
        event_registration = EventRegistration(event_id=event_id, patron_id=patron_id, registration_date=QDateTime.currentDateTime(), attendance_status='REGISTERED')
        library_event = LibraryEvent(event_id=event_id)
        library_event.current_participants += 1