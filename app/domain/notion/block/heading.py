from app.domain.notion.block.block import Block
from app.domain.notion.block.rich_text import RichText
from dataclasses import dataclass


class Heading(Block):
    heading_type: str  # heading_1, heading_2, heading_3
    rich_text: RichText
    color: str

    def __init__(self, heading_type: str, rich_text: RichText, color: str, id: str, archived: bool, created_time: str, last_edited_time: str, has_children: bool,
                 parent: dict):
        super().__init__(id, archived, created_time, last_edited_time, has_children, parent)
        self.heading_type = heading_type
        self.rich_text = rich_text
        self.color = color

    @staticmethod
    def of(block: dict) -> "Heading":
        heading_type = block["type"]
        heading = block[heading_type]
        rich_text = RichText.from_entity(heading["rich_text"])
        return Heading(
            id=block["id"],
            archived=block["archived"],
            created_time=block["created_time"],
            last_edited_time=block["last_edited_time"],
            has_children=block["has_children"],
            parent=block["parent"],
            heading_type=heading_type,
            rich_text=rich_text,
            color=heading["color"]
        )

    @property
    def type(self) -> str:
        return "heading"

    def to_dict_sub(self) -> dict:
        raise NotImplementedError
