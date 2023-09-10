from app.router.notion.model.project_model import Project
from app.domain.notion.page.goal.goal_type import GoalType
from fastapi import APIRouter
from typing import Optional
from app.interface.notion_client import NotionClient
from datetime import date as DateObject

router = APIRouter()


@ router.get("/awssaa", response_model=list[Project])
async def aws_saa(date: Optional[DateObject]):
    """ AWS SAAの目標をふりかえれるための情報を提供する """
    entities = NotionClient().retrieve_projects(goal_id=GoalType.AWS_SAA.value)
    print(entities)
    projects = convert_to_model(entities)

    # 更新日時がdate以降のものを抽出
    projects = [
        project for project in projects if project.updated_at.date() >= date]
    return projects


def convert_to_model(entites: list[dict]) -> list[Project]:
    return [Project(**entity) for entity in entites]
