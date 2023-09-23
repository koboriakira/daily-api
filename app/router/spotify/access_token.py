from fastapi import Request, Response, HTTPException
from fastapi import APIRouter
from app.util.get_logger import get_logger
from app.spotify.controller.spotify_controller import SpotifyController

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", status_code=303)
def get_access_token():
    """ Spotifyの認証ページにリダイレクト """
    auth_url = SpotifyController.get_auth_url()
    logger.debug(auth_url)
    return Response(headers={"Location": auth_url}, status_code=303)


@router.get("/callback", response_model=dict)
async def callback(request: Request):
    """
    Spotifyの認証後のコールバック用URL。
    直接呼び出すことはありません。
    """
    # 認証コードを取得
    code = request.query_params.get('code')
    if code is None:
        raise HTTPException(status_code=400, detail="code is not found.")

    response = SpotifyController.authorize(code=code)
    logger.debug(response)
    if "access_token" not in response:
        raise HTTPException(status_code=401, detail="Authorization failed.")
    return {
        "message": "Authorization succeeded."
    }
