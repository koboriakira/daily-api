from dataclasses import dataclass
from typing import Optional, Any


@dataclass(frozen=True)
class Album:
    album_type: str
    artists: list
    available_markets: list
    external_ids: dict
    external_urls: dict
    genres: list
    href: str
    id: str
    images: list[dict]
    label: str
    name: str
    popularity: int
    release_date: str
    type: str
    uri: str

    @staticmethod
    def from_dict(obj: dict) -> 'Album':
        album_type = obj.get("album_type")
        artists = obj.get("artists")
        available_markets = obj.get("available_markets")
        external_ids = obj.get("external_ids")
        external_urls = obj.get("external_urls")
        genres = obj.get("genres")
        href = obj.get("href")
        id = obj.get("id")
        images = obj.get("images")
        label = obj.get("label")
        name = obj.get("name")
        popularity = obj.get("popularity")
        release_date = obj.get("release_date")
        type = obj.get("type")
        uri = obj.get("uri")
        return Album(album_type, artists, available_markets, external_ids, external_urls, genres, href, id, images,
                     label, name, popularity, release_date, type, uri)
