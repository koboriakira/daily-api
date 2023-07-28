from notion_client import Client
import os


class NotionController:
    def __init__(self):
        self.notion_client = Client(auth=os.getenv("NOTION_API_TOKEN"))

    def test(self):
        # ページを作成するためのページIDを取得
        parent_page_id = "38bd0d06-e0c5-4b22-b307-2402363b0794"

        # 新しいページを作成
        new_page = self.notion_client.pages.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            properties={},
            children=[
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "text": [{"type": "text", "text": {"content": "This is a new header"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "text": [{"type": "text", "text": {"content": "This is a new paragraph"}}]
                    }
                }
            ]
        )


if __name__ == "__main__":
    # python -m app.controller.notion_controller
    notion_controller = NotionController()
    notion_controller.test()
