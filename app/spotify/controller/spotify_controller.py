from app.spotify.interface.spotipy import Spotipy
from app.spotify.controller.track_response_translator import TrackResponseTranslator
from app.spotify.controller.track_response import TrackResponse
from typing import Optional
from app.util.get_logger import get_logger

logger = get_logger(__name__)


class SpotifyController:
    def __init__(self):
        self.sp = Spotipy.get_instance()

    def get_track(self, track_id: str) -> Optional[TrackResponse]:
        track = self.sp.get_track(track_id=track_id)
        if track is None:
            return None
        return TrackResponseTranslator.to_entity(track)

    def get_playing(self) -> Optional[TrackResponse]:
        track = self.sp.get_playing()
        if track is None:
            return None
        return TrackResponseTranslator.to_entity(track)
