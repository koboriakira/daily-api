from fastapi import Header
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Union
from app.interface.notion_client import NotionClient
from app.util.authorize_checker import AuthorizeChecker
from app.domain.notion.block.rich_text import RichTextBuilder
from app.domain.notion.block import Paragraph
from app.model.url import NotionUrl

router = APIRouter()


class ZettlekastenRequest(BaseModel):
    title: str
    url: Optional[str] = None


@router.post("/", response_model=NotionUrl)
async def create_zettlekasten(request: ZettlekastenRequest):
    """ NotionのZettlekastenに新しいページを追加する """
    notion_client = NotionClient()

    # テキスト
    page = notion_client.create_zettlekasten(
        request.title,
        url=request.url)
    return NotionUrl(url=page["url"], block_id=page["id"])
