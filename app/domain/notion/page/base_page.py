from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from app.domain.notion.properties.property import Properties


class BasePage(metaclass=ABCMeta):
    id: str
    created_time: datetime
    last_edited_time: datetime
    parent: dict  # いずれオブジェクトにする
    archived: bool
    object: str = "page"
