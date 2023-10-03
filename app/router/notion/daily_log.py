from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.interface.notion_client import NotionClient
from datetime import date as DateObject

router = APIRouter()


class DailyLogRequest(BaseModel):
    daily_goal: Optional[str]
    daily_retro_comment: Optional[str]


@router.post("/", response_model=bool)
async def post_daily_log(request: DailyLogRequest):
    """ デイリーログを更新する """
    notion_client = NotionClient()
    notion_client.update_daily_log(daily_goal=request.daily_goal,
                                   daily_retro_comment=request.daily_retro_comment)


@router.get("/")
async def get_daily_log(date: Optional[DateObject] = None, detail: bool = False):
    """ Notionのデイリーログを取得する """
    notion_client = NotionClient()
    return notion_client.get_daily_log(date=date,
                                       detail=detail)


@router.get("/{date}/id", response_model=str)
async def get_daily_log_id(date: DateObject):
    """ NotionのデイリーログIDを取得する """
    notion_client = NotionClient()
    return notion_client.get_daily_log_id(date=date)
