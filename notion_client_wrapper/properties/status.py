from dataclasses import dataclass
from notion_client_wrapper.properties.property import Property
from typing import Optional


@dataclass
class Status(Property):
    status_id: Optional[str]
    status_name: str
    status_color: Optional[str]
    type: str = "status"

    def __init__(self,
                 name: str,
                 status_name: str,
                 id: Optional[str] = None,
                 status_id: Optional[str] = None,
                 status_color: Optional[str] = None):
        self.name = name
        self.status_name = status_name
        self.id = id
        self.status_id = status_id
        self.status_color = status_color

    @ staticmethod
    def of(name: str, param: dict) -> "Status":
        return Status(
            name=name,
            status_name=param["status"]["name"],
            id=param["id"],
            status_id=param["status"]["id"],
            status_color=param["status"]["color"]
        )

    @staticmethod
    def from_status_name(name: str, status_name: str) -> "Status":
        return Status(
            name=name,
            status_name=status_name
        )

    def is_today(self) -> bool:
        return self.status_name == "Today"

    def __dict__(self):
        result = {
            "type": self.type,
            "status": {
                "name": self.status_name
            }
        }
        if self.status_id is not None:
            result["status"]["id"] = self.status_id
        if self.status_color is not None:
            result["status"]["color"] = self.status_color
        return {self.name: result}
