from app.router.notion.model.page_base_model import PageBaseModel
from pydantic import BaseModel, Field
from typing import Optional


class Task(BaseModel):
    id: str = Field(..., title="タスクのID")
    title: str = Field(..., title="タスクのタイトル")
    status: str = Field(..., title="タスクのステータス")
    implementation_date: Optional[str] = Field(..., title="タスクの実施予定日",
                                               regex=r"^\d{4}-\d{2}-\d{2}$")


class Project(PageBaseModel):
    goal_id_list: list[str] = Field(..., title="目標のIDのリスト")
    status: str = Field(..., title="プロジェクトのステータス")
    tasks: Optional[list[Task]] = Field(title="タスクのリスト", default=None)


def convert_to_model(entites: list[dict]) -> list[Project]:
    return [Project(**entity) for entity in entites]
