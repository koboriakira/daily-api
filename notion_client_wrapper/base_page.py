from dataclasses import dataclass, field
from notion_client_wrapper.base_operator import BaseOperator
from notion_client_wrapper.cover import Cover
from notion_client_wrapper.block import Block
from notion_client_wrapper.icon import Icon
from notion_client_wrapper.properties import Properties
from typing import Optional

@dataclass(frozen=True)
class BasePage:
    id: str
    created_time: str
    last_edited_time: str
    created_by: BaseOperator
    last_edited_by: BaseOperator
    properties: Properties
    cover: Optional[Cover] = None
    icon: Optional[Icon] = None
    archived: bool = False
    block_children: list[Block] = field(default_factory=list)
    object = "page"
