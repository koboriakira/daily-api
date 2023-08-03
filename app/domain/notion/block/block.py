from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional


@dataclass
class Block(metaclass=ABCMeta):
    id: str
    archived: bool
    has_children: bool
    created_time: str
    last_edited_time: str
    type: str  # 継承先で変わる
    parent: Optional[dict[str, str]] = None
