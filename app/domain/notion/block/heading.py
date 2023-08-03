from app.domain.notion.block.block import Block
from dataclasses import dataclass


class Heading(Block):
    type: str  # heading_1, heading_2, heading_3
    rich_text: list  # TODO: あとでRichTextクラスを作る
    color: str

    def __init__(self, id: str, archived: bool, created_time: str, last_edited_time: str, has_children: bool,
                 parent: dict, type: str, rich_text: list, color: str):
        super().__init__(id, archived, created_time, last_edited_time, has_children, parent)
        self.type = type
        self.rich_text = rich_text
        self.color = color

    @staticmethod
    def of(block: dict) -> "Heading":
        type = block["type"]
        heading = block[type]
        return Heading(
            id=block["id"],
            archived=block["archived"],
            created_time=block["created_time"],
            last_edited_time=block["last_edited_time"],
            has_children=block["has_children"],
            parent=block["parent"],
            type=type,
            rich_text=heading["rich_text"],
            color=heading["color"]
        )
