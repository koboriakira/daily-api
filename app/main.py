from fastapi import FastAPI, Request, Response
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from app.domain.item import Items
import random
import urllib

app = FastAPI()

# Spotify Developer Dashboardで取得した情報を入力します
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
IP_ADDRESS = os.getenv('GLOBAL_IP_ADDRESS')
PORT = 5023
REDIRECT_URI = f'http://{IP_ADDRESS}:{PORT}/callback'

# ユーザーのスコープを設定します。
# 最近聴いた曲を取得するためには'user-read-recently-played'が必要です
SCOPE = 'user-read-recently-played'

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=SCOPE)


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/get_recently_played")
async def get_recently_played():
    # ユーザーをSpotifyの認証ページにリダイレクト
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return Response(headers={"Location": auth_url}, status_code=303)


@app.get("/callback")
async def callback(request: Request):
    # 認証コードを取得
    code = request.query_params.get('code')

    # 認証コードからアクセストークンを取得
    token_info = sp_oauth.get_access_token(code)

    # アクセストークンを使用して最近聴いた曲の履歴を取得
    sp = spotipy.Spotify(auth=token_info['access_token'])
    recently_played = sp.current_user_recently_played()

    items = Items.from_dict_list(values=recently_played['items'])

    external_urls = list(set(
        map(lambda item: item.context["external_urls"]["spotify"], items.values)))

    return ",".join(external_urls)
