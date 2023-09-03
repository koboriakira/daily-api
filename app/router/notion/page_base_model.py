from pydantic import BaseModel, Field
from datetime import datetime as DatetimeObject


class PageBaseModel(BaseModel):
    title: str = Field(..., title="タイトル")
    id: str = Field(..., title="ID",
                    regex=r"^\w{8}-?\w{4}-?\w{4}-?\w{4}-?\w{12}")
    url: str = Field(..., title="NotionのURL",
                     regex=r"^https://www.notion.so/.*")
    created_at: DatetimeObject = Field(..., title="プロジェクトの最終更新日時")
    updated_at: DatetimeObject = Field(..., title="プロジェクトの作成日時")
    daily_log_id: list[str] = Field(..., title="デイリーログのIDのリスト")
