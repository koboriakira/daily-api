from app.controller.spotify_controller import SpotifyController
from fastapi import Request, Response, Header
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.interface.notion_client import NotionClient
from app.util.authorize_checker import AuthorizeChecker
from app.domain.notion.block.rich_text import RichText, RichTextBuilder
from app.domain.notion.block import BlockFactory, Block, Paragraph

router = APIRouter()


class Text(BaseModel):
    content: list[str]


@router.post("/")
async def add_text_daily_log(text: Text):
    """ 指定されたテキストをNotionのデイリーログに追加する """
    notion_client = NotionClient()
    for text_content in text.content:
        rich_text = RichTextBuilder.get_instance().add_text(text_content).build()
        paragraph = Paragraph.from_rich_text(rich_text=rich_text)
        notion_client.add_daily_log(block=paragraph)


@router.get("/")
async def get_daily_log(Authorization: Optional[str] = Header(default=None)):
    """ Notionのデイリーログを取得する """
    AuthorizeChecker.validate(access_token=Authorization)
    notion_client = NotionClient()
    return notion_client.get_daily_log()
