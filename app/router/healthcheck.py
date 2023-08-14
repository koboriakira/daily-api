from fastapi import APIRouter, HTTPException, Depends
router = APIRouter()


@router.get("/", response_model=str)
def healthcheck():
    return "Healthy"
