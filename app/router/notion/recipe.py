from pydantic import BaseModel, Field
from fastapi import APIRouter
from typing import Optional
from app.interface.notion_client import NotionClient
from app.domain.notion.properties import Status
from app.router.notion.model.page_base_model import PageBaseModel


router = APIRouter()


class Recipe(PageBaseModel):
    ingredients: list[str] = Field(..., title="材料")
    meal_categories: list[str] = Field(..., title="カテゴリ")
    status: str = Field(..., title="プロジェクトのステータス")


@router.get("/")
async def get_recipes(detail: bool = False):
    """ NotionのRecipeを取得する """
    notion_client = NotionClient()
    entities = notion_client.retrieve_recipes(detail=detail)
    return convert_to_model(entities)


def convert_to_model(entites: list[dict]) -> list[Recipe]:
    return [Recipe(**entity) for entity in entites]
