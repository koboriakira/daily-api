from app.router.notion.model.page_base_model import PageBaseModel
from pydantic import BaseModel, Field
from fastapi import APIRouter
from typing import Optional
from app.interface.notion_client import NotionClient
from datetime import date as DateObject
from datetime import datetime as DatetimeObject
from app.model.tag import Tags

router = APIRouter()


class Book(PageBaseModel):
    status: Optional[str] = Field(default=None, title="ステータス")


@ router.get("/", response_model=list[Book])
async def get_books():
    """ 音楽を取得 """
    entities = NotionClient().retrieve_books()
    print(entities)
    return convert_to_model(entities)


def convert_to_model(entites: list[dict]) -> list[Book]:
    return [Book(**entity) for entity in entites]
