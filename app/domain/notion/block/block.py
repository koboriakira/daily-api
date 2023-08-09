from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional


@dataclass
class Block(metaclass=ABCMeta):
    type: str  # 継承先で変わる
    id: Optional[str]
    archived: Optional[bool]
    has_children: Optional[bool]
    created_time: Optional[str]
    last_edited_time: Optional[str]
    parent: Optional[dict[str, str]] = None

    @abstractmethod
    def to_dict(self) -> dict:
        """ dictに変換する。主に書き込み用 """
        pass
