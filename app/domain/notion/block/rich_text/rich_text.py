from app.domain.notion.block.rich_text.rich_text_element import RichTextElement
from dataclasses import dataclass


@dataclass(frozen=True)
class RichText:
    elements: list[RichTextElement]

    @staticmethod
    def from_entity(rich_text: list) -> "RichText":
        return RichText(elements=list(map(lambda x: RichTextElement.from_entity(x), rich_text)))

    def to_dict(self) -> list[dict]:
        return list(map(lambda x: x.to_dict(), self.elements))
