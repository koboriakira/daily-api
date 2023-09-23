from app.domain.spotify.track import Track
from app.spotify.controller.track_response import TrackResponse


class TrackResponseTranslator:
    @staticmethod
    def to_entity(track: Track) -> TrackResponse:
        return TrackResponse(
            id=track.id,
            name=track.name,
            artists=[artist["name"] for artist in track.artists],
            spotify_url=track.spotify_url,
            cover_url=track.album["images"][0]["url"],
            release_date=track.album["release_date"]
        )
