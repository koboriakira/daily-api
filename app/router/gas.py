from fastapi import APIRouter
from app.line.line_client import LineClientFactory
from datetime import date as DateObject
from datetime import datetime as DateTimeObject
from datetime import time as TimeObject
from datetime import timedelta
import requests
import os
import json
import yaml
from pydantic import BaseModel
from typing import Optional
from app.util.get_logger import get_logger
import re

logger = get_logger(__name__)

GAS_DEPLOY_ID = os.environ.get("GAS_DEPLOY_ID")
GAS_CALENDAR_API_URI = f"https://script.google.com/macros/s/{GAS_DEPLOY_ID}/exec"

router = APIRouter()
line_client = LineClientFactory.get_instance()


@router.get("/calendar/", response_model=list[dict])
def get_calendar(start_date: DateObject, end_date: DateObject):

    # UTC+00:00で検索してしまうため、ちょっと広めに検索して、あとで絞る
    replaced_start_date = start_date - timedelta(days=1)

    url = f"{GAS_CALENDAR_API_URI}?startDate={replaced_start_date}&endDate={end_date}"
    response = requests.get(url)
    # \xa0が入っているので、置換する
    data = json.loads(response.text.replace("\xa0", " "))

    def read_yaml(content: str) -> dict:
        return yaml.safe_load(content)

    def convert(data: list[dict], start_date: DateTimeObject, end_date: DateTimeObject):
        for schedule in data:
            start = DateTimeObject.fromisoformat(
                schedule["start"]) + timedelta(hours=9)
            end = DateTimeObject.fromisoformat(
                schedule["end"]) + timedelta(hours=9)
            description = schedule["description"] if "description" in schedule else ""
            try:
                # <br>タグは改行に置換する
                description = description.replace("<br>", "\n")
                # そのほかのHTMLタグはすべて置換する
                description = re.sub(r"<[^>]*?>", "", description)
                description = read_yaml(description)
            except:
                print("yaml parse error")
                print(description)
                description = None
            if start_date.timestamp() <= start.timestamp() and end.timestamp() <= end_date.timestamp():
                yield {
                    "category": schedule["category"],
                    "start": start.strftime("%Y-%m-%d %H:%M:%S+09:00"),
                    "end": end.strftime("%Y-%m-%d %H:%M:%S+09:00"),
                    "title": schedule["title"],
                    "detail": description,
                }

    start_date = DateTimeObject.combine(start_date, TimeObject(0, 0, 0))
    end_date = DateTimeObject.combine(end_date, TimeObject(23, 59, 59))
    return list(convert(data,
                        start_date,
                        end_date))


class PostCalendarRequest(BaseModel):
    category: str
    start: DateTimeObject
    end: DateTimeObject
    title: str
    detail: str


@ router.post("/calendar/")
def post_calendar(request: PostCalendarRequest):
    data = {
        "category": request.category,
        "startTime": request.start.isoformat(),
        "endTime": request.end.isoformat(),
        "title": request.title,
        "description": request.detail,
    }
    response = requests.post(GAS_CALENDAR_API_URI, json=data)
    return response.text


@ router.delete("/calendar/")
def delete_calendar(date: DateObject, category: str, title: str):
    start_datetime = DateTimeObject.combine(
        date, TimeObject(0, 0))
    end_datetime = DateTimeObject.combine(
        date, TimeObject(23, 59))

    data = {
        "mode": "delete",
        "title": title,
        "startTime": start_datetime.strftime("%Y-%m-%dT%H:%M:%S+09:00"),
        "endTime": end_datetime.strftime("%Y-%m-%dT%H:%M:%S+09:00"),
        "category": category
    }
    logger.debug(json.dumps(data, ensure_ascii=False))
    logger.debug(GAS_CALENDAR_API_URI, data)
    response = requests.post(GAS_CALENDAR_API_URI, json=data)
    return response.text
