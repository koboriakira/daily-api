from app.domain.notion.block.block import Block
from app.domain.notion.block.rich_text import RichText
from dataclasses import dataclass


class Callout(Block):
    rich_text: RichText
    color: str

    def __init__(self, rich_text: RichText, color: str, id: str, archived: bool, created_time: str, last_edited_time: str, has_children: bool,
                 parent: dict):
        super().__init__(id, archived, created_time, last_edited_time, has_children, parent)
        self.rich_text = rich_text
        self.color = color

    @staticmethod
    def of(block: dict) -> "Callout":
        callout = block["callout"]
        rich_text = RichText.from_entity(callout["rich_text"])
        return Callout(
            id=block["id"],
            archived=block["archived"],
            created_time=block["created_time"],
            last_edited_time=block["last_edited_time"],
            has_children=block["has_children"],
            parent=block["parent"],
            rich_text=rich_text,
            color=callout["color"]
        )

    @property
    def type(self) -> str:
        return "callout"

    def to_dict_sub(self) -> dict:
        raise NotImplementedError
