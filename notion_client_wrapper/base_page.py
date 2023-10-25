from dataclasses import dataclass, field
from notion_client_wrapper.base_operator import BaseOperator
from notion_client_wrapper.block import Block
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.icon import Icon
from notion_client_wrapper.properties.properties import Properties
from notion_client_wrapper.properties.notion_datetime import NotionDatetime
from typing import Optional

@dataclass(frozen=True)
class BasePage:
    id: str
    url: str
    created_time: NotionDatetime
    last_edited_time: NotionDatetime
    created_by: BaseOperator
    last_edited_by: BaseOperator
    properties: Properties
    cover: Optional[Cover] = None
    icon: Optional[Icon] = None
    archived: bool = False
    parent: Optional[dict] = None
    block_children: list[Block] = field(default_factory=list)
    object = "page"
