from fastapi import APIRouter
from app.line.line_client import LineClientFactory

router = APIRouter()
line_client = LineClientFactory.get_instance()


@router.post("/message", response_model=dict)
def message_push():
    return line_client.push_message("hello")
