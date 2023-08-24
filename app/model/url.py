from pydantic import BaseModel, Field


class NotionUrl(BaseModel):
    url: str = Field(..., title="NotionのURL",
                     regex=r"^https://www.notion.so/.*")
    block_id: str = Field(..., title="NotionのブロックID", regex=r"^[\w-]*")
