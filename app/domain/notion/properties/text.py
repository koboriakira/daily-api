from dataclasses import dataclass
from app.domain.notion.properties.property import Property
from typing import Optional


@dataclass
class Text(Property):
    text: str
    value: list[dict]
    type: str = "rich_text"

    def __init__(self, name: str, id: Optional[str] = None, value: list[dict] = [], text: Optional[str] = None):
        self.name = name
        self.id = id
        self.value = value
        self.text = text

    @staticmethod
    def from_dict(name: str, param: dict) -> "Text":
        id = param["id"]
        value = param["title"]
        text = "".join([item["plain_text"] for item in param["title"]])
        return Text(
            name=name,
            id=id,
            value=value,
            text=text
        )

    def __dict__(self):
        result = {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": self.text
                    }
                }
            ]
        }
        if self.id is not None:
            result["rich_text"]["id"] = self.id
        return {
            self.name: result
        }

    @ staticmethod
    def from_plain_text(name: str, text: str) -> "Text":
        return Text(
            name=name,
            text=text,
        )
