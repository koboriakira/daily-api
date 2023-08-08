from app.domain.spotify.item import Items, Track
from app.util.cache import Cache
from app.util.global_ip_address import GlobalIpAddress
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import Optional


class SpotifyController:

    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    SCOPE = 'user-library-read'

    def __init__(self, sp: spotipy.Spotify):
        self.sp = sp

    @ classmethod
    def get_instance(cls, access_token: Optional[str] = None) -> 'SpotifyController':
        if access_token is not None:
            # アクセストークンが指定されていれば使う
            sp = spotipy.Spotify(auth=access_token)
            return cls(sp)
        # なければリフレッシュトークン経由で取得する
        token_info = cls.__read_access_token_info()
        print(token_info)
        sp_oauth = cls.__get_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        sp = spotipy.Spotify(auth=token_info['access_token'])
        return cls(sp)

    def current_user_recently_played(self):
        token_info = self.__read_access_token_info()
        sp = spotipy.Spotify(auth=token_info['access_token'])
        recently_played = sp.current_user_recently_played()

        items = Items.from_dict_list(values=recently_played['items'])

        external_urls = list(set(
            map(lambda item: item.context["external_urls"]["spotify"], items.values)))

        return ",".join(external_urls)

    def get_track(self, track_id: str) -> Track:
        token_info = self.__read_access_token_info()
        sp = spotipy.Spotify(auth=token_info['access_token'])
        track_entity = sp.track(track_id=track_id)
        track = Track.from_dict(track_entity)
        # TODO: trackタイプかalbumタイプかを判定する
        return track

    @classmethod
    def get_recently_played_url(cls) -> str:
        """ ユーザーをSpotifyの認証ページを生成する """
        sp_oauth = cls.__get_spotify_oauth()
        auth_url = sp_oauth.get_authorize_url()
        print(auth_url)
        return auth_url

    @classmethod
    def authorize(cls, code: str):
        sp_oauth = cls.__get_spotify_oauth()
        token_info = sp_oauth.get_access_token(code)
        cls.__write_access_token_info(token_info)
        return token_info

    @classmethod
    def __write_access_token_info(self, access_token_info: dict) -> None:
        Cache.write('spotify_access_token_info', access_token_info)

    @classmethod
    def __read_access_token_info(self) -> None:
        return Cache.read('spotify_access_token_info')

    @classmethod
    def __get_spotify_oauth(cls):
        return SpotifyOAuth(client_id=cls.CLIENT_ID,
                            client_secret=cls.CLIENT_SECRET,
                            redirect_uri=cls.get_callback_url(),
                            scope=cls.SCOPE)

    @classmethod
    def get_callback_url(cls) -> str:
        """ 認証のコールバック用URLを取得 """
        # NOTE: 返却値が変わる場合は、Spotifyのアプリ設定画面のRedirect URIsも変更する必要がある
        path = "spotify/access_token_callback"
        if os.getenv('ENVIRONMENT') == "development":
            return f"http://localhost:5023/{path}"
        else:
            return f"http://{GlobalIpAddress.get()}/{path}"


if __name__ == "__main__":
    SpotifyController.get_recently_played_url()
