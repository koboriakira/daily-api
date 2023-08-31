from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
from slack_sdk import WebClient
import os
from datetime import datetime as DatetimeObject
from datetime import timedelta
from typing import Optional

DIARY = "C05F6AASERZ"
TEST = "C05H3USHAJU"

UPLOAD_CHANNEL = TEST
NOTIFICATION_CHANNEL = "C04Q3AV4TA5"

router = APIRouter()
slack_bot = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
slack_user = WebClient(token=os.environ["SLACK_USER_TOKEN"])


class Text(BaseModel):
    content: str


@router.post("/photo", response_model=dict)
def upload_photo(file: UploadFile = File(...)):
    now = DatetimeObject.now()
    text = _get_initial_comment(now)
    thread_ts = _get_photo_thread_ts(now, text)
    text = text if thread_ts is None else ""

    if file:
        filename = file.filename
        response = slack_user.files_upload_v2(
            channels=UPLOAD_CHANNEL,
            initial_comment=text,
            file=file.file,
            filename=filename,
            thread_ts=thread_ts,
        )
        if response["ok"]:
            return {"finename": filename}
        else:
            slack_bot.chat_postMessage(
                channel=NOTIFICATION_CHANNEL,
                text=f"【写真自動アップロード】\nファイルのアップロードに失敗しました。\n```{response}```",
            )
    else:
        slack_bot.chat_postMessage(
            channel=NOTIFICATION_CHANNEL,
            text=f"【写真自動アップロード】\nアップロードファイルが見つかりません。",
        )


def _get_initial_comment(now: DatetimeObject) -> str:
    # nowが6-12時なら「朝」
    date = now.strftime("%Y年%m月%d日")
    if now.hour > 0 and now.hour <= 6:
        return f"{date} 深夜(早朝)の写真"
    if now.hour > 6 and now.hour <= 12:
        return f"{date} 朝の写真"
    elif now.hour > 12 and now.hour <= 18:
        return f"{date} 昼の写真"
    return f"{date} 夜の写真"


def _get_photo_thread_ts(now: DatetimeObject, text: str) -> Optional[str]:
    # 直近30分以内で、initial_commentが同じ投稿があるか確認
    response = slack_user.conversations_history(
        channel=UPLOAD_CHANNEL,
        limit=1,
        oldest=int((now - timedelta(minutes=120)).timestamp()),
        latest=int(now.timestamp()),
    )
    if response["ok"] and response["messages"]:
        for message in response["messages"]:
            print(message["text"])
            if message["text"] == text:
                return message["ts"]
    return None


@ router.get("/test")
def test():
    return _get_photo_thread_ts(DatetimeObject.now(), "アップロードテスト")
