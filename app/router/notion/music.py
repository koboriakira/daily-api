from app.router.notion.page_base_model import PageBaseModel
from pydantic import BaseModel, Field
from fastapi import APIRouter
from typing import Optional
from app.interface.notion_client import NotionClient
from datetime import date as DateObject
from datetime import datetime as DatetimeObject
from app.model import NotionUrl


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


def convert_to_model(entities: list[dict]) -> list[Music]:
    return [Music(**entity) for entity in entities]
