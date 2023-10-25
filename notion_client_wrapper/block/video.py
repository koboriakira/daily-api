from notion_client_wrapper.block.block import Block
from dataclasses import dataclass


class Video(Block):
    caption: list
    external_url: str
    type: str = "video"

    def __init__(self, id: str, archived: bool, created_time: str, last_edited_time: str, has_children: bool,
                 parent: dict, caption: list, external_url: str):
        super().__init__(id, archived, created_time, last_edited_time, has_children, parent)
        self.caption = caption
        self.external_url = external_url

    @staticmethod
    def of(block: dict) -> "Video":
        video = block["video"]
        video_external = video["external"] if "external" in video else {}
        return Video(
            id=block["id"],
            archived=block["archived"],
            created_time=block["created_time"],
            last_edited_time=block["last_edited_time"],
            has_children=block["has_children"],
            parent=block["parent"],
            caption=video["caption"],
            external_url=video_external["url"] if "url" in video_external else ""
        )

    @property
    def type(self) -> str:
        return "video"

    def to_dict_sub(self) -> dict:
        raise NotImplementedError
