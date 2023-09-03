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
    title: str = Field(..., title="タイトル")
    spotify_url: str = Field(..., title="SpotifyのURL",
                             regex=r"^https://open.spotify.com/.*")


@ router.get("/registered/{date}")
async def get_registerd(date: DateObject):
    """ 登録した音楽を取得 """
    music_entities = NotionClient().retrieve_musics()
    music_entities = list(
        filter(lambda music: music["created_at"].date() == date, music_entities))
    return convert_to_model(music_entities)


@ router.get("/")
async def get_music():
    """ 音楽を取得 """
    music_entities = NotionClient().retrieve_musics()
    return convert_to_model(music_entities)


def convert_to_model(music_entites: list[dict]) -> list[Music]:
    return [Music(**music_entity) for music_entity in music_entites]
