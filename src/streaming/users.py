"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""

from datetime import date
from .sessions import ListeningSession

class User:
    def __init__(self, id: str, name: str, age: int) -> None :
        self.user_id: str = id
        self.name = name
        self.age = age
        self.sessions: list["ListeningSession"] = []

    def add_session(self, session: "ListeningSession") -> None:
        self.sessions.append(session)

    def total_listening_seconds(self) -> int:
        return sum(i.duration_listened_seconds for i in self.sessions)

    def total_listening_minutes(self) -> float:
        return self.total_listening_seconds() / 60

    def unique_tracks_listened(self) -> set[str]:
        return {i.track.track_id for i in self.sessions}

class FreeUser(User):
    def __init__(self, id: str, name: str, age: int) -> None :
        super().__init__(id, name, age)

class PremiumUser(User):
    def __init__(self, id: str, name: str, age: int, subscription_start: date) -> None :
        super().__init__(id, name, age)
        self.subscription_start = subscription_start

class FamilyAccountUser(User):
    def __init__(self, id: str, name: str, age: int) -> None :
        super().__init__(id, name, age)
        self.sub_users: list["FamilyMember"] = []

    def add_sub_user(self, member: "FamilyMember") -> None :
        if member not in self.sub_users:
            self.sub_users.append(member)

    def all_members(self) -> list[User]:
        return [self] + self.sub_users

class FamilyMember(User):
    def __init__(self, id: str,  name: str, age: int, parent: FamilyAccountUser) -> None :
        super().__init__(id, name, age)
        self.parent = parent
        parent.add_sub_user(self)

