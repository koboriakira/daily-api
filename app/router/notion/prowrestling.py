from app.router.notion.page_base_model import PageBaseModel
from pydantic import BaseModel, Field
from fastapi import APIRouter
from typing import Optional
from app.interface.notion_client import NotionClient
from datetime import date as DateObject
from datetime import datetime as DatetimeObject
from app.model.tag import Tags

router = APIRouter()


# class Prowrestling(PageBaseModel):
#     tags: list[Tags] = Field(..., title="タグのリスト")


@ router.get("/")
async def get_prowrestling():
    """ 音楽を取得 """
    entities = NotionClient().retrieve_prowrestlings()
    print(entities)
    return convert_to_model(entities)


def convert_to_model(entites: list[dict]) -> list[PageBaseModel]:
    return [PageBaseModel(**entity) for entity in entites]
