from fastapi import FastAPI, Request, Response
from app.controller.spotify_controller import SpotifyController

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
