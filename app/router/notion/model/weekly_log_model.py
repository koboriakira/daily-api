from pydantic import BaseModel, Field


class WeeklyLogModel(BaseModel):
    title: str = Field(..., title="タイトル")
    id: str = Field(..., title="ID",
                    regex=r"^\w{8}-?\w{4}-?\w{4}-?\w{4}-?\w{12}")
    url: str = Field(..., title="NotionのURL",
                     regex=r"^https://www.notion.so/.*")
    goal: str = Field(..., title="目標")
