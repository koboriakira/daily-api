from dataclasses import dataclass
from app.domain.notion.block.block import Block
from app.domain.notion.block.block_type import BlockType
from app.domain.notion.block.video import Video
from app.domain.notion.block.paragraph import Paragraph
from app.domain.notion.block.quote import Quote
from app.domain.notion.block.heading import Heading
from app.domain.notion.block.divider import Divider
from app.domain.notion.block.bulleted_list_item import BulletedlistItem
from app.domain.notion.block.numbered_list_item import NumberedListItem
from app.domain.notion.block.embed import Embed
from app.domain.notion.block.bookmark import Bookmark
from app.domain.notion.block.image import Image
from app.domain.notion.block.code import Code
from app.domain.notion.block.table import Table
from app.domain.notion.block.child_database import ChildDatabase
from app.domain.notion.block.to_do import ToDo
from app.domain.notion.block.callout import Callout
from app.domain.notion.block.child_page import ChildPage
from typing import Union


@dataclass
class BlockFactory():

    @staticmethod
    def create(block: dict) -> Union[Video, Paragraph, Quote]:
        if block["object"] != "block":
            raise ValueError("block must be of type block")
        block_type = BlockType(block["type"])
        match block_type:
            case BlockType.VIDEO:
                return Video.of(block)
            case BlockType.PARAGRAPH:
                return Paragraph.of(block)
            case BlockType.QUOTE:
                return Quote.of(block)
            case BlockType.HEADING_1:
                return Heading.of(block)
            case BlockType.HEADING_2:
                return Heading.of(block)
            case BlockType.HEADING_3:
                return Heading.of(block)
            case BlockType.DIVIDER:
                return Divider.of(block)
            case BlockType.BULLETED_LIST_ITEM:
                return BulletedlistItem.of(block)
            case BlockType.EMBED:
                return Embed.of(block)
            case BlockType.BOOKMARK:
                return Bookmark.of(block)
            case BlockType.IMAGE:
                return Image.of(block)
            case BlockType.CODE:
                return Code.of(block)
            case BlockType.TABLE:
                return Table.of(block)
            case BlockType.NUMBERED_LIST_ITEM:
                return NumberedListItem.of(block)
            case BlockType.CHILD_DATABASE:
                return ChildDatabase.of(block)
            case BlockType.TO_DO:
                return ToDo.of(block)
            case BlockType.CALLOUT:
                return Callout.of(block)
            case BlockType.CHILD_PAGE:
                return ChildPage.of(block)
            case _:
                print(block)
                raise ValueError(
                    f"block type is not supported {block_type}\n{block}")
