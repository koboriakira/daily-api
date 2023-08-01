from dataclasses import dataclass
from app.domain.notion.properties.property import Property
from typing import Optional


@dataclass
class Url(Property):
    url: str
    id: str
    type: str = "url"

    def __init__(self, name: str, url: str, id: str):
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

    def __dict__(self):
        return {
            self.name: {
                "id": self.id,
                "type": self.type,
                "url": self.url
            }
        }
