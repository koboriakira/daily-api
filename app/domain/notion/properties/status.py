from dataclasses import dataclass
from app.domain.notion.properties.property import Property
from typing import Optional


@dataclass
class Status(Property):
    status_id: str
    status_name: str
    status_color: str
    id: str
    type: str = "url"

    def __init__(self, name: str, id: str, status_id: str, status_name: str, status_color: str):
        self.name = name
        self.id = id
        self.status_id = status_id
        self.status_name = status_name
        self.status_color = status_color

    @staticmethod
    def of(name: str, param: dict) -> "Status":
        return Status(
            name=name,
            id=param["id"],
            status_id=param["status"]["id"],
            status_name=param["status"]["name"],
            status_color=param["status"]["color"]
        )

    def __dict__(self):
        return {
            self.name: {
                "id": self.id,
                "type": self.type,
                "url": self.url
            }
        }
