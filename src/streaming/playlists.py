"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""

from .tracks import Track
from .users import User

class Playlist:
    def __init__(self, id: str, title: str, owner: User) -> None :
        self.id: str = id
        self.title: str = title
        self.owner: User = owner
        self.tracks: list[Track] = []

    def add_track(self, track: Track) -> None :
        if track not in self.tracks:
            self.tracks.append(track)
    def remove_track(self, track_id: str) -> None:
        new_tracks = []
        for i in self.tracks:
            t_id = i.id if hasattr(i, "id") else i.track_id
            if t_id != track_id:
                new_tracks.append(i)
        self.tracks = new_tracks


class CollaborativePlaylist(Playlist):
    def __init__(self, id: str, title: str, owner: User) -> None :
        super().__init__(id, title, owner)
        self.contributors: list[User] = [owner]

    def add_contributor(self, user: User) -> None :
        if user not in self.contributors:
            self.contributors.append(user)
    def remove_contributor(self, user: User) -> None:
        if user != self.owner and user in self.contributors:
            self.contributors.remove(user)