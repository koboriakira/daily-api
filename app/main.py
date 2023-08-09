from app.domain.notion.block.rich_text import RichText, RichTextBuilder
from app.domain.notion.block import BlockFactory, Block, Paragraph
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import FastAPI, Request, Response, Header
from app.controller.spotify_controller import SpotifyController
from app.interface.notion_client import NotionClient
from app.util.authorize_checker import AuthorizeChecker
from typing import Union

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/spotify/access_token")
async def get_recently_played():
    # ユーザーをSpotifyの認証ページにリダイレクト
    auth_url = SpotifyController.get_recently_played_url()
    print(auth_url)
    return Response(headers={"Location": auth_url}, status_code=303)


@app.get("/spotify/access_token_callback")
async def callback(request: Request):
    # 認証コードを取得
    code = request.query_params.get('code')
    return SpotifyController.authorize(code=code)


@app.get("/spotify/current_user_recently_played")
async def current_user_recently_played(request: Request):
    spotify_controller = SpotifyController.get_instance()
    result = spotify_controller.current_user_recently_played()
    return result


@app.post("/spotify/{track_id}/add_notion")
async def spotify_add_notion(track_id: str):
    spotify_controller = SpotifyController.get_instance()
    notion_client = NotionClient()
    track = spotify_controller.get_track(track_id=track_id)
    if track is not None:
        daily_log = notion_client.get_daily_log()
        daily_log_id = daily_log.id
        url = notion_client.add_track(track=track, daily_log_id=daily_log_id)
        return url
    album = spotify_controller.get_album(album_id=track_id)
    if album is not None:
        daily_log = notion_client.get_daily_log()
        daily_log_id = daily_log.id
        url = notion_client.add_album(album=album, daily_log_id=daily_log_id)
        return url


class Text(BaseModel):
    content: list[str]


@app.post("/notion/add_daily_log")
async def add_text_daily_log(text: Text):
    notion_client = NotionClient()
    for text_content in text.content:
        rich_text = RichTextBuilder.get_instance().add_text(text_content).build()
        paragraph = Paragraph.from_rich_text(rich_text=rich_text)
        notion_client.add_daily_log(block=paragraph)


@ app.get("/notion/daily_log")
async def callback(Authorization: Union[str, None] = Header(default=None)):
    AuthorizeChecker.validate(access_token=Authorization)
    notion_client = NotionClient()
    return notion_client.get_daily_log()
