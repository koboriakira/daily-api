from dataclasses import dataclass
from app.domain.notion.page.base_page import BasePage
from app.domain.notion.properties import Date
from app.domain.notion.properties import Title
from datetime import datetime


@dataclass(frozen=True)
class Recipe(BasePage):
    # 共通部分
    id: str
    created_time: datetime
    last_edited_time: datetime
    parent: dict  # いずれオブジェクトにする
    archived: bool

    # レシピ固有部分
    title: Title  # タイトル(レシピ名)

    @staticmethod
    def of(query_result: dict):
        properties = query_result["properties"]
        title = Title.of("Name", properties["Name"])
        return Recipe(
            id=query_result["id"],
            created_time=query_result["created_time"],
            last_edited_time=query_result["last_edited_time"],
            parent=query_result["parent"],
            archived=query_result["archived"],
            title=title,
        )
