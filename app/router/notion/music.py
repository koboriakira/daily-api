from app.router.notion.model.page_base_model import PageBaseModel
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException
from typing import Optional
from app.interface.notion_client import NotionClient
from app.spotify.controller.spotify_controller import SpotifyController
from datetime import date as DateObject
from datetime import datetime as DatetimeObject
from app.model import NotionUrl
from app.util.get_logger import get_logger


logger = get_logger(__name__)
router = APIRouter()


class Music(PageBaseModel):
    artist: str = Field(..., title="アーティスト")
    spotify_url: str = Field(..., title="SpotifyのURL",
                             regex=r"^https://open.spotify.com/.*")


@ router.get("/registered/{date}")
async def get_registerd(date: DateObject):
    """ 登録した音楽を取得 """
    entities = NotionClient().retrieve_musics()
    entities = list(
        filter(lambda entity: entity["created_at"].date() == date, entities))
    return convert_to_model(entities)


@ router.get("/", response_model=list[Music])
async def get_music():
    """ 音楽を取得 """
    music_entities = NotionClient().retrieve_musics()
    return convert_to_model(music_entities)


class PostMusicRequest(BaseModel):
    name: str = Field(..., title="曲名")
    artists: list[str] = Field(..., title="アーティスト名")
    spotify_url: str = Field(..., title="SpotifyのURL",
                             regex=r"^https://open.spotify.com/.*")
    cover_url: str = Field(..., title="カバー画像のURL",
                           regex=r"^https://i.scdn.co/image/.*")
    release_date: Optional[DateObject] = Field(..., title="リリース日")


@ router.post("/", response_model=dict)
async def post_music(request: PostMusicRequest):
    """ 音楽を記録 """
    notion_client = NotionClient()

    daily_log_id = notion_client.get_daily_log_id(date=DateObject.today())
    result = notion_client.add_track(name=request.name,
                                     artists=request.artists,
                                     spotify_url=request.spotify_url,
                                     cover_url=request.cover_url,
                                     release_date=request.release_date,
                                     daily_log_id=daily_log_id)
    return {
        "page_id": result["id"],
        "url": result["url"]
    }

@ router.post("/spotify/{spotify_track_id}", response_model=dict)
async def post_music_by_spotify_track(spotify_track_id: str):
    """ SpotifyのトラックIDをもとに音楽を記録 """
    logger.info("post_music_by_spotify_track")
    logger.info(spotify_track_id)
    spotify_controller = SpotifyController()
    notion_client = NotionClient()

    spotify_controller = SpotifyController()
    track = spotify_controller.get_track(track_id=spotify_track_id)
    if track is None:
        return HTTPException(status_code=404, detail="Track not found")

    result = notion_client.add_track(name=track.name,
                                     artists=track.artists,
                                     spotify_url=track.spotify_url,
                                     cover_url=track.cover_url,
                                     release_date=DateObject.fromisoformat(track.release_date) if track.release_date is not None else None,
                                     )
    return {
        "page_id": result["id"],
        "url": result["url"]
    }


def convert_to_model(entities: list[dict]) -> list[Music]:
    return [Music(**entity) for entity in entities]
