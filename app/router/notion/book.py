from app.router.notion.model.book_model import Book, convert_to_book_model
from fastapi import APIRouter
from app.interface.notion_client import NotionClient

router = APIRouter()


@ router.get("/", response_model=list[Book])
async def get_books():
    """ 音楽を取得 """
    entities = NotionClient().retrieve_books()
    print(entities)
    return convert_to_book_model(entities)
