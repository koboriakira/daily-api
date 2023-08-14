from pydantic import BaseModel, Field
from app.domain.spotify.track import Track as TrackModel


class Track(BaseModel):
    id: str = Field(description="Spotify ID of the track")
    name: str = Field(description="Name of the track")
    artist: str = Field(description="Name of the artist")
    spotify_url: str = Field(description="Spotify URL of the track")

    def __hash__(self):
        return hash((self.id, self.spotify_url))


class TrackEntityConverter:
    @staticmethod
    def convertToEntity(model: TrackModel) -> Track:
        return Track(
            id=model.id,
            name=model.name,
            artist=model.artists[0]["name"],
            spotify_url=model.spotify_url,
        )
