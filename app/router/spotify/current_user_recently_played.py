from fastapi import APIRouter
router = APIRouter()


@router.get("/")
async def current_user_recently_played():
    raise NotImplementedError
