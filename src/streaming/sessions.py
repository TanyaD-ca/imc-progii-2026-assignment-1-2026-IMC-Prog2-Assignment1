"""
sessions.py
-----------
Implement the ListeningSession class for recording listening events.

Classes to implement:
  - ListeningSession
"""

from datetime import datetime
from .users import User
from .tracks import Track

class ListeningSession:
    def __init__(self, id: str, user: User, track: Track, timestamp: datetime, duration_seconds: int) -> None :
        self.session_id: str = id
        self.user: User = user
        self.track: Track = track
        self.timestamp: datetime = timestamp
        self.duration_listened_seconds: int = duration_seconds
    def duration_listened_minutes(self) -> float:
            return self.duration_listened_seconds / 60