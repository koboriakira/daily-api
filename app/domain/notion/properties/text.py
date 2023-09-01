from dataclasses import dataclass
from app.domain.notion.properties.property import Property
from app.domain.notion.block.rich_text import RichText
from typing import Optional


@dataclass
class Text(Property):
    rich_text: RichText

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
        raise NotImplementedError()

    @ staticmethod
    def from_plain_text(name: str, text: str) -> "Text":
        return Text(
            name=name,
            text=text,
        )

    @property
    def text(self) -> str:
        return self.rich_text.to_plain_text()
