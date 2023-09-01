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
    implementation_date: Optional[str] = Field(..., title="タスクの実施予定日",
                                               regex=r"^\d{4}-\d{2}-\d{2}$")


class Project(BaseModel):
    id: str = Field(..., title="プロジェクトのID")
    title: str = Field(..., title="プロジェクトのタイトル")
    url: str = Field(..., title="プロジェクトのURL",
                     regex=r"^https://www.notion.so/.*")
    status: str = Field(..., title="プロジェクトのステータス")
    tasks: list[Task] = Field(..., title="プロジェクトのタスク")


@router.get("/")
async def get_projects(status: str):
    """ NotionのZettlekastenに新しいページを追加する """
    notion_client = NotionClient()

    status_list = _get_status_list(status)
    projects = notion_client.find_projects(status_list=status_list)

    project_model_list = []
    for project in projects:
        task_model_list = []
        for task in project["tasks"]:
            print(task)
            task_model_list.append(Task(**task))
        project["tasks"] = task_model_list
        project_model_list.append(Project(**project))

    return projects


def _get_status_list(status_str: str) -> list[Status]:
    if status_str.lower() == "all":
        return [
            Status.from_status_name("ステータス", "In Progress"),
            Status.from_status_name("ステータス", "Today"),
            Status.from_status_name("ステータス", "Inbox"),
            Status.from_status_name("ステータス", "Not started"),
            Status.from_status_name("ステータス", "Next action"),
        ]
    else:
        return [Status.from_status_name(
            "ステータス", s) for s in status_str.split(",")]
