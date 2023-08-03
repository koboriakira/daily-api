from app.domain.notion.block.block import Block
from dataclasses import dataclass


class Bookmark(Block):
    caption: list
    bookmark_url: str

    def __init__(self, id: str, archived: bool, created_time: str, last_edited_time: str, has_children: bool,
                 parent: dict, caption: list, bookmark_url: str):
        super().__init__(id, archived, created_time, last_edited_time, has_children, parent)
        self.caption = caption
        self.bookmark_url = bookmark_url

    @staticmethod
    def of(block: dict) -> "Bookmark":
        bookmark = block["bookmark"]
        return Bookmark(
            id=block["id"],
            archived=block["archived"],
            created_time=block["created_time"],
            last_edited_time=block["last_edited_time"],
            has_children=block["has_children"],
            parent=block["parent"],
            caption=bookmark["caption"],
            bookmark_url=bookmark["url"] if "url" in bookmark else ""
        )
