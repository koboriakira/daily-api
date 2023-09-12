from app.router.notion.model.project_model import Project, Task, convert_to_project_model
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


@router.get("/", response_model=list[Project])
async def get_projects(status: Optional[str] = None, remind_date: Optional[DateObject] = None):
    """ NotionのZettlekastenに新しいページを追加する """
    notion_client = NotionClient()

    status_list = _get_status_list(status)
    get_detail_flag = True if status is not None else False
    projects = notion_client.retrieve_projects(status_list=status_list,
                                               get_detail=get_detail_flag,
                                               remind_date=remind_date)
    return convert_to_project_model(projects)


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
