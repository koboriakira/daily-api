from abc import ABCMeta, abstractmethod
from typing import Optional


class RichTextElement(metaclass=ABCMeta):
    annotations: Optional[dict[str, bool]]
    plain_text: Optional[dict[str, bool]]
    href: Optional[dict[str, bool]]

    def __init__(self, annotations: Optional[dict[str, bool]] = None, plain_text: Optional[dict[str, bool]] = None, href: Optional[dict[str, bool]] = None):
        self.annotations = annotations
        self.plain_text = plain_text
        self.href = href

    def to_dict(self) -> dict:
        result = {
            "type": self.get_type(),
        }
        if self.annotations is not None:
            result["annotations"] = self.annotations
        if self.plain_text is not None:
            result["plain_text"] = self.plain_text
        if self.href is not None:
            result["href"] = self.href
        result[self.get_type()] = self.to_dict_sub()
        return result

    @staticmethod
    def from_entity(rich_text_element: dict) -> "RichTextElement":
        """ dictからRichTextElementを生成する """
        type = rich_text_element["type"]
        if type == "text":
            text = rich_text_element["text"]
            return RichTextTextElement(
                content=text["content"],
                link_url=text["link"]["url"] if "link" in text else None,
                annotations=rich_text_element["annotations"],
                plain_text=rich_text_element["plain_text"],
                href=rich_text_element["href"]
            )
        elif type == "mention":
            mention = rich_text_element["mention"]
            mention_type = mention["type"]
            if mention_type in ["database", "page"]:
                return RichTextMentionElement(
                    mention_type=mention_type,
                    object_id=mention[mention_type]["id"],
                    annotations=rich_text_element["annotations"],
                    plain_text=rich_text_element["plain_text"],
                    href=rich_text_element["href"]
                )
            else:
                raise NotImplementedError
        elif type == "equation":
            raise NotImplementedError
        raise Exception("invalid type")

    @abstractmethod
    def get_type(self) -> str:
        """ text, mention, equationのどれかを返す """
        pass

    @abstractmethod
    def to_dict_sub(self) -> str:
        """ Text, Mention, Equationのそれぞれで実装する """
        pass


class RichTextTextElement(RichTextElement):
    content: str
    link_url: Optional[str] = None

    def __init__(self, content: str, link_url: Optional[str] = None, annotations: Optional[dict[str, bool]] = None, plain_text: Optional[dict[str, bool]] = None, href: Optional[dict[str, bool]] = None):
        self.content = content
        self.link_url = link_url
        super().__init__(annotations, plain_text, href)

    @ staticmethod
    def of(content: str, link_url: Optional[str] = None) -> "RichTextTextElement":
        return RichTextTextElement(
            content=content,
            link_url=link_url
        )

    def get_type(self) -> str:
        return "text"

    def to_dict_sub(self) -> str:
        result = {
            "content": self.content,
        }
        if self.link_url is not None:
            result["link"] = {
                "url": self.link_url
            }
        return result


class RichTextMentionElement(RichTextElement):
    # TODO: 日付やリンクプレビューなどもあるみたい
    # refs: https://developers.notion.com/reference/rich-text#mention
    mention_type: str  # database, page, date, link_preview
    object_id: Optional[str]  # database_idまたはpage_id

    def __init__(self, mention_type: str, object_id: Optional[str] = None, annotations: Optional[dict[str, bool]] = None, plain_text: Optional[dict[str, bool]] = None, href: Optional[dict[str, bool]] = None):
        self.mention_type = mention_type
        self.object_id = object_id
        super().__init__(annotations, plain_text, href)

    @staticmethod
    def of_database(database_id: str) -> "RichTextMentionElement":
        return RichTextMentionElement(
            mention_type="database",
            object_id=database_id
        )

    @staticmethod
    def of_page(page_id: str) -> "RichTextMentionElement":
        return RichTextMentionElement(
            mention_type="page",
            object_id=page_id
        )

    def get_type(self) -> str:
        return "mention"

    def to_dict_sub(self) -> str:
        """ Text, Mention, Equationのそれぞれで実装する """
        result = {
            "type": self.mention_type,
        }
        if self.mention_type in ["database", "page"]:
            result[self.mention_type] = {
                "id": self.object_id
            }

        return result


class RichTextEquationElement(RichTextElement):
    # TODO: not implemented yet
    pass
