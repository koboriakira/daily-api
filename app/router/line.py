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


@router.post("/message", response_model=dict)
def message_push(text: Text):
    return line_client.push_message(text.content)


class Action(BaseModel):
    label: str
    text: str
    type = "message"

    def to_dict(self):
        return {
            "type": self.type,
            "label": self.label,
            "text": self.text
        }


class ConfirmTemplateRequest(BaseModel):
    text: str
    actions: list[Action]
    type = "confirm"

    def to_dict(self):
        return {
            "type": self.type,
            "text": self.text,
            "actions": [action.to_dict() for action in self.actions]
        }


@router.post("/message/confirm_template", response_model=dict)
def message_push(request: ConfirmTemplateRequest):
    template = request.to_dict()
    print(template)
    line_client.push_confirm_template(template)
    return {
        "success": True
    }


@router.post("/message/photo",
             response_model=dict,
             description="今日撮影した写真があることをLINE通知します")
def message_push_photo():
    return line_client.push_message("今日撮影した写真があるので管理しましょう！")


class Message(BaseModel):
    type: str  # message, audio, location
    id: str
    text: Optional[str] = None  # messageのとき
    duration: Optional[int] = None  # audioのとき
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

    import os
    import requests
    import json
    channel_access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
    get_content_url = "https://api-data.line.me/v2/bot/message/{messageId}/content"
    for event in request.events:
        if event.type == "message":
            if event.message.type == "audio":
                # 画像の場合
                response = requests.get(
                    get_content_url.format(messageId=event.message.id),
                    headers={"Authorization": f"Bearer {channel_access_token}"}
                )
                # コンテンツのバイナリデータ
                content = response.content

                # バイナリデータを保存
                with open("audio.m4a", "wb") as f:
                    f.write(content)

                with open("audio.wav", "wb") as f:
                    f.write(content)

    return request
