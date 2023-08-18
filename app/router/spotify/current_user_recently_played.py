from app.model.spotify.track import Track
from app.controller.spotify_controller import SpotifyController
from fastapi import APIRouter
from typing import Optional
router = APIRouter()


@router.get("/", response_model=list[Track])
async def current_user_recently_played(after: Optional[float] = None) -> list[Track]:
    """ 最近聴いている曲の一覧を取得 """
    spotify_controller = SpotifyController.get_instance()
    result = spotify_controller.current_user_recently_played(after=after)
    return result
