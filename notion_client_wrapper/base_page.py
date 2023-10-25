from dataclasses import dataclass, field
from notion_client_wrapper.base_operator import BaseOperator
from notion_client_wrapper.block import Block
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.icon import Icon
from notion_client_wrapper.properties.properties import Properties
from notion_client_wrapper.properties.notion_datetime import NotionDatetime
from notion_client_wrapper.properties.title import Title
from notion_client_wrapper.properties.status import Status
from notion_client_wrapper.properties.select import Select
from notion_client_wrapper.properties.multi_select import MultiSelect
from notion_client_wrapper.properties.date import Date
from notion_client_wrapper.properties.text import Text
from notion_client_wrapper.properties.relation import Relation
from notion_client_wrapper.properties.checkbox import Checkbox
from notion_client_wrapper.properties.url import Url
from notion_client_wrapper.properties.number import Number
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

    def get_title(self) -> Title:
        return self.properties.get_title()

    def get_status(self, name: str) -> Status:
        return self.properties.get_property(name=name, instance_class=Status)

    def get_text(self, name: str) -> Text:
        return self.properties.get_property(name=name, instance_class=Text)

    def get_date(self, name: str) -> Date:
        return self.properties.get_property(name=name, instance_class=Date)

    def get_select(self, name: str) -> Select:
        return self.properties.get_property(name=name, instance_class=Select)

    def get_multi_select(self, name: str) -> MultiSelect:
        return self.properties.get_property(name=name, instance_class=MultiSelect)

    def get_relation(self, name: str) -> Relation:
        return self.properties.get_property(name=name, instance_class=Relation)

    def get_checkbox(self, name: str) -> Checkbox:
        return self.properties.get_property(name=name, instance_class=Checkbox)

    def get_url(self, name: str) -> Url:
        return self.properties.get_property(name=name, instance_class=Url)

    def get_number(self, name: str) -> Number:
        return self.properties.get_property(name=name, instance_class=Number)
