from app.model.spotify.track import RecentlyPlayedTrackConverter, TrackConverter
from app.model.spotify.track import RecentlyPlayedTrack
from app.domain.spotify.item import Items
from app.domain.spotify.track import Track
from app.domain.spotify.album import Album
from app.util.cache import Cache
from app.util.global_ip_address import GlobalIpAddress
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import Optional


class SpotifyController:

    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    SCOPE = 'user-library-read,user-top-read'

    def __init__(self, sp: spotipy.Spotify):
        self.sp = sp

    @classmethod
    def get_instance(cls, access_token: Optional[str] = None) -> 'SpotifyController':
        if access_token is not None:
            # アクセストークンが指定されていれば使う
            sp = spotipy.Spotify(auth=access_token)
            return cls(sp)
        # なければリフレッシュトークン経由で取得する
        access_token = cls.__get_access_token_from_refresh_token()
        sp = spotipy.Spotify(auth=access_token)
        return cls(sp)

    def current_user_recently_played(self) -> list[RecentlyPlayedTrack]:
        token_info = self.__read_access_token_info()
        sp = spotipy.Spotify(auth=token_info['access_token'])
        recently_played = sp.current_user_recently_played()

        items = Items.from_dict_list(values=recently_played['items'])
        track_entities = list(set(
            map(lambda item: RecentlyPlayedTrackConverter.from_item(item), items.values)))

        return track_entities

    def get_track(self, track_id: str) -> Optional[Track]:
        try:
            token_info = self.__read_access_token_info()
            sp = spotipy.Spotify(auth=token_info['access_token'])
            track_entity = sp.track(track_id=track_id)
            track = Track.from_dict(track_entity)
            return track
        except Exception as e:
            return None

    def get_album(self, album_id: str) -> Album:
        try:
            token_info = self.__read_access_token_info()
            sp = spotipy.Spotify(auth=token_info['access_token'])
            album_entity = sp.album(album_id=album_id)
            return Album.from_dict(album_entity)
        except Exception as e:
            print(e)
            return None

    @classmethod
    def get_auth_url(cls) -> str:
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

    def recommend(self, track_id: str):
        token_info = self.__read_access_token_info()
        sp = spotipy.Spotify(auth=token_info['access_token'])
        recommendations = sp.recommendations(seed_tracks=[track_id])
        tracks = recommendations["tracks"]
        for track in tracks:
            # まだ保存していない曲を返すルール
            track_id = track["id"]
            contain_result = sp.current_user_saved_tracks_contains(tracks=[
                                                                   track_id])
            is_contain = contain_result[0]
            if not is_contain:
                track_model = Track.from_dict(track)
                print(track_model)
                return TrackConverter.from_track_model(track_model)
        # 見つからなかった場合は、とりあえず最初の曲を返す
        return TrackConverter.from_track_model(Track.from_dict(tracks[0]))
