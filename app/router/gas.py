from fastapi import APIRouter
from app.line.line_client import LineClientFactory
from pydantic import BaseModel
from datetime import date as DateObject
from datetime import datetime as DateTimeObject
from datetime import timedelta
import requests
import os
import json

GAS_CALENDAR_API_URI = os.environ.get("GAS_CALENDAR_API_URI")

router = APIRouter()
line_client = LineClientFactory.get_instance()


class Date(BaseModel):
    value: DateObject


@router.get("/calendar/{date}", response_model=list[dict])
def get_calendar(date: DateObject):
    # ex. /calendar/2023-08-28
    url = f"{GAS_CALENDAR_API_URI}?date={date}"
    response = requests.get(url)
    data = json.loads(response.text)

    def convert(schedule: dict) -> dict:
        start = DateTimeObject.fromisoformat(
            schedule["start"]) + timedelta(hours=9)
        end = DateTimeObject.fromisoformat(
            schedule["end"]) + timedelta(hours=9)
        return {
            "start": start.isoformat(),
            "end": end.isoformat(),
            "title": schedule["title"],
        }

    return [convert(schedule) for schedule in data]
