import os
from notion_client import Client
from app.domain.notion.properties import Date
from app.domain.notion.page import DailyLog, Recipe
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
        daily_log = self.__find_daily_log(date)
        properties = daily_log["properties"]

        # 日付
        date = Date.of("日付", properties["日付"])

        # レシピ
        recipe_ids = properties["レシピ"]["relation"]
        recipe_ids = list(
            map(lambda r: self.__find_recipe(r["id"]), recipe_ids))

        return DailyLog(
            id=daily_log["id"],
            created_time=daily_log["created_time"],
            last_edited_time=daily_log["last_edited_time"],
            parent=daily_log["parent"],
            archived=daily_log["archived"],
            date=date,
            recipes=recipe_ids
        )

    def __find_daily_log(self, date: datetime) -> dict:
        data = self.client.databases.query(
            database_id="58da568b4e634a469ffe36adeb59ab30")
        for result in data["results"]:
            title = result["properties"]["名前"]["title"][0]["text"]["content"]
            if title == datetime.strftime(date, "%Y-%m-%d"):
                return result
        raise Exception("Not found")

    def __find_recipe(self, page_id: str) -> Recipe:
        result = self.client.pages.retrieve(page_id=page_id)
        return Recipe.of(result)


if __name__ == "__main__":
    # python -m app.interface.notion_client
    notion_client = NotionClient()
    # 2023-07-29の日報を取得
    daily_log = notion_client.get_daily_log(datetime(2023, 7, 30))
    print(daily_log.recipes)
    print(daily_log.date)
