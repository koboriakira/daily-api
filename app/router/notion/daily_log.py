from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.interface.notion_client import NotionClient
from datetime import date as DateObject
from app.router.response.api_response import ApiResponse, success

router = APIRouter()


class DailyLogRequest(BaseModel):
    daily_goal: Optional[str]
    daily_retro_comment: Optional[str]


@router.post("/{date}/", response_model=ApiResponse)
async def post_daily_log(date: DateObject, request: DailyLogRequest):
    """ デイリーログを更新する """
    print(request)
    notion_client = NotionClient()
    notion_client.update_daily_log(date=date,
                                   daily_goal=request.daily_goal,
                                   daily_retro_comment=request.daily_retro_comment)
    return success(data=None)


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
