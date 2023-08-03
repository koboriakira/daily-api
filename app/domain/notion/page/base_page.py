from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from app.domain.notion.properties.property import Properties
from app.domain.notion.block import Block
from typing import Optional


class BasePage(metaclass=ABCMeta):
    id: str
    created_time: datetime
    last_edited_time: datetime
    parent: dict  # いずれオブジェクトにする
    archived: bool
    blocks: list[Block]
    cover: Optional[dict] = None
    icon: Optional[dict] = None
    object: str = "page"
