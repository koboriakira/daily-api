from fastapi import FastAPI, Request, Response
import requests
import base64
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib
import os

app = FastAPI()

# Spotify Developer Dashboardで取得した情報を入力します
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# ユーザーのスコープを設定します。
# 最近聴いた曲を取得するためには'user-read-recently-played'が必要です
SCOPE = 'user-read-recently-played'

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI, scope=SCOPE)


@app.get("/get_recently_played")
async def get_recently_played():
    # ユーザーをSpotifyの認証ページにリダイレクト
    auth_url = sp_oauth.get_authorize_url()
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

    return recently_played
