from fastapi import APIRouter, HTTPException
from typing import Optional
from app.spotify.controller.spotify_controller import SpotifyController
from app.spotify.controller.track_response import TrackResponse
from spotipy.exceptions import SpotifyException
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
async def get_current_playing():
    """
    現在流れている曲を取得する
    """
    try:
        new_spotify_controller = SpotifyController()
    except SpotifyException as e:
        print(e)
        if "access token expired" in str(e):
            return HTTPException(status_code=401, detail="Spotifyのアクセストークンが有効切れです。")
        return HTTPException(status_code=401, detail="不明なエラーです。")
    except FileNotFoundError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Spotifyの認証が必要です。")
    return new_spotify_controller.get_playing()
