from fastapi import APIRouter
from typing import Optional
from app.spotify.controller.spotify_controller import SpotifyController
from app.spotify.controller.track_response import TrackResponse

router = APIRouter()


@router.get("/{track_id}", response_model=Optional[TrackResponse])
async def get_track(track_id: str):
    """
    指定されたSpotifyの曲の情報を取得する。
    """
    new_spotify_controller = SpotifyController()
    return new_spotify_controller.get_track(track_id=track_id)


# @router.get("/recommend/{track_id}", response_model=TrackEntity)
# async def recommend(track_id: str):
#     """
#     指定されたSpotifyの曲をもとに、レコメンドをする
#     """
#     spotify_controller = SpotifyController.get_instance()
#     return spotify_controller.recommend(track_id=track_id)


@router.get("/current/playing", response_model=Optional[TrackResponse])
async def get_playing():
    """
    現在流れている曲を取得する
    """
    new_spotify_controller = SpotifyController()
    return new_spotify_controller.get_playing()
