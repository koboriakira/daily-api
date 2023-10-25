from abc import ABCMeta, abstractmethod
from typing import Optional
from notion_client_wrapper.properties.property import Property
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
from dataclasses import dataclass


@dataclass(frozen=True)
class Properties:
    values: list[Property]

    def __dict__(self):
        result = {}
        for value in self.values:
            result = {**result, **value.__dict__()}
        return result

    @staticmethod
    def from_dict(properties: dict[str, dict]) -> "Properties":
        values = []
        for key, value in properties.items():
            values.append(Property.from_dict(key, value))
        return Properties(values=values)

    def get_title(self) -> Title:
        for value in self.values:
            if isinstance(value, Title):
                return value
        raise Exception(f"Title property not found. properties: {self.values}")

    def get_status(self, name: str) -> Status:
        return self._get_property(name=name, instance_class=Status)

    def get_text(self, name: str) -> Text:
        return self._get_property(name=name, instance_class=Text)

    def get_date(self, name: str) -> Date:
        return self._get_property(name=name, instance_class=Date)

    def get_select(self, name: str) -> Select:
        return self._get_property(name=name, instance_class=Select)

    def get_multi_select(self, name: str) -> MultiSelect:
        return self._get_property(name=name, instance_class=MultiSelect)

    def get_relation(self, name: str) -> Relation:
        return self._get_property(name=name, instance_class=Relation)

    def get_checkbox(self, name: str) -> Checkbox:
        return self._get_property(name=name, instance_class=Checkbox)

    def get_url(self, name: str) -> Url:
        return self._get_property(name=name, instance_class=Url)

    def get_number(self, name: str) -> Number:
        return self._get_property(name=name, instance_class=Number)

    def _get_property(self, name: str, instance_class: type) -> Optional[Property]:
        for value in self.values:
            if isinstance(value, instance_class) and value.name == name:
                return value
        return None
