from fastapi import APIRouter, HTTPException
from app.line.line_client import LineClientFactory
from pydantic import BaseModel
from typing import Any, Optional

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


class Message(BaseModel):
    type: str  # message, audio, location
    id: str
    text: Optional[str] = None # messageのとき
    duration: Optional[int] = None # audioのとき
    contentProvider: Optional[dict] = None  # audioのとき。ある場合は{"type": "line"}のはず
    latitude: Optional[float] = None  # locationのとき
    longitude: Optional[float] = None  # locationのとき
    address: Optional[str] = None  # locationのとき


class DeliveryContext(BaseModel):
    isRedelivery: bool  # 再送信かどうか


class Source(BaseModel):
    type: str
    userId: str
    groupId: Optional[str] = None
    roomId: Optional[str] = None


class Event(BaseModel):
    type: str
    message: Message
    webhookEventId: str
    deliveryContext: DeliveryContext
    timestamp: int
    source: Source
    replyToken: str
    mode: str


class LineWebhookRequest(BaseModel):
    destination: str
    events: list[Event]


@router.post("/webhook/")
def message_push(request: LineWebhookRequest | Any):
    print(request)
    if not isinstance(request, LineWebhookRequest):
        raise HTTPException(status_code=400, detail="Invalid request")
    return request
