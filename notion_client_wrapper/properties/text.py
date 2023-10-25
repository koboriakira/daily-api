from dataclasses import dataclass
from notion_client_wrapper.properties.property import Property
from notion_client_wrapper.block.rich_text import RichText
from typing import Optional


@dataclass
class Text(Property):
    rich_text: RichText
    type: str = "rich_text"

    def __init__(self, name: str, rich_text: RichText, id: Optional[str] = None):
        self.name = name
        self.id = id
        self.rich_text = rich_text

    @staticmethod
    def from_dict(name: str, param: dict) -> "Text":
        try:
            rich_text = RichText.from_entity(param["rich_text"])
            id = param["id"]
            return Text(
                name=name,
                id=id,
                rich_text=rich_text,
            )
        except Exception as e:
            print(param)
            raise e

    def __dict__(self):
        result = {
            "type": self.type,
            "rich_text": self.rich_text.to_dict()
        }
        return {self.name: result}

    @staticmethod
    def from_plain_text(name: str, text: str) -> "Text":
        return Text(
            name=name,
            rich_text=RichText.from_plain_text(text=text),
        )

    @property
    def text(self) -> str:
        return self.rich_text.to_plain_text()
