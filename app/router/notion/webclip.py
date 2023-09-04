from app.router.notion.page_base_model import PageBaseModel
from pydantic import BaseModel, Field
from fastapi import APIRouter
from typing import Optional
from app.interface.notion_client import NotionClient
from datetime import date as DateObject
from datetime import datetime as DatetimeObject
from app.model import NotionUrl


router = APIRouter()


class WebClip(PageBaseModel):
    clipped_url: str = Field(...,
                             title="記事のURL",
                             regex=r"^https?://.*")
    status: str = Field(...,
                        title="ステータス",
                        regex=r"^(Inbox|Next Action|In progress|In Review|Done|Archived|Need Someday|Trash)$")


@ router.get("/", response_model=list[WebClip])
async def get_music():
    """ 音楽を取得 """
    entities = NotionClient().retrieve_webclips()
    return convert_to_model(entities)


def convert_to_model(entities: list[dict]) -> list[WebClip]:
    return [WebClip(**entity) for entity in entities]
