"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""

from .tracks import Track

class Artist:
    def __init__(self, id: str, name: str, genre: str) -> None:
        self.artist_id: str = id
        self.name:str = name
        self.genre = genre
        self.tracks: list["Track"] = []
    def __repr__(self): # returns an “official” str repr. of the object
        return f"Artist(id={self.artist_id}, name={self.name}, genre={self.genre})"

    def add_track(self, track: "Track") -> None:
        if track not in self.tracks:
            self.tracks.append(track)
    def track_count(self) -> int:
        return len(self.tracks)
