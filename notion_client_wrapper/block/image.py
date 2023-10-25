from app.domain.notion.block.block import Block
from dataclasses import dataclass


class Image(Block):
    image_caption: list
    image_type: str
    image_file: dict
    type: str = "image"

    def __init__(self, id: str, archived: bool, created_time: str, last_edited_time: str, has_children: bool,
                 parent: dict, image_caption: list, image_type: str, image_file: dict):
        super().__init__(id, archived, created_time, last_edited_time, has_children, parent)
        self.image_caption = image_caption
        self.image_type = image_type
        self.image_file = image_file

    @staticmethod
    def of(block: dict) -> "Image":
        image = block["image"]
        image_caption = image["caption"] if "caption" in image else []
        image_type = image["type"] if "type" in image else ""
        image_file = image["file"] if "file" in image else {}
        return Image(
            id=block["id"],
            archived=block["archived"],
            created_time=block["created_time"],
            last_edited_time=block["last_edited_time"],
            has_children=block["has_children"],
            parent=block["parent"],
            image_caption=image_caption,
            image_type=image_type,
            image_file=image_file
        )

    @property
    def type(self) -> str:
        return "image"

    def to_dict_sub(self) -> dict:
        raise NotImplementedError
