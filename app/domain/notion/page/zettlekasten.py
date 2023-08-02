from dataclasses import dataclass
from app.domain.notion.page.base_page import BasePage
from app.domain.notion.properties import Date
from app.domain.notion.properties import Title
from app.domain.notion.properties import Url
from datetime import datetime


@dataclass
class Zettlekasten(BasePage):
    title: Title

    def __init__(self, id: str, created_time: datetime, last_edited_time: datetime, parent: dict, archived: bool,
                 title: Title):
        self.id = id
        self.created_time = created_time
        self.last_edited_time = last_edited_time
        self.parent = parent
        self.archived = archived
        self.title = title

    @staticmethod
    def of(query_result: dict) -> 'Zettlekasten':
        properties = query_result["properties"]
        title = Title.from_properties(properties)
        return Zettlekasten(
            id=query_result["id"],
            created_time=query_result["created_time"],
            last_edited_time=query_result["last_edited_time"],
            parent=query_result["parent"],
            archived=query_result["archived"],
            title=title)
