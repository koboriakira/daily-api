import os
from notion_client import Client


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


if __name__ == "__main__":
    # python -m app.interface.notion_client
    notion_client = NotionClient()
    page = notion_client.client.pages.retrieve(
        page_id="847ce5dcee364b22a231d0fc1b670319")
    print(page)

    date_option = {
        "Date": {
            "type": "date",
            "date": {
                    "start": "2023-09-02",
                    "end": None,
                    "time_zone": None
            }
        }
    }

    notion_client.client.pages.update(
        page_id="847ce5dcee364b22a231d0fc1b670319",
        properties={
            **date_option
        }
    )
