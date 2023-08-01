from dataclasses import dataclass
from abc import ABCMeta, abstractmethod


@dataclass(frozen=True)
class Property(metaclass=ABCMeta):
    id: str
    name: str
    type: str

    @abstractmethod
    def __dict__(self):
        pass


@dataclass(frozen=True)
class Properties:
    values: list[Property]

    def __dict__(self):
        return {
            "properties": {
                value.name: value.__dict__() for value in self.values
            }
        }
