from pydantic import BaseModel, Field
from fastapi import APIRouter
from typing import Optional
from app.interface.notion_client import NotionClient
from app.domain.notion.properties import Status
from datetime import datetime as DatetimeObject
from datetime import date as DateObject
from datetime import timedelta

router = APIRouter()


class ProjectStatusList:
    VALUES = ["IceBox", "Suspend", "Inbox", "Next action", "Not started",
              "In progress", "Today", "Scheduled", "Done", "Archived", "Trash"]

    ALL_VALUES = ["In progress", "Today", "Inbox", "Not started",
                  "Next action"]

    @classmethod
    def to_regex(cls) -> str:
        list = "|".join(cls.VALUES)
        return r"^(" + list + r")$"


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
    created_at: DatetimeObject = Field(..., title="プロジェクトの最終更新日時")
    updated_at: DatetimeObject = Field(..., title="プロジェクトの最終更新日時")


@router.get("/")
async def get_projects(status: Optional[str] = None):
    """ NotionのZettlekastenに新しいページを追加する """
    notion_client = NotionClient()

    status_list = _get_status_list(status)
    get_detail_flag = True if status is not None else False
    projects = notion_client.find_projects(status_list=status_list,
                                           get_detail=get_detail_flag)

    project_model_list = []
    for project in projects:
        project["created_at"] = DatetimeObject\
            .fromisoformat(project["created_at"].replace("Z", "+00:00"))\
            .astimezone() + timedelta(hours=9)
        project["updated_at"] = DatetimeObject\
            .fromisoformat(project["updated_at"].replace("Z", "+00:00"))\
            .astimezone() + timedelta(hours=9)
        task_model_list = []
        for task in project["tasks"] if "tasks" in project else []:
            print(task)
            task_model_list.append(Task(**task))
        project["tasks"] = task_model_list
        project_model_list.append(Project(**project))

    return projects


class PostProjectRequest(BaseModel):
    title: str = Field(title="プロジェクトのタイトル")
    goal: str = Field(title="プロジェクトのゴール")
    status: Optional[str] = Field(title="プロジェクトのステータス",
                                  default="Inbox",
                                  regex=ProjectStatusList.to_regex())
    start_date: Optional[DateObject] = Field(title="プロジェクトの開始日", default=None)
    end_date: Optional[DateObject] = Field(title="プロジェクトの終了日",
                                           default=None)
    remind_date: Optional[DateObject] = Field(title="プロジェクトのリマインド日",
                                              default=None)


@ router.post("/")
def post_project(request: PostProjectRequest):
    """ Notionのプロジェクトに新しいページを追加する """
    notion_client = NotionClient()
    result = notion_client.create_project(
        title=request.title,
        goal=request.goal,
        status=request.status,
        start_date=request.start_date if request.start_date else DateObject.today(),
        end_date=request.end_date,
        remind_date=request.remind_date)
    return {
        "url": result["url"],
    }


class UpdateProjectRequest(BaseModel):
    status: Optional[str] = Field(title="プロジェクトのステータス",
                                  default="Inbox",
                                  regex=ProjectStatusList.to_regex())


@ router.post("/{project_id}")
def update_project(project_id: str, request: UpdateProjectRequest):
    """ Notionのプロジェクトを更新する """
    notion_client = NotionClient()
    notion_client.update_project(project_block_id=project_id,
                                 status=request.status)
    return {
        "success": True,
    }


def _get_status_list(status_str: Optional[str]) -> list[Status]:
    if status_str is None:
        return [Status.from_status_name("ステータス", s) for s in ProjectStatusList.VALUES]
    if status_str.lower() == "all":
        return [Status.from_status_name("ステータス", s) for s in ProjectStatusList.ALL_VALUES]
    else:
        return [Status.from_status_name(
            "ステータス", s) for s in status_str.split(",")]
