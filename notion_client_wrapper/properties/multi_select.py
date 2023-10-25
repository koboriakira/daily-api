from dataclasses import dataclass
from app.domain.notion.properties.property import Property
from typing import Optional


@dataclass(frozen=True)
class MultiSelectElement(Property):
    id: str
    name: str
    color: str

    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color
        }


@dataclass
class MultiSelect(Property):
    values: list[MultiSelectElement]
    type: str = "multi_select"

    def __init__(self,
                 name: str,
                 values: list[dict[str, str]],
                 id: Optional[str] = None,):
        self.name = name
        self.values = values
        self.id = id

    @ staticmethod
    def of(name: str, param: dict) -> "MultiSelect":
        multi_select = [
            MultiSelectElement(
                id=element["id"],
                name=element["name"],
                color=element["color"]
            ) for element in param["multi_select"]]

        return MultiSelect(
            name=name,
            values=multi_select,
            id=param["id"],
        )

    def __dict__(self):
        result = [e.__dict__() for e in self.values]
        return {self.name: result}
