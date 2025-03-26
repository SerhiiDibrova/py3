

from PyQt5.QtCore import QDateTime
from datetime import date
from client.base_model import BaseModel
from client.qml_property import QmlProperty

class EventRegistration(BaseModel):
    event_id: int = QmlProperty(int)
    patron_id: int = QmlProperty(int)
    registration_date: date = QmlProperty(QDateTime)
    attendance_status: str = QmlProperty(str)

    def __repr__(self):
        return f"EventRegistration(event_id={self.event_id}, patron_id={self.patron_id}, registration_date={self.registration_date}, attendance_status={self.attendance_status})"