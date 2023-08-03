from dataclasses import dataclass
from app.domain.notion.page.base_page import BasePage
from app.domain.notion.properties import Date
from app.domain.notion.properties import Title
from app.domain.notion.properties import Url
from app.domain.notion.block import Block
from datetime import datetime


@dataclass
class Webclip(BasePage):
    url: Url
    title: Title  # タイトル(レシピ名)

    def __init__(self, id: str, created_time: datetime, last_edited_time: datetime, parent: dict, archived: bool,
                 title: Title, url: Url, blocks: list[Block]):
        self.id = id
        self.created_time = created_time
        self.last_edited_time = last_edited_time
        self.parent = parent
        self.archived = archived
        self.title = title
        self.url = url
        self.blocks = blocks

    @staticmethod
    def of(query_result: dict, blocks: list[Block]):
        properties = query_result["properties"]
        url = Url.of("URL", properties["URL"])
        title = Title.from_properties(properties)
        return Webclip(
            id=query_result["id"],
            created_time=query_result["created_time"],
            last_edited_time=query_result["last_edited_time"],
            parent=query_result["parent"],
            archived=query_result["archived"],
            title=title,
            url=url,
            blocks=blocks,
        )
