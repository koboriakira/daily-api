from app.domain.notion.block.block import Block
from dataclasses import dataclass
from typing import Optional


class Paragraph(Block):
    rich_text: list[dict]  # TODO: あとでRichTextクラスを作る
    color: Optional[str] = None

    def __init__(self,
                 rich_text: list,
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
        return Paragraph(
            id=block["id"],
            archived=block["archived"],
            created_time=block["created_time"],
            last_edited_time=block["last_edited_time"],
            has_children=block["has_children"],
            parent=block["parent"],
            rich_text=paragraph["rich_text"],
            color=paragraph["color"]
        )

    @staticmethod
    def of_for_insert(text: str) -> "Paragraph":
        """ 書き込み用のParagraphを生成する """
        rich_text = [
            {
                "type": "text",
                "text": {
                    "content": text,
                    "link": None
                }
            }
        ]
        return Paragraph(rich_text=rich_text)

    def to_dict(self) -> dict:
        paragraph = {
            "rich_text": self.rich_text,
        }
        if self.color is not None:
            paragraph["color"] = self.color
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": paragraph
        }
