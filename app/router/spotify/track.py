from app.controller.spotify_controller import SpotifyController
from fastapi import APIRouter
from app.interface.notion_client import NotionClient
from app.model.url import NotionUrl
router = APIRouter()


@router.post("/{track_id}/add_notion", response_model=NotionUrl)
async def add_track_to_notion(track_id: str):
    """
    指定されたSpotifyの曲もしくはアルバムをNotionに追加する。
    作成したページのURLを返す。
    """
    spotify_controller = SpotifyController.get_instance()
    notion_client = NotionClient()
    track = spotify_controller.get_track(track_id=track_id)
    if track is not None:
        daily_log = notion_client.get_daily_log()
        daily_log_id = daily_log.id
        url = notion_client.add_track(track=track, daily_log_id=daily_log_id)
        return NotionUrl(url=url)
    album = spotify_controller.get_album(album_id=track_id)
    if album is not None:
        daily_log = notion_client.get_daily_log()
        daily_log_id = daily_log.id
        url = notion_client.add_album(album=album, daily_log_id=daily_log_id)
        return NotionUrl(url=url)
