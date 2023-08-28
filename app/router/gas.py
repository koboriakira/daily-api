from fastapi import APIRouter
from app.line.line_client import LineClientFactory
from datetime import date as DateObject
from datetime import datetime as DateTimeObject
from datetime import timedelta
import requests
import os
import json

GAS_CALENDAR_API_URI = os.environ.get("GAS_CALENDAR_API_URI")

router = APIRouter()
line_client = LineClientFactory.get_instance()


@router.get("/calendar/", response_model=list[dict])
def get_calendar(start_date: DateObject, end_date: DateObject):

    # UTC+00:00で検索してしまうため、ちょっと広めに検索して、あとで絞る
    replaced_start_date = start_date - timedelta(days=1)

    url = f"{GAS_CALENDAR_API_URI}?startDate={replaced_start_date}&endDate={end_date}"
    response = requests.get(url)
    data = json.loads(response.text)

    def convert(data: list[dict], start_date: DateTimeObject, end_date: DateTimeObject):
        for schedule in data:
            start = DateTimeObject.fromisoformat(
                schedule["start"]) + timedelta(hours=9)
            end = DateTimeObject.fromisoformat(
                schedule["end"]) + timedelta(hours=9)
            if start_date.timestamp() <= start.timestamp() and end.timestamp() <= end_date.timestamp():
                yield {
                    "start": start.isoformat(),
                    "end": end.isoformat(),
                    "title": schedule["title"],
                }

    return list(convert(data,
                        DateTimeObject(start_date.year,
                                       start_date.month, start_date.day),
                        DateTimeObject(end_date.year, end_date.month, end_date.day)))
