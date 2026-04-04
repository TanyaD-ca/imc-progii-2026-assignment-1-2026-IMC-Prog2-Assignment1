"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""

from .artists import Artist
from .tracks import AlbumTrack

class Album:

    def __init__(self, id: str, title: str, artist: Artist, release_year: int) -> None :
        self.album_id: str = id
        self.title: str = title
        self.artist: Artist = artist
        self.release_year: int = release_year
        self.tracks: list["AlbumTrack"] = []

    def add_track(self, track: "AlbumTrack") -> None :
        if track not in self.tracks:
            self.tracks.append(track)
            track.album = self
            self.tracks.sort(key = lambda x: x.track_number)

    def track_ids(self) -> set[str]:
        return set(i.track_id for i in self.tracks)
    def duration_seconds(self) -> int:
        return sum(i.duration_seconds for i in self.tracks)


