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

    @classmethod
    def from_properties(cls, properties: dict) -> "Title":
        if "Name" in properties:
            return cls.__of("Name", properties["Name"])
        if "Title" in properties:
            return cls.__of("Title", properties["Title"])
        if "名前" in properties:
            return cls.__of("名前", properties["名前"])
        raise Exception(f"Title property not found. properties: {properties}")

    def __dict__(self):
        return {
            self.name: {
                "id": self.id,
                "type": self.type,
                "title": self.value
            }
        }

    @staticmethod
    def __of(name: str, param: dict) -> "Title":
        return Title(
            name=name,
            id=param["id"],
            value=param["title"]
        )
