from abc import ABCMeta, abstractmethod
from typing import Optional, Any
from notion_client_wrapper.properties.title import Title
from notion_client_wrapper.properties.text import Text
from notion_client_wrapper.properties.multi_select import MultiSelect

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
            case "rich_text":
                return Text.from_dict(key, property)
            case "multi_select":
                return MultiSelect.of(key, property)
            case _:
                raise Exception(f"Unsupported property type: {type}")
