from unittest import TestCase
import json
from app.model.spotify.track import RecentlyPlayedTrack


class RecentlyPlayedTrackTest(TestCase):
    def test_重複を削除(self):
        # 重複したデータを含むリスト
        duplicated_tracks = self._get_duplicated_tracks()

        unique_tracks = list(set(duplicated_tracks))

        assert len(unique_tracks) == 3

    def _get_duplicated_tracks(self) -> list[RecentlyPlayedTrack]:
        data = [
            {
                "id": "0aLkYYO8w7T0U2Vhb0pe2O",
                "name": "Sara Sara",
                "artist": "SEVENTEEN",
                "spotify_url": "https://open.spotify.com/track/0aLkYYO8w7T0U2Vhb0pe2O",
                "played_at": "2023-08-18T12:01:45.691Z"
            },
            {
                "id": "0aLkYYO8w7T0U2Vhb0pe2O",
                "name": "Sara Sara",
                "artist": "SEVENTEEN",
                "spotify_url": "https://open.spotify.com/track/0aLkYYO8w7T0U2Vhb0pe2O",
                "played_at": "2023-08-18T11:47:38.855Z"
            },
            {
                "id": "3VT1ZDr8PSITQfYbBGtaVk",
                "name": "NOT FOUND",
                "artist": "Mr.Children",
                "spotify_url": "https://open.spotify.com/track/3VT1ZDr8PSITQfYbBGtaVk",
                "played_at": "2023-08-19T06:55:25.065Z"
            },
            {
                "id": "3VT1ZDr8PSITQfYbBGtaVk",
                "name": "NOT FOUND",
                "artist": "Mr.Children",
                "spotify_url": "https://open.spotify.com/track/3VT1ZDr8PSITQfYbBGtaVk",
                "played_at": "2023-08-19T06:50:28.168Z"
            },
            {
                "id": "3VT1ZDr8PSITQfYbBGtaVk",
                "name": "NOT FOUND",
                "artist": "Mr.Children",
                "spotify_url": "https://open.spotify.com/track/3VT1ZDr8PSITQfYbBGtaVk",
                "played_at": "2023-08-19T06:45:32.120Z"
            },
            {
                "id": "3VT1ZDr8PSITQfYbBGtaVk",
                "name": "NOT FOUND",
                "artist": "Mr.Children",
                "spotify_url": "https://open.spotify.com/track/3VT1ZDr8PSITQfYbBGtaVk",
                "played_at": "2023-08-19T06:40:36.066Z"
            },
            {
                "id": "1GIsaJcD5PEc2EOLH3ePpy",
                "name": "スタート",
                "artist": "CAPSULE",
                "spotify_url": "https://open.spotify.com/track/1GIsaJcD5PEc2EOLH3ePpy",
                "played_at": "2023-08-18T11:02:34.673Z"
            },
        ]
        return [RecentlyPlayedTrack(**d) for d in data]
