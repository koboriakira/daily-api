from fastapi import Header
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Union
from app.interface.notion_client import NotionClient
from app.domain.notion.block.rich_text import RichTextBuilder
from app.domain.notion.block import Paragraph
from datetime import date as DateObject

router = APIRouter()


class Text(BaseModel):
    content: Union[list[str], str]


@router.post("/", response_model=bool)
async def add_text_daily_log(text: Text):
    """ 指定されたテキストをNotionのデイリーログに追加する """
    notion_client = NotionClient()

    # テキスト
    if isinstance(text.content, str):
        rich_text = RichTextBuilder.get_instance().add_text(text.content).build()
        paragraph = Paragraph.from_rich_text(rich_text=rich_text)
        notion_client.add_daily_log(block=paragraph)
        return True

    # リスト
    for text_content in text.content:
        rich_text = RichTextBuilder.get_instance().add_text(text_content).build()
        paragraph = Paragraph.from_rich_text(rich_text=rich_text)
        notion_client.add_daily_log(block=paragraph)
    return True


@router.get("/")
async def get_daily_log(Authorization: Optional[str] = Header(default=None)):
    """ Notionのデイリーログを取得する """
    notion_client = NotionClient()
    return notion_client.get_daily_log()


@router.get("/{date}/id", response_model=str)
async def get_daily_log_id(date: DateObject):
    """ NotionのデイリーログIDを取得する """
    notion_client = NotionClient()
    return notion_client.get_daily_log_id(date=date)
