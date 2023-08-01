from dataclasses import dataclass
from app.domain.notion.base_page import BasePage
from app.domain.notion.properties.date import Date
from datetime import datetime


@dataclass(frozen=True)
class DailyLog(BasePage):
    id: str
    created_time: datetime
    last_edited_time: datetime
    parent: dict  # いずれオブジェクトにする
    # cover:
    # icon
    archived: bool
    date: Date  # 日付
    recipes: list[str]  # レシピ

    @staticmethod
    def of(query_result: dict):
        properties = query_result["properties"]
        date = Date.of("日付", properties["日付"])
        recipe_ids = properties["レシピ"]["relation"]
        return DailyLog(
            id=query_result["id"],
            created_time=query_result["created_time"],
            last_edited_time=query_result["last_edited_time"],
            parent=query_result["parent"],
            archived=query_result["archived"],
            date=date,
            recipes=recipe_ids
        )
