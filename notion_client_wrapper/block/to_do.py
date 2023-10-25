from notion_client_wrapper.block.block import Block
from notion_client_wrapper.block.rich_text import RichText
from dataclasses import dataclass


class ToDo(Block):
    rich_text: RichText
    color: str
    checked: bool

    def __init__(self, rich_text: RichText, color: str, checked: bool, id: str, archived: bool, created_time: str, last_edited_time: str, has_children: bool,
                 parent: dict):
        super().__init__(id, archived, created_time, last_edited_time, has_children, parent)
        self.rich_text = rich_text
        self.color = color
        self.checked = checked

    @staticmethod
    def of(block: dict) -> "ToDo":
        to_do = block["to_do"]
        rich_text = RichText.from_entity(to_do["rich_text"])
        return ToDo(
            id=block["id"],
            archived=block["archived"],
            created_time=block["created_time"],
            last_edited_time=block["last_edited_time"],
            has_children=block["has_children"],
            parent=block["parent"],
            rich_text=rich_text,
            color=to_do["color"],
            checked=to_do["checked"]
        )

    def type(self) -> str:
        return "to_do"

    def to_dict_sub(self) -> dict:
        raise NotImplementedError
