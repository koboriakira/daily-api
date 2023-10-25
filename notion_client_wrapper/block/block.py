from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional


@dataclass
class Block(metaclass=ABCMeta):
    id: Optional[str]
    archived: Optional[bool]
    has_children: Optional[bool]
    created_time: Optional[str]
    last_edited_time: Optional[str]
    parent: Optional[dict[str, str]] = None

    def to_dict(self) -> dict:
        result = {
            "object": "block",
        }
        if self.id is not None:
            result["id"] = self.id
        if self.archived is not None:
            result["archived"] = self.archived
        if self.has_children is not None:
            result["has_children"] = self.has_children
        if self.created_time is not None:
            result["created_time"] = self.created_time
        if self.last_edited_time is not None:
            result["last_edited_time"] = self.last_edited_time
        if self.parent is not None:
            result["parent"] = self.parent
        result["type"] = self.type
        result[self.type] = self.to_dict_sub()
        return result

    @abstractmethod
    def to_dict_sub(self) -> dict:
        pass

    @property
    @abstractmethod
    def type(self) -> str:
        pass
