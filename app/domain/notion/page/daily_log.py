from dataclasses import dataclass
from app.domain.notion.page.base_page import BasePage
from app.domain.notion.page.recipe import Recipe
from app.domain.notion.page.webclip import Webclip
from app.domain.notion.properties import Date
from datetime import datetime


@dataclass
class DailyLog(BasePage):
    date: Date  # 日付
    recipes: list[Recipe]  # レシピ
    webclips: list[Webclip]  # Webクリップ

    def __init__(self, id: str, created_time: datetime, last_edited_time: datetime, parent: dict, archived: bool,
                 date: Date, recipes: list[str], webclips: list[Webclip]):
        self.id = id
        self.created_time = created_time
        self.last_edited_time = last_edited_time
        self.parent = parent
        self.archived = archived
        self.date = date
        self.recipes = recipes
        self.webclips = webclips
