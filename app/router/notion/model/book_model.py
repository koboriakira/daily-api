from app.router.notion.model.page_base_model import PageBaseModel
from pydantic import Field
from typing import Optional


class Book(PageBaseModel):
    status: Optional[str] = Field(default=None, title="ステータス")


def convert_to_book_model(entites: list[dict]) -> list[Book]:
    return [Book(**entity) for entity in entites]
