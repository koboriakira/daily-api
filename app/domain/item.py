from dataclasses import dataclass
from app.domain.track import Track


@dataclass(frozen=True)
class Item:
    track: Track
    played_at: str
    context: dict

    @staticmethod
    def from_dict(obj: dict) -> 'Item':
        track = Track.from_dict(obj["track"])
        played_at = obj["played_at"]
        context = obj["context"]
        return Item(track, played_at, context)


@dataclass(frozen=True)
class Items:
    values: list[Item]

    @staticmethod
    def from_dict_list(values: list[dict]) -> 'Items':
        return Items(values=[Item.from_dict(item) for item in values])
