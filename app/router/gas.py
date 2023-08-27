from fastapi import APIRouter
from app.line.line_client import LineClientFactory
from pydantic import BaseModel
from datetime import date as DateObject
import requests
import os
import json

GAS_CALENDAR_API_URI = os.environ.get("GAS_CALENDAR_API_URI")

router = APIRouter()
line_client = LineClientFactory.get_instance()


class Date(BaseModel):
    value: DateObject


@router.get("/calendar/{date}", response_model=list[dict])
def message_push(date: DateObject):
    # ex. /calendar/2023-08-28
    url = f"{GAS_CALENDAR_API_URI}?date={date}"

    response = requests.get(url)
    return json.loads(response.text)
