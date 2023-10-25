from notion_client_wrapper.block.block import Block
from notion_client_wrapper.block.rich_text import RichText
from dataclasses import dataclass


class BulletedlistItem(Block):
    rich_text: RichText
    color: str

    def __init__(self, rich_text: RichText, color: str, id: str, archived: bool, created_time: str, last_edited_time: str, has_children: bool,
                 parent: dict):
        super().__init__(id, archived, created_time, last_edited_time, has_children, parent)
        self.rich_text = rich_text
        self.color = color

    @staticmethod
    def of(block: dict) -> "BulletedlistItem":
        bulleted_list_item = block["bulleted_list_item"]
        rich_text = RichText.from_entity(bulleted_list_item["rich_text"])
        return BulletedlistItem(
            id=block["id"],
            archived=block["archived"],
            created_time=block["created_time"],
            last_edited_time=block["last_edited_time"],
            has_children=block["has_children"],
            parent=block["parent"],
            rich_text=rich_text,
            color=bulleted_list_item["color"]
        )

    @property
    def type(self) -> str:
        return "bulleted_list_item"

    def to_dict_sub(self) -> dict:
        raise NotImplementedError
