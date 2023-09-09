from app.controller.spotify_controller import SpotifyController
from fastapi import APIRouter
from app.interface.notion_client import NotionClient
from app.model.url import NotionUrl
from app.model.spotify.track import Track as TrackEntity
from app.model.spotify.track import TrackConverter

from typing import Optional
router = APIRouter()


@router.get("/{track_id}", response_model=TrackEntity)
async def get_track(track_id: str):
    """
    指定されたSpotifyの曲の情報を取得する。
    """
    spotify_controller = SpotifyController.get_instance()
    track = spotify_controller.get_track(track_id=track_id)
    return TrackConverter.from_track_model(track=track)


@router.get("/recommend/{track_id}", response_model=TrackEntity)
async def recommend(track_id: str):
    """
    指定されたSpotifyの曲をもとに、レコメンドをする
    """
    spotify_controller = SpotifyController.get_instance()
    return spotify_controller.recommend(track_id=track_id)


@router.get("/current/playing", response_model=Optional[TrackEntity])
async def get_playing():
    """
    現在流れている曲を取得する
    """
    spotify_controller = SpotifyController.get_instance()
    return spotify_controller.get_playing()
