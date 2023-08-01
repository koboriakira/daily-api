import os
from notion_client import Client
from app.domain.notion.properties.date import Date
from app.domain.notion.properties.property import Properties
from app.domain.notion.daily_log import DailyLog
from datetime import datetime


class NotionClient:
    def __init__(self):
        self.client = Client(auth=os.getenv("NOTION_API_TOKEN"))

    def _search(self, query: str) -> list:
        response = self.client.search(query=query)
        return response["results"]

    def test_create_new_page_in_database(self):
        database_id = "1cb454d6-205c-4eda-9fed-a1cf371305a3"
        self.client.pages.create(
            parent={"type": "database_id", "database_id": database_id},
            properties={
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Test"
                        }
                    }
                ]
            },
            children=[
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "Test"
                                }
                            }
                        ]
                    }
                },
            ]
        )

    def get_daily_log(self, date: datetime) -> DailyLog:
        data = notion_client.client.databases.query(
            database_id="58da568b4e634a469ffe36adeb59ab30")
        for result in data["results"]:
            title = result["properties"]["名前"]["title"][0]["text"]["content"]
            if title == datetime.strftime(date, "%Y-%m-%d"):
                return DailyLog.of(result)
        raise Exception("Not found")


if __name__ == "__main__":
    # python -m app.interface.notion_client
    notion_client = NotionClient()
    daily_log = notion_client.get_daily_log(datetime.now())
    print(daily_log)
