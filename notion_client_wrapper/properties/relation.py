from dataclasses import dataclass
from app.domain.notion.properties.property import Property
from typing import Optional


@dataclass
class Relation(Property):
    id_list: list[str]
    type: str = "relation"
    has_more: bool = False

    def __init__(self, name: str, id: Optional[str] = None, id_list: list[str] = [], has_more: bool = False):
        self.name = name
        self.id = id
        self.id_list = id_list
        self.has_more = has_more

    @staticmethod
    def of(name: str, property: dict[str, str]) -> "Relation":
        id_list = list(map(lambda r: r["id"], property["relation"]))
        return Relation(
            name=name,
            id_list=id_list,
            has_more=property["has_more"])

    @staticmethod
    def from_id_list(name: str, id_list: list[str]) -> "Relation":
        return Relation(
            name=name,
            id_list=id_list,
        )

    @classmethod
    def from_id(cls, name: str, id: str) -> "Relation":
        return cls.from_id_list(name=name, id_list=[id])

    def __dict__(self):
        result = {
            "type": self.type,
            "relation": [
                {
                    "id": id
                } for id in self.id_list
            ],
            "has_more": self.has_more
        }
        if self.id is not None:
            result["relation"]["id"] = self.id
        return {
            self.name: result
        }
