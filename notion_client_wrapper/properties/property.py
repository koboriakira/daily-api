from abc import ABCMeta, abstractmethod
from typing import Optional, Any
from notion_client_wrapper.properties.title import Title


class Property(metaclass=ABCMeta):
    id: Optional[str]
    name: str
    type: str

    @abstractmethod
    def __dict__(self):
        pass

    def from_dict(key: str, property: dict[str, Any]) -> 'Property':
        type = property["type"]
        match type:
            case "title":
                return Title.from_property(key, property)
