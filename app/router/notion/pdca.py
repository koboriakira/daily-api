from app.router.notion.model.project_model import Project, convert_to_project_model
from app.router.notion.model.book_model import Book, convert_to_book_model
from app.domain.notion.goal_type import GoalType
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
    projects = convert_to_project_model(entities)

    # 更新日時がdate以降のものを抽出
    projects = [
        project for project in projects if project.updated_at.date() >= date]
    return projects


@ router.get("/reading", response_model=list[Book])
async def aws_saa(date: Optional[DateObject]):
    """ 読書の目標をふりかえれるための情報を提供する """
    entities = NotionClient().retrieve_books()
    print(entities)
    books = convert_to_book_model(entities)

    # 更新日がdate以降のものを抽出
    books = [
        book for book in books if book.updated_at.date() >= date]

    # 更新日と登録日が同じものを省く
    books = [book for book in books if book.updated_at.date() !=
             book.created_at.date()]
    return books
