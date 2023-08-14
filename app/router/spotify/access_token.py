from app.controller.spotify_controller import SpotifyController
from fastapi import Request, Response
from fastapi import APIRouter
router = APIRouter()


@router.get("/", status_code=303)
def get_access_token():
    """ Spotifyの認証ページにリダイレクト """
    auth_url = SpotifyController.get_auth_url()
    print(auth_url)
    return Response(headers={"Location": auth_url}, status_code=303)


@router.get("/callback", response_model=dict)
async def callback(request: Request):
    """
    Spotifyの認証後のコールバック用URL。
    直接呼び出すことはありません。
    """
    # 認証コードを取得
    code = request.query_params.get('code')
    return SpotifyController.authorize(code=code)
