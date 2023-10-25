from notion_client_wrapper.block.rich_text.rich_text_element import RichTextElement
from dataclasses import dataclass


@dataclass(frozen=True)
class RichText:
    elements: list[RichTextElement]

    @staticmethod
    def from_entity(rich_text: list) -> "RichText":
        return RichText(elements=list(map(lambda x: RichTextElement.from_entity(x), rich_text)))

    @staticmethod
    def from_plain_text(text: str) -> "RichText":
        rich_text_element = RichTextElement.from_plain_text(text)
        return RichText(elements=[rich_text_element])

    def to_plain_text(self) -> str:
        return "".join(map(lambda x: x.to_plain_text(), self.elements))

    def to_dict(self) -> list[dict]:
        return list(map(lambda x: x.to_dict(), self.elements))
