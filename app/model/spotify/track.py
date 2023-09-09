from pydantic import BaseModel, Field
from app.domain.spotify.item import Item
from app.domain.spotify.track import Track as TrackModel


class Track(BaseModel):
    id: str = Field(description="Spotify ID of the track")
    name: str = Field(description="Name of the track")
    artist: list[str] = Field(description="Name of the artist")
    spotify_url: str = Field(description="Spotify URL of the track")
    cover_url: str = Field(description="Cover URL of the track")

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, __value: 'RecentlyPlayedTrack') -> bool:
        return self.id == __value.id


class RecentlyPlayedTrack(Track):
    played_at: str = Field(description="When the track was played")


class TrackConverter:
    @staticmethod
    def from_track_model(track: TrackModel) -> Track:
        return Track(
            id=track.id,
            name=track.name,
            artist=[artist["name"] for artist in track.artists],
            spotify_url=track.spotify_url,
            cover_url=track.album["images"][0]["url"]
        )


class RecentlyPlayedTrackConverter:
    @staticmethod
    def from_item(item: Item) -> RecentlyPlayedTrack:
        return RecentlyPlayedTrack(
            id=item.track.id,
            name=item.track.name,
            artist=[artist["name"] for artist in item.track.artists],
            spotify_url=item.track.spotify_url,
            cover_url=item.track.album["images"][0]["url"],
            played_at=item.played_at
        )
