"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.

Classes to implement:
  - Track (abstract base class)
    - Song
      - SingleRelease
      - AlbumTrack
    - Podcast
      - InterviewEpisode
      - NarrativeEpisode
    - AudiobookTrack
"""

from abc import ABC
from datetime import date
from .albums import Album
from .artists import Artist

class Track(ABC):
    def __init__(self, id: str, title: str, duration_seconds: int, genre: str) -> None :
        self.track_id: str = id
        self.title: str = title
        self.duration_seconds: int = duration_seconds
        self.genre: str = genre

    def duration_minutes(self) -> float:
        return self.duration_seconds / 60
    # if the tracks have the same id
    def __eq__(self, other) -> bool:
        if not isinstance(other, Track):
            return False
        return self.track_id == other.track_id

class Song(Track):
    def __init__(self, id: str, title: str, duration_seconds: int, genre: str, artist: Artist) -> None :
        super().__init__(id, title, duration_seconds, genre)
        self.artist: Artist = artist

class SingleRelease(Song):
    def __init__(self, id: str, title: str, duration_seconds: int, genre: str, artist: Artist, release_date: date) -> None :
        super().__init__(id, title, duration_seconds, genre, artist)
        self.release_date: date = release_date

class AlbumTrack(Song):
    def __init__( self, id: str, title: str, duration_seconds: int, genre: str, artist: Artist, track_number: int, album: "Album" = None ) -> None:
        super().__init__(id, title, duration_seconds, genre, artist)
        self.track_number: int = track_number
        self.track_id: str = id
        self.album: Album | None = album

class Podcast(Track):
    def __init__(self, id: str, title: str, duration_seconds: int, genre: str, host: str, description: str = "") -> None :
        super().__init__(id, title, duration_seconds, genre)
        self.host: str = host
        self.description: str = description

class InterviewEpisode(Podcast):
    def __init__(self, id: str, title: str, duration_seconds: int, genre: str, host: str, guest: str = "") -> None :
        super().__init__(id, title, duration_seconds, genre, host)
        self.guest: str = guest

class NarrativeEpisode(Podcast):
    def __init__(self, id: str, title: str, duration_seconds: int, genre: str, host: str, season: int = 1, episode_number: int = 1) -> None :
        super().__init__(id, title, duration_seconds, genre, host)
        self.season: int = season
        self.episode_number: int = episode_number

class AudiobookTrack(Track):
    def __init__(self, id: str, title: str, duration_seconds: int, genre: str, author: str, narrator: str) -> None :
        super().__init__(id, title, duration_seconds, genre)
        self.author: str = author
        self.narrator: str = narrator