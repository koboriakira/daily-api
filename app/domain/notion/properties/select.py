from dataclasses import dataclass
from app.domain.notion.properties.property import Property
from typing import Optional


@dataclass
class Select(Property):
    selected_name: str
    selected_id: str
    selected_color: str
    type: str = "select"

    def __init__(self,
                 name: str,
                 selected_name: str,
                 selected_id: str,
                 selected_color: str,
                 id: Optional[str] = None,):
        self.name = name
        self.selected_name = selected_name
        self.selected_id = selected_id if selected_id is not None else "undefined"
        self.selected_color = selected_color if selected_color is not None else "undefined"
        self.id = id

    @ staticmethod
    def of(name: str, param: dict) -> Optional["Select"]:
        select = param["select"]
        if select is None:
            return None
        return Select(
            name=name,
            selected_id=select["id"],
            selected_name=select["name"],
            selected_color=select["color"],
            id=param["id"],
        )

    def __dict__(self):
        result = {
            "type": self.type,
            "select": {
                "id": self.selected_id,
                "name": self.selected_name,
                "color": self.selected_color
            }
        }
        if self.id is not None:
            result["id"] = self.id
        return {self.name: result}
