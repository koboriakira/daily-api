from fastapi import FastAPI, Request, Response
import requests
import base64
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib
import os

# Spotify Developer Dashboardで取得した情報を入力します
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# ユーザーのスコープを設定します。
# 最近聴いた曲を取得するためには'user-read-recently-played'が必要です
SCOPE = 'user-read-recently-played'

app = FastAPI()


@app.get("/get_recently_played")
async def get_recently_played():
    # ユーザーをSpotifyの認証ページにリダイレクト
    auth_url = f'https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&scope={urllib.parse.quote(SCOPE)}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}'
    return Response(headers={"Location": auth_url}, status_code=303)


@app.get("/callback")
async def callback(request: Request):
    # 認証コードを取得
    code = request.query_params.get('code')

    # 認証コードからアクセストークンを取得
    auth_header = base64.b64encode(
        f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'Basic {auth_header}',
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }
    response = requests.post(
        'https://accounts.spotify.com/api/token', headers=headers, data=data)
    access_token = response.json().get('access_token')

    # アクセストークンを使用して最近聴いた曲の履歴を取得
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(
        'https://api.spotify.com/v1/me/player/recently-played', headers=headers)
    recently_played = response.json()

    return recently_played
