from fastapi import APIRouter
from app.line.line_client import LineClientFactory
from pydantic import BaseModel

router = APIRouter()
line_client = LineClientFactory.get_instance()


class Text(BaseModel):
    content: str


@router.post("/message", response_model=dict)
def message_push(text: Text):
    return line_client.push_message(text.content)


@router.post("/message/photo",
             response_model=dict,
             description="今日撮影した写真があることをLINE通知します")
def message_push_photo():
    return line_client.push_message("今日撮影した写真があるので管理しましょう！")
