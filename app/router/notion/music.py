from pydantic import BaseModel, Field
from fastapi import APIRouter
from typing import Optional
from app.interface.notion_client import NotionClient
from datetime import date as DateObject


router = APIRouter()


class Task(BaseModel):
    id: str = Field(..., title="タスクのID")
    title: str = Field(..., title="タスクのタイトル")
    status: str = Field(..., title="タスクのステータス")
    date: Optional[str] = Field(..., title="タスクの実施予定日",
                                regex=r"^\d{4}-\d{2}-\d{2}$")


class Project(BaseModel):
    id: str = Field(..., title="プロジェクトのID")
    title: str = Field(..., title="プロジェクトのタイトル")
    url: str = Field(..., title="プロジェクトのURL",
                     regex=r"^https://www.notion.so/.*")
    status: str = Field(..., title="プロジェクトのステータス")
    tasks: list[Task] = Field(..., title="プロジェクトのタスク")


@router.get("/registerd")
async def get_registerd(date: Optional[DateObject] = None, embed_url: bool = False):
    """ 登録した音楽を取得 """
    notion_client = NotionClient()

    musics = notion_client.find_musics(date=date)

    if embed_url:
        for music in musics:
            track_id = music["spotify_url"].split("/")[-1]
            music["embed_url"] = f"""<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/{track_id}?utm_source=generator" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>"""

    return musics
