from fastapi import Header
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Union
from app.interface.notion_client import NotionClient
from app.util.authorize_checker import AuthorizeChecker
from notion_client_wrapper.block.rich_text import RichTextBuilder
from notion_client_wrapper.block import Paragraph
from app.model import NotionUrl
from app.router.notion.model.page_base_model import PageBaseModel

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


@router.get("/", response_model=list[PageBaseModel])
async def get_zettlekastens():
    """ Zettlekastenのページを取得する """
    notion_client = NotionClient()

    # テキスト
    entities = notion_client.retrieve_zettlekastens()
    print(entities)
    return convert_to_model(entities)


def convert_to_model(entites: list[dict]) -> list[PageBaseModel]:
    return [PageBaseModel(**entity) for entity in entites]
