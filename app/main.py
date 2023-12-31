from fastapi import FastAPI
from app.router import healthcheck
from app.router.spotify import access_token, track, current_user_recently_played
from app.router.notion import daily_log, block, zettlekasten, project, recipe, music, prowrestling, book, webclip, comment, weekly_log, pdca
from app.router import line
from app.router import gas
from app.router import slack

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
app.include_router(weekly_log.router,
                   prefix="/notion/weekly_log", tags=["notion"])
app.include_router(zettlekasten.router,
                   prefix="/notion/zettlekasten", tags=["notion"])
app.include_router(project.router,
                   prefix="/notion/project", tags=["notion"])
app.include_router(recipe.router,
                   prefix="/notion/recipe", tags=["notion"])
app.include_router(music.router,
                   prefix="/notion/music", tags=["notion"])
app.include_router(prowrestling.router,
                   prefix="/notion/prowrestling", tags=["notion"])
app.include_router(book.router,
                   prefix="/notion/book", tags=["notion"])
app.include_router(webclip.router,
                   prefix="/notion/webclip", tags=["notion"])
app.include_router(block.router,
                   prefix="/notion/block", tags=["notion"])
app.include_router(comment.router,
                   prefix="/notion/comment", tags=["notion"])
app.include_router(pdca.router,
                   prefix="/notion/pdca", tags=["notion"])
app.include_router(line.router,
                   prefix="/line", tags=["line"])
app.include_router(gas.router,
                   prefix="/gas", tags=["gas"])
app.include_router(slack.router,
                   prefix="/slack", tags=["slack"])
