from abc import ABCMeta, abstractmethod


class Property(metaclass=ABCMeta):
    id: str
    name: str
    type: str

    @abstractmethod
    def __dict__(self):
        pass


class Properties:
    values: list[Property]

    def __dict__(self):
        return {
            "properties": {
                value.name: value.__dict__() for value in self.values
            }
        }
