from app.model.spotify.track import RecentlyPlayedTrack
from app.controller.spotify_controller import SpotifyController
from fastapi import APIRouter
router = APIRouter()


@router.get("/", response_model=list[RecentlyPlayedTrack])
async def current_user_recently_played() -> list[RecentlyPlayedTrack]:
    """ 最近聴いている曲の一覧を取得 """
    spotify_controller = SpotifyController.get_instance()
    result = spotify_controller.current_user_recently_played()
    return result
