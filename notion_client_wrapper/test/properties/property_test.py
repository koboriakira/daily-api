from unittest import TestCase
from notion_client_wrapper.properties import Properties, Property, Title, Text, MultiSelect


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

    def test_タグの変換(self):
        input = {
          "id": "idFT",
          "type": "multi_select",
          "multi_select": [
            {
              "id": "a0c44ff8-352a-4aff-8546-e3c58b1ea886",
              "name": "タグA",
              "color": "orange"
            },
            {
              "id": "054f3c75-69af-4274-9f61-4e1fc594a97d",
              "name": "タグB",
              "color": "brown"
            }
          ]
        }
        actual: MultiSelect = Property.from_dict("text", input)
        assert actual.name == "text"
        assert actual.values[0].name == "タグA"
        assert actual.values[0].color == "orange"
        assert actual.values[1].name == "タグB"
        assert actual.values[1].color == "brown"
