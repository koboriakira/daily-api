from enum import Enum
from notion_client_wrapper.properties import Select


class ProwrestlingOrganization(Enum):
    TJPW = "東京女子"

    def to_select(self) -> Select:
        return Select(
            name="団体",
            selected_name=self.value,
            selected_id=self.id,
            selected_color=self.color
        )

    @staticmethod
    def from_name(name: str) -> "ProwrestlingOrganization":
        match name:
            case "東京女子":
                return ProwrestlingOrganization.TJPW
            case _:
                raise ValueError(f"Invalid value: {name}")

    @property
    def id(self):
        match self:
            case ProwrestlingOrganization.TJPW:
                return ">a]c"
            case _:
                raise ValueError(f"Invalid value: {self}")

    @property
    def color(self):
        match self:
            case ProwrestlingOrganization.TJPW:
                return "red"
            case _:
                raise ValueError(f"Invalid value: {self}")
