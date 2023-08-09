from typing import Optional
from dataclasses import dataclass
from app.domain.notion.block.rich_text.rich_text_element import RichTextElement, RichTextTextElement
from app.domain.notion.block.rich_text.rich_text import RichText


@dataclass(frozen=True)
class RichTextBuilder:
    rich_text: list[RichTextElement]

    @staticmethod
    def get_instance() -> "RichTextBuilder":
        return RichTextBuilder(rich_text=[])

    def add_text(self, content: str, link_url: Optional[str] = None) -> "RichTextBuilder":
        self.rich_text.append(RichTextTextElement.of(content, link_url))
        return self

    def build(self) -> RichText:
        return RichText(elements=self.rich_text)
