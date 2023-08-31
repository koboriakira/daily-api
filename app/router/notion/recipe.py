from pydantic import BaseModel, Field
from fastapi import APIRouter
from typing import Optional
from app.interface.notion_client import NotionClient
from app.domain.notion.properties import Status


router = APIRouter()


class Task(BaseModel):
    id: str = Field(..., title="タスクのID")
    title: str = Field(..., title="タスクのタイトル")
    status: str = Field(..., title="タスクのステータス")
    date: Optional[str] = Field(..., title="タスクの実施予定日",
                                regex=r"^\d{4}-\d{2}-\d{2}$")


class Project(BaseModel):
    id: str = Field(..., title="プロジェクトのID")
    title: str = Field(..., title="プロジェクトのタイトル")
    url: str = Field(..., title="プロジェクトのURL",
                     regex=r"^https://www.notion.so/.*")
    status: str = Field(..., title="プロジェクトのステータス")
    tasks: list[Task] = Field(..., title="プロジェクトのタスク")


@router.get("/")
async def get_recipes(detail: bool = False):
    """ NotionのRecipeを取得する """
    notion_client = NotionClient()

    recipes = notion_client.find_recipes(detail=detail)

    # project_model_list = []
    # for project in projects:
    #     task_model_list = []
    #     for task in project["tasks"]:
    #         print(task)
    #         task_model_list.append(Task(**task))
    #     project["tasks"] = task_model_list
    #     project_model_list.append(Project(**project))

    return recipes
