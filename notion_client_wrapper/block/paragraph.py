from notion_client_wrapper.block.block import Block
from notion_client_wrapper.block.rich_text import RichText
from dataclasses import dataclass
from typing import Optional


class Paragraph(Block):
    rich_text: RichText
    color: Optional[str] = None

    def __init__(self,
                 rich_text: RichText,
                 color: Optional[str] = None,
                 id: Optional[str] = None,
                 archived: Optional[bool] = None,
                 created_time: Optional[str] = None,
                 last_edited_time: Optional[str] = None,
                 has_children: Optional[bool] = None,
                 parent: Optional[dict] = None):
        super().__init__(id, archived, created_time, last_edited_time, has_children, parent)
        self.rich_text = rich_text
        self.color = color

    @ staticmethod
    def of(block: dict) -> "Paragraph":
        paragraph = block["paragraph"]
        rich_text = RichText.from_entity(paragraph["rich_text"])
        return Paragraph(
            rich_text=rich_text,
            id=block["id"],
            archived=block["archived"],
            created_time=block["created_time"],
            last_edited_time=block["last_edited_time"],
            has_children=block["has_children"],
            parent=block["parent"],
            color=paragraph["color"]
        )

    @staticmethod
    def from_rich_text(rich_text: RichText) -> "Paragraph":
        return Paragraph(rich_text=rich_text)

    @staticmethod
    def from_plain_text(text: str) -> "Paragraph":
        rich_text = RichText.from_plain_text(text)
        return Paragraph(rich_text=rich_text)

    @property
    def type(self) -> str:
        return "paragraph"

    def to_dict_sub(self) -> dict:
        result = {
            "rich_text": self.rich_text.to_dict(),
        }
        if self.color is not None:
            result["color"] = self.color
        return result
