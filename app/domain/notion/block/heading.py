from app.domain.notion.block.block import Block
from app.domain.notion.block.rich_text import RichText
from dataclasses import dataclass
from typing import Optional


class Heading(Block):
    heading_type: str  # heading_1, heading_2, heading_3
    rich_text: RichText
    color: Optional[str] = None

    def __init__(self,
                 heading_type: str,
                 rich_text: RichText,
                 color: Optional[str] = None,
                 id: Optional[str] = None,
                 archived: Optional[bool] = None,
                 created_time: Optional[str] = None,
                 last_edited_time: Optional[str] = None,
                 has_children: Optional[bool] = None,
                 parent: Optional[dict] = None):
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

    @staticmethod
    def from_plain_text(heading_size: int, text: str) -> "Heading":
        rich_text = RichText.from_plain_text(text)
        return Heading(
            heading_type=f"heading_{heading_size}",
            rich_text=rich_text,
        )

    @property
    def type(self) -> str:
        return self.heading_type

    def to_dict_sub(self) -> dict:
        result = {
            "rich_text": self.rich_text.to_dict(),

        }
        if self.color is not None:
            result["color"] = self.color
        return result
