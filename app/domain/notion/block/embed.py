from app.domain.notion.block.block import Block
from dataclasses import dataclass


class Embed(Block):
    caption: list
    embed_url: str

    def __init__(self, id: str, archived: bool, created_time: str, last_edited_time: str, has_children: bool,
                 parent: dict, caption: list, embed_url: str):
        super().__init__(id, archived, created_time, last_edited_time, has_children, parent)
        self.caption = caption
        self.embed_url = embed_url

    @staticmethod
    def of(block: dict) -> "Embed":
        embed = block["embed"]
        return Embed(
            id=block["id"],
            archived=block["archived"],
            created_time=block["created_time"],
            last_edited_time=block["last_edited_time"],
            has_children=block["has_children"],
            parent=block["parent"],
            caption=embed["caption"],
            embed_url=embed["url"] if "url" in embed else ""
        )
