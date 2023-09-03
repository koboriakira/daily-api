from pydantic import BaseModel, Field


class Tag(BaseModel):
    block_id: str = Field(..., title="ブロックID",
                          regex=r"^\w{8}-?\w{4}-?\w{4}-?\w{4}-?\w{12}")
    title: str = Field(..., title="タグ名")


class Tags(BaseModel):
    tags: list[Tag] = Field(..., title="タグのリスト")
