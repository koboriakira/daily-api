from dataclasses import dataclass
from app.domain.notion.properties.property import Property
from typing import Optional


@dataclass
class Title(Property):
    text: str
    value: list[dict]
    type: str = "title"

    def __init__(self, name: str, id: Optional[str] = None, value: list[dict] = [], text: Optional[str] = None):
        self.name = name
        self.id = id
        self.value = value
        self.text = text

    @classmethod
    def from_properties(cls, properties: dict) -> "Title":
        if "Name" in properties:
            return cls.__of("Name", properties["Name"])
        if "Title" in properties:
            return cls.__of("Title", properties["Title"])
        if "名前" in properties:
            return cls.__of("名前", properties["名前"])
        raise Exception(f"Title property not found. properties: {properties}")

    @classmethod
    def from_property(cls, key:str, property: dict) -> "Title":
        return cls.__of(key, property)

    def __dict__(self):
        result = {
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": self.text
                    }
                }
            ]
        }
        if self.id is not None:
            result["title"]["id"] = self.id
        return {
            self.name: result
        }

    @staticmethod
    def __of(name: str, param: dict) -> "Title":
        return Title(
            name=name,
            id=param["id"],
            value=param["title"],
            text="".join([item["plain_text"] for item in param["title"]])
        )

    @ staticmethod
    def from_plain_text(name: str, text: str) -> "Title":
        return Title(
            name=name,
            text=text,
        )
