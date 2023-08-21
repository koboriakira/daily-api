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
