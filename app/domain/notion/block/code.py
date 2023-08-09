from app.domain.notion.block.block import Block
from dataclasses import dataclass


class Code(Block):
    def __init__(self, id: str, archived: bool, created_time: str, last_edited_time: str, has_children: bool,
                 parent: dict):
        super().__init__(id, archived, created_time, last_edited_time, has_children, parent)

    @staticmethod
    def of(block: dict) -> "Code":
        return Code(
            id=block["id"],
            archived=block["archived"],
            created_time=block["created_time"],
            last_edited_time=block["last_edited_time"],
            has_children=block["has_children"],
            parent=block["parent"],
        )

    @property
    def type(self) -> str:
        return "code"

    def to_dict_sub(self) -> dict:
        raise NotImplementedError
