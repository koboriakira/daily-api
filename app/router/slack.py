from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
from slack_sdk import WebClient
import os

DIARY = "C05F6AASERZ"
TEST = "C05H3USHAJU"

router = APIRouter()
slack_user = WebClient(token=os.environ["SLACK_USER_TOKEN"])


class Text(BaseModel):
    content: str


@router.post("/photo", response_model=dict)
def message_push(file: UploadFile = File(...)):
    if file:
        filename = file.filename
        slack_user.files_upload_v2(
            channels=TEST,
            initial_comment="アップロードテスト",
            file=file.file,
            filename=filename,
        )
        return {"アップロードファイル名": filename}
    return {"Error": "アップロードファイルが見つかりません。"}
