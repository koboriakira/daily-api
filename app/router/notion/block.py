from fastapi import Header
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Union
from app.interface.notion_client import NotionClient
from app.util.authorize_checker import AuthorizeChecker
from app.domain.notion.block.rich_text import RichTextBuilder
from app.domain.notion.block import Paragraph

router = APIRouter()


class TextBlock(BaseModel):
    block_id: str
    content: Union[list[str], str]


@router.post("/text", response_model=bool)
async def add_text_block(block: TextBlock):
    """ 指定されたテキストをNotionのページに追加する """
    notion_client = NotionClient()

    # テキスト
    if isinstance(block.content, str):
        rich_text = RichTextBuilder.get_instance().add_text(block.content).build()
        paragraph = Paragraph.from_rich_text(rich_text=rich_text)
        notion_client.append_blocks(block_id=block.block_id, block=paragraph)
        return True

    # リスト
    blocks = []
    for text_content in block.content:
        rich_text = RichTextBuilder.get_instance().add_text(text_content).build()
        paragraph = Paragraph.from_rich_text(rich_text=rich_text)
        blocks.append(paragraph)
    notion_client.append_blocks(block_id=block.block_id, block=blocks)
    return True


@router.get("/")
async def get_daily_log(Authorization: Optional[str] = Header(default=None)):
    """ Notionのデイリーログを取得する """
    AuthorizeChecker.validate(access_token=Authorization)
    notion_client = NotionClient()
    return notion_client.get_daily_log()
