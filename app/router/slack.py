from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
from slack_sdk import WebClient
import shutil
import os

router = APIRouter()
slack_bot = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
slack_user = WebClient(token=os.environ["SLACK_USER_TOKEN"])


class Text(BaseModel):
    content: str


@router.post("/photo", response_model=dict)
def message_push(file: UploadFile = File(...)):
    if file:
        filename = file.filename
        # fileobj = file.file
        return {"アップロードファイル名": filename}
    return {"Error": "アップロードファイルが見つかりません。"}
