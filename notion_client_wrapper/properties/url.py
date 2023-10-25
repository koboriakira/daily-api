from dataclasses import dataclass
from notion_client_wrapper.properties.property import Property
from typing import Optional


@dataclass
class Url(Property):
    url: str
    type: str = "url"

    def __init__(self, name: str, url: str, id: Optional[str] = None):
        self.name = name
        self.url = url
        self.id = id

    @staticmethod
    def of(name: str, param: dict) -> "Url":
        return Url(
            name=name,
            url=param["url"],
            id=param["id"],
        )

    @staticmethod
    def from_url(name: str, url: str) -> "Url":
        return Url(
            name=name,
            url=url
        )

    def __dict__(self):
        result = {
            "type": self.type,
            "url": self.url
        }
        if self.id is not None:
            result["id"] = self.id
        return {
            self.name: result
        }
