from dataclasses import dataclass
from app.domain.notion.properties.property import Property
from typing import Optional


@dataclass(frozen=True)
class Title(Property):
    name: str
    value: list[dict]
    id: str = "title"
    type: str = "title"

    @staticmethod
    def of(name: str, param: dict) -> "Title":
        return Title(
            name=name,
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
