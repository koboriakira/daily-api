from dataclasses import dataclass
from app.domain.notion.properties.property import Property
from typing import Optional


@dataclass
class Title(Property):
    value: list[dict]
    id: str
    type: str = "title"

    def __init__(self, name: str, id: str, value: list[dict]):
        self.name = name
        self.id = id
        self.value = value

    @staticmethod
    def of(name: str, param: dict) -> "Title":
        return Title(
            name=name,
            id=param["id"],
            value=param["title"]
        )

    def __dict__(self):
        return {
            self.name: {
                "id": self.id,
                "type": self.type,
                "title": self.value
            }
        }
