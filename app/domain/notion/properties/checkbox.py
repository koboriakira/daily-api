from dataclasses import dataclass
from app.domain.notion.properties.property import Property
from typing import Optional


@dataclass
class Checkbox(Property):
    checked: bool
    type: str = "checkbox"

    def __init__(self,
                 name: str,
                 checked: bool,
                 id: Optional[str] = None,):
        self.name = name
        self.checked = checked
        self.id = id

    @ staticmethod
    def of(name: str, param: dict) -> "Checkbox":
        return Checkbox(
            name=name,
            checked=param['checkbox'],
            id=param["id"],
        )

    @staticmethod
    def from_bool(name: str, checked: bool) -> "Checkbox":
        return Checkbox(
            name=name,
            checked=checked
        )

    def __dict__(self):
        result = {
            "type": self.type,
            "checkbox": self.checked,
        }
        if self.id is not None:
            result["id"] = self.id
        return {self.name: result}
