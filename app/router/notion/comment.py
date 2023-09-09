from pydantic import BaseModel, Field
from fastapi import APIRouter
from app.interface.notion_client import NotionClient

router = APIRouter()


class PostCommentRequest(BaseModel):
    """ コメントを投稿するリクエスト """
    page_id: str = Field(..., title="ページID")
    text: str = Field(..., title="コメント")


@ router.post("/", response_model=dict)
async def post_comment(request: PostCommentRequest):
    """ 音楽を取得 """
    NotionClient().append_comment(page_id=request.page_id,
                                  text=request.text)
    return {
        "success": True,
    }
