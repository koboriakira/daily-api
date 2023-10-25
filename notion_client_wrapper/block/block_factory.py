from dataclasses import dataclass
from notion_client_wrapper.block.block import Block
from notion_client_wrapper.block.block_type import BlockType
from notion_client_wrapper.block.video import Video
from notion_client_wrapper.block.paragraph import Paragraph
from notion_client_wrapper.block.quote import Quote
from notion_client_wrapper.block.heading import Heading
from notion_client_wrapper.block.divider import Divider
from notion_client_wrapper.block.bulleted_list_item import BulletedlistItem
from notion_client_wrapper.block.numbered_list_item import NumberedListItem
from notion_client_wrapper.block.embed import Embed
from notion_client_wrapper.block.bookmark import Bookmark
from notion_client_wrapper.block.image import Image
from notion_client_wrapper.block.code import Code
from notion_client_wrapper.block.table import Table
from notion_client_wrapper.block.child_database import ChildDatabase
from notion_client_wrapper.block.to_do import ToDo
from notion_client_wrapper.block.callout import Callout
from notion_client_wrapper.block.child_page import ChildPage
from typing import Union


@dataclass
class BlockFactory():

    @staticmethod
    def create(block: dict) -> Block:
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
