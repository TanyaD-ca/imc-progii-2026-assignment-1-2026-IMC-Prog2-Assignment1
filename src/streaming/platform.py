"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""

from datetime import datetime, timedelta

from .tracks import Track, Song
from .users import User, PremiumUser, FamilyMember
from .artists import Artist
from .albums import Album
from .playlists import Playlist, CollaborativePlaylist
from .sessions import ListeningSession
class StreamingPlatform:
    def __init__(self) -> None :
        self._tracks: dict[str, Track] = {}
        self._users: dict[str, User] = {}
        self._artists: dict[str, Artist] = {}
        self._albums: dict[str, Album] = {}
        self._playlists: dict[str, Playlist] = {}
        self._sessions: list[ListeningSession] = []

    def add_track(self, track: Track) -> None:
        self._tracks[track.track_id] = track

    def add_user(self, user: User) -> None:
        self._users[user.user_id] = user

    def add_artist(self, artist: Artist) -> None:
        self._artists[artist.artist_id] = artist

    def add_album(self, album: Album) -> None:
        self._albums[album.album_id] = album

    def add_playlist(self, playlist: Playlist) -> None:
        self._playlists[playlist.id] = playlist

    def record_session(self, session: ListeningSession):
        self._sessions.append(session)


    def get_track(self, id: str):
        return self._tracks.get(id)

    def get_user(self, id: str):
        return self._users.get(id)

    def get_artist(self, id: str):
        return self._artists.get(id)

    def get_album(self, id: str):
        return self._albums.get(id)


    def all_users(self) -> list[User]:
        return list(self._users.values())

    def all_tracks(self) -> list[Track]:
        return list(self._tracks.values())


    #  Q1: Total Cumulative Listening Time
    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        total = 0
        for session in self._sessions:
            if start <= session.timestamp <= end:
                total += session.duration_seconds
        minutes = total / 60
        return minutes

    # Q2: Average Unique Tracks per Premium User
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        our_date = datetime.now() - timedelta(days=days)
        users = []
        for user in self._users.values():
            if isinstance(user, PremiumUser):
                users.append(user)
        if len(users) ==0:
            return 0.0
        counts =[]
        for user in users:
            tracks = set()
            for session in self._sessions:
                if session.user == user and session.timestamp >= our_date:
                    tracks.add(session.track.id)
            counts.append(len(tracks))
        total = 0
        for i in counts:
            total  = total + i
        return total / len(counts)

    # Q3: Track with Most Distinct Listeners
    def track_with_most_distinct_listeners(self) -> Track | None :
        listeners = {}
        for i in self._sessions:
            if i.track not in listeners:
                listeners[i.track] = set()
            listeners[i.track].add(i.user)
        if len(listeners) == 0:
            return None
        best_track = None
        max_count = 0
        for track in listeners:
            count = len(listeners[track])
            if count > max_count:
                max_count = count
                best_track = track
        return best_track

    # Q4: Average Session Duration  by User Type
    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        data = {}
        for i in self._sessions:
            user_type = type(i.user).__name__
            if user_type not in data:
                data[user_type] = []
            data[user_type].append(i.duration_seconds)
        result = []
        for user_type in data:
            durations = data[user_type]
            average = sum(durations) / len(durations)
            result.append((user_type, average))
        result.sort(key=lambda x: x[1], reverse = True) # the list is sorted by the second value in each tuple, in descending order
        return result

    # Q5: Total Listening Time for Underage Sub - Users
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        total = 0
        for session in self._sessions:
            if isinstance(session.user, FamilyMember):
                if session.user.age < age_threshold:
                    total = total + session.duration_seconds
        return total / 60

    # Q6: Top Artists by Listening Time
    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
        data = {}
        for session in self._sessions:
            if isinstance(session.track, Song):
                artist = session.track.artist
                if artist not in data:
                    data[artist] = 0
                data[artist] = data[artist] + session.duration_seconds
        result = []
        for artist in data:
            minutes = data[artist] / 60
            result.append((artist, minutes))
        result.sort(key=lambda x: x[1], reverse = True)
        return result[:n]

    # Q7: User's Top Genre
    def user_top_genre(self, user_id: str) -> tuple[str, float] | None:
        user = self._users.get(user_id)
        if not user:
            return None
        data = {}
        total = 0
        for session in self._sessions:
            if session.user == user:
                genre = session.track.genre
                if genre not in data:
                    data[genre] = 0
                data[genre] = data[genre] + session.duration_seconds
                total = total + session.duration_seconds
        if total == 0:
            return None
        top_genre = None
        top_duration = 0
        for genre in data:
            if data[genre] > top_duration:
                top_duration = data[genre]
                top_genre = genre
        percentage = (top_duration / total) * 100
        return top_genre, percentage

    # Q8: Collaborative Playlists with Many Artists
    def collaborative_playlists_with_many_artists(self, threshold: int = 3) -> list[CollaborativePlaylist]:
        result = []
        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                artists = set()
                for track in playlist.tracks:
                    if isinstance(track, Song):
                        artists.add(track.artist)
                if len(artists) >= threshold:
                    result.append(playlist)
        return result

    # Q9: Average Tracks per Playlist Type
    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
         normal = []
         collab = []
         for playlist in self._playlists.values():
             if isinstance(playlist, CollaborativePlaylist):
                 collab.append(len(playlist.tracks))
             else:
                 normal.append(len(playlist.tracks))
         if len(normal) > 0:
             avg_normal = sum(normal) / len(normal)
         else:
             avg_normal = 0.0
         if len(collab) > 0:
             avg_collab = sum(collab) / len(collab)
         else:
             avg_collab = 0.0
         return {"Playlist": avg_normal, "CollaborativePlaylist": avg_collab}

    # Q10: Users Who Completed Albums
    def users_who_completed_albums(self) -> list[tuple[User, list[str]]]:
         result = []
         for user in self._users.values():
             listened = []
             for session in self._sessions:
                 if session.user == user:
                     if session.track not in listened:
                         listened.append(session.track)
             completed = []
             for album in self._albums.values():
                 if len(album.tracks) == 0:
                     continue
                 all_listened = True
                 for track in album.tracks:
                     if track not in listened:
                         all_listened = False
                         break
                 if all_listened:
                     completed.append(album.title)
             if len(completed) > 0:
                 result.append((user, completed))
         return result
