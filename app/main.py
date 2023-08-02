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


@app.get("/notion/daily_log")
async def callback(Authorization: Union[str, None] = Header(default=None)):
    AuthorizeChecker.validate(access_token=Authorization)
    notion_client = NotionClient()
    return notion_client.get_daily_log()
