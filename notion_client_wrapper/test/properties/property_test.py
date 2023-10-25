from unittest import TestCase
from notion_client_wrapper.properties import Properties, Property, Title, Text


class PropertyTest(TestCase):
    def test_タイトルの変換(self):
        input =  {
          "id": "title",
          "type": "title",
          "title": [
            {
              "type": "text",
              "text": {
                "content": "テストワークスペース",
                "link": None
              },
              "annotations": {
                "bold": False,
                "italic": False,
                "strikethrough": False,
                "underline": False,
                "code": False,
                "color": "default"
              },
              "plain_text": "テストワークスペース",
              "href": None
            }
          ]
        }
        actual: Title = Property.from_dict("title", input)
        assert actual.name == "title"
        assert actual.text == "テストワークスペース"

    def test_テキストの変換(self):
        input = {
          "id": "E%5Cwy",
          "type": "rich_text",
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "サンプルテキスト",
                "link": None
              },
              "annotations": {
                "bold": False,
                "italic": False,
                "strikethrough": False,
                "underline": False,
                "code": False,
                "color": "default"
              },
              "plain_text": "サンプルテキスト",
              "href": None
            }
          ]
        }
        actual: Text = Property.from_dict("text", input)
        assert actual.name == "text"
        assert actual.text == "サンプルテキスト"
