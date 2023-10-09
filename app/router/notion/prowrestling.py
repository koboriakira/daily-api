from app.router.notion.model.page_base_model import PageBaseModel
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


@ router.get("/", response_model=list[PageBaseModel])
async def get_prowrestling():
    """ プロレス大会情報を取得 """
    entities = NotionClient().retrieve_prowrestlings()
    print(entities)
    return convert_to_model(entities)


class CreateProwrestlingRequest(BaseModel):
    title: str = Field(..., title="タイトル")
    date: DateObject = Field(..., title="日付")
    url: Optional[str] = Field(None, title="URL")


@ router.post("/", response_model=PageBaseModel)
async def create_prowrestling(request: CreateProwrestlingRequest):
    """ プロレス大会情報を作成 """
    entity = NotionClient().create_prowrestling(
        title=request.title, date=request.date, url=request.url)
    return PageBaseModel(**entity)


def convert_to_model(entites: list[dict]) -> list[PageBaseModel]:
    return [PageBaseModel(**entity) for entity in entites]
