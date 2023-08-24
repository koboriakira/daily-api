from app.router import healthcheck
from app.router.spotify import access_token, track, current_user_recently_played
from app.router.notion import daily_log
from app.router.notion import block
from app.router import line
from fastapi import FastAPI
from fastapi import FastAPI, Request
from app.controller.spotify_controller import SpotifyController
from app.interface.notion_client import NotionClient

app = FastAPI()

app.include_router(healthcheck.router,
                   prefix="/healthcheck", tags=["healthcheck"])
app.include_router(access_token.router,
                   prefix="/spotify/access_token", tags=["spotify"])
app.include_router(track.router,
                   prefix="/spotify/track", tags=["spotify"])
app.include_router(current_user_recently_played.router,
                   prefix="/spotify/current_user_recently_played", tags=["spotify"])
app.include_router(daily_log.router,
                   prefix="/notion/daily_log", tags=["notion"])
app.include_router(block.router,
                   prefix="/notion/block", tags=["notion"])
app.include_router(line.router,
                   prefix="/line", tags=["line"])
