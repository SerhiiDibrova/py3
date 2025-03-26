

from PyQt5.QtCore import QObject, pyqtProperty
from dataclasses import dataclass

@dataclass
class LibraryEvent(QObject):
    event_id: int
    max_participants: int
    current_participants: int

    def __repr__(self):
        return f"LibraryEvent(event_id={self.event_id}, max_participants={self.max_participants}, current_participants={self.current_participants})"

    @pyqtProperty(int)
    def event_id(self):
        return self._event_id

    @event_id.setter
    def event_id(self, value):
        self._event_id = value

    @pyqtProperty(int)
    def current_participants(self):
        return self._current_participants

    @current_participants.setter
    def current_participants(self, value):
        self._current_participants = value