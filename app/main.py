from fastapi import FastAPI
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify Developer Dashboardで取得した情報を入力します
CLIENT_ID = 'your-spotify-client-id'
CLIENT_SECRET = 'your-spotify-client-secret'

# 'urn:ietf:wg:oauth:2.0:oob'をリダイレクトURIとして設定します
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# ユーザーのスコープを設定します。最近聴いた曲を取得するために'user-read-recently-played'が必要です
SCOPE = 'user-read-recently-played'

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/access_token")
async def access_token():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=REDIRECT_URI,
                                                scope=SCOPE))

    # 最近聴いた曲を取得します
    results = sp.current_user_recently_played()

    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])
