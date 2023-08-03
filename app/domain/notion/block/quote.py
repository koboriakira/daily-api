from app.domain.notion.block.block import Block
from dataclasses import dataclass


class Quote(Block):
    rich_text: list  # TODO: あとでRichTextクラスを作る
    color: str

    def __init__(self, id: str, archived: bool, created_time: str, last_edited_time: str, has_children: bool,
                 parent: dict, rich_text: list, color: str):
        super().__init__(id, archived, created_time, last_edited_time, has_children, parent)
        self.rich_text = rich_text
        self.color = color

    @staticmethod
    def of(block: dict) -> "Quote":
        quote = block["quote"]
        return Quote(
            id=block["id"],
            archived=block["archived"],
            created_time=block["created_time"],
            last_edited_time=block["last_edited_time"],
            has_children=block["has_children"],
            parent=block["parent"],
            rich_text=quote["rich_text"],
            color=quote["color"]
        )
