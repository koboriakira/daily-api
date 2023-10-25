from notion_client_wrapper.properties.properties import Properties
from notion_client_wrapper.properties.property import Property
from notion_client_wrapper.properties.title import Title
from notion_client_wrapper.properties.text import Text
from notion_client_wrapper.properties.multi_select import MultiSelect
from notion_client_wrapper.properties.select import Select
from notion_client_wrapper.properties.number import Number
from notion_client_wrapper.properties.checkbox import Checkbox
from notion_client_wrapper.properties.status import Status
from notion_client_wrapper.properties.date import Date
from notion_client_wrapper.properties.url import Url
from notion_client_wrapper.properties.relation import Relation
from notion_client_wrapper.properties.notion_datetime import NotionDatetime

from typing import Any

class PropertyTranslator:
    @classmethod
    def from_dict(cls, properties: dict[str, dict]) -> Properties:
        values = []
        for key, value in properties.items():
            values.append(cls.from_property_dict(key, value))
        return Properties(values=values)

    @classmethod
    def from_property_dict(cls, key: str, property: dict[str, Any]) -> 'Property':
        type = property["type"]
        match type:
            case "title":
                return Title.from_property(key, property)
            case "rich_text":
                return Text.from_dict(key, property)
            case "multi_select":
                return MultiSelect.of(key, property)
            case "select":
                return Select.of(key, property)
            case "number":
                return Number.of(key, property)
            case "checkbox":
                return Checkbox.of(key, property)
            case "date":
                return Date.of(key, property)
            case "status":
                return Status.of(key, property)
            case "url":
                return Url.of(key, property)
            case "relation":
                return Relation.of(key, property)
            case "last_edited_time":
                return NotionDatetime.last_edited_time(property["last_edited_time"])
            case "created_time":
                return NotionDatetime.created_time(property["created_time"])
            case _:
                raise Exception(f"Unsupported property type: {type} {property}")
