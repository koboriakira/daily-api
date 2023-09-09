from fastapi import Header
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Union
from app.interface.notion_client import NotionClient
from app.util.authorize_checker import AuthorizeChecker
from app.domain.notion.block.rich_text import RichTextBuilder
from app.domain.notion.block import Paragraph, Heading

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


class AppendRelationRequest(BaseModel):
    block_id: str
    type: str = "page"  # いったんpageのみ対応


@router.post("/{block_id}/relation", response_model=dict[str, bool])
async def append_relation(block_id: str, request: AppendRelationRequest):
    """ 指定されたバックリンクをNotionのページに追加する """
    notion_client = NotionClient()

    # テキスト
    if request.type == "page":
        rich_text = RichTextBuilder\
            .get_instance()\
            .add_page_mention(page_id=request.block_id)\
            .build()
        paragraph = Paragraph.from_rich_text(rich_text=rich_text)
        notion_client.append_blocks(block_id=block_id, block=paragraph)
        return {
            "success": True
        }
    raise Exception("Not supported type")


class AppendHeadingRequest(BaseModel):
    size: int  # 1~6
    text: str


@router.post("/{block_id}/heading", response_model=dict[str, bool])
async def append_heading(block_id: str, request: AppendHeadingRequest):
    """ 指定された見出しタグをNotionのページに追加する """
    notion_client = NotionClient()
    heading = Heading.from_plain_text(
        heading_size=request.size, text=request.text)
    notion_client.append_blocks(block_id=block_id, block=heading)
    return {
        "success": True
    }


@router.get("/")
async def get_daily_log(Authorization: Optional[str] = Header(default=None)):
    """ Notionのデイリーログを取得する """
    AuthorizeChecker.validate(access_token=Authorization)
    notion_client = NotionClient()
    return notion_client.get_daily_log()
