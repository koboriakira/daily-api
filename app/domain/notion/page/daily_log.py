from dataclasses import dataclass
from app.domain.notion.page import BasePage
from app.domain.notion.properties import Date
from datetime import datetime


@dataclass
class DailyLog(BasePage):
    date: Date  # 日付
    recipes: list[str]  # レシピ

    def __init__(self, id: str, created_time: datetime, last_edited_time: datetime, parent: dict, archived: bool,
                 date: Date, recipes: list[str]):
        self.id = id
        self.created_time = created_time
        self.last_edited_time = last_edited_time
        self.parent = parent
        self.archived = archived
        self.date = date
        self.recipes = recipes

    @staticmethod
    def of(query_result: dict):
        print(query_result)
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
