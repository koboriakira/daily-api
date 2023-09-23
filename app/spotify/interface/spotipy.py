from app.spotify.interface.track_translator import TrackTranslator
from app.domain.spotify.track import Track
from app.util.cache import Cache
from app.util.global_ip_address import GlobalIpAddress
from app.util.get_logger import get_logger
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import Optional

logger = get_logger(__name__)


class Spotipy:

    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    SCOPE = 'user-library-read,user-top-read,user-read-currently-playing'

    def __init__(self, sp: spotipy.Spotify):
        self.sp = sp

    @classmethod
    def get_instance(cls, access_token: Optional[str] = None) -> 'Spotipy':
        token_info = cls.__read_access_token_info()
        if token_info is not None and 'access_token' in token_info:
            # アクセストークンが指定されていれば使う
            sp = spotipy.Spotify(auth=token_info['access_token'])
            return cls(sp)
        # なければリフレッシュトークン経由で取得する
        access_token = cls.__get_access_token_from_refresh_token()
        sp = spotipy.Spotify(auth=access_token)
        return cls(sp)

    def current_user_recently_played(self) -> list:
        raise NotImplementedError()

    def get_track(self, track_id: str) -> Optional[Track]:
        track_entity = self.sp.track(track_id=track_id)
        logger.debug(track_entity)
        if track_entity is None:
            return None
        return TrackTranslator.from_entity(track_entity)

    def get_playing(self) -> Optional[Track]:
        playing_track = self.sp.current_user_playing_track()
        if playing_track is None:
            return None
        logger.debug(playing_track)
        return TrackTranslator.from_entity(playing_track["item"])

    def get_album(self, album_id: str):
        raise NotImplementedError()

    @classmethod
    def get_auth_url(cls) -> str:
        """ ユーザーをSpotifyの認証ページを生成する """
        sp_oauth = cls.__get_spotify_oauth()
        auth_url = sp_oauth.get_authorize_url()
        logger.debug(auth_url)
        return auth_url

    @classmethod
    def authorize(cls, code: str):
        sp_oauth = cls.__get_spotify_oauth()
        token_info = sp_oauth.get_access_token(code)
        cls.__write_access_token_info(token_info)
        return token_info

    @classmethod
    def __get_access_token_from_refresh_token(cls) -> str:
        token_info = cls.__read_access_token_info()
        sp_oauth = cls.__get_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        cls.__write_access_token_info(token_info)
        return token_info['access_token']

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
        path = "spotify/access_token/callback"
        if os.getenv('ENVIRONMENT') == "development":
            return f"http://localhost:5023/{path}"
        else:
            return f"http://{GlobalIpAddress.get()}/{path}"

    # def recommend(self, track_id: str):
    #     recommendations = self.sp.recommendations(seed_tracks=[track_id])
    #     tracks = recommendations["tracks"]
    #     for track in tracks:
    #         # まだ保存していない曲を返すルールを追加
    #         track_id = track["id"]
    #         contain_result = self.sp.current_user_saved_tracks_contains(tracks=[
    #             track_id])
    #         is_contain = contain_result[0]
    #         if not is_contain:
    #             track_model = Track.from_dict(track)
    #             print(track_model)
    #             return TrackConverter.from_track_model(track_model)
    #     # 見つからなかった場合は、とりあえず最初の曲を返す
    #     return TrackConverter.from_track_model(Track.from_dict(tracks[0]))
