from fastapi import APIRouter
from pydantic import BaseModel
from app.interface.notion_client import NotionClient
from datetime import date as DateObject

router = APIRouter()


@router.get("/{isoweek}/id", response_model=dict)
async def get_weekly_log_id(isoweek: str):
    """ NotionのデイリーログIDを取得する """

    # "2023-W01"のような文字列を、年と週番号に分割する
    year = int(isoweek[:4])
    isoweeknum = int(isoweek[-2:])

    notion_client = NotionClient()
    result = notion_client.find_weekly_log(year=year, isoweeknum=isoweeknum)

    return {
        "weekly_log_id": result["id"] if result else None,
    }


class CreateWeeklyLogRequest(BaseModel):
    year: int
    isoweeknum: int


@ router.post("/", response_model=dict)
async def create_weekly_log(request: CreateWeeklyLogRequest):
    """ 指定された週のウィークリーログを作成する """
    """ ウィークリーログを作成する """
    notion_client = NotionClient()
    notion_client.create_weekly_log(year=request.year,
                                    isoweeknum=request.isoweeknum)
    return {
        "success": True,
    }
