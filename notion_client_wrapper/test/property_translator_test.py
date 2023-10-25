from unittest import TestCase
from notion_client_wrapper.property_translator import PropertyTranslator
from notion_client_wrapper.properties.properties import Properties
from notion_client_wrapper.properties.property import Property
from notion_client_wrapper.properties.title import Title
from notion_client_wrapper.properties.text import Text
from notion_client_wrapper.properties.multi_select import MultiSelect
from notion_client_wrapper.properties.select import Select
from notion_client_wrapper.properties.number import Number
from notion_client_wrapper.properties.checkbox import Checkbox
from notion_client_wrapper.properties.status import Status
from notion_client_wrapper.properties.date import Date
from notion_client_wrapper.properties.url import Url
from notion_client_wrapper.properties.relation import Relation
from notion_client_wrapper.properties.notion_datetime import NotionDatetime

class PropertyTranslatorTest(TestCase):
    def test_シンプルなプロパティの変換(self):
        input = {
          "title": {
            "id": "title",
            "type": "title",
            "title": [
              {
                "type": "text",
                "text": {
                  "content": "テスト用ページ",
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
                "plain_text": "テスト用ページ",
                "href": None
              }
            ]
          }
        }
        actual = PropertyTranslator.from_dict(input)

        title = actual.get_title()
        self.assertEqual(title.name, "title")
        self.assertEqual(title.text, "テスト用ページ")

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
        actual: Title = PropertyTranslator.from_property_dict("dummy", input)
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
        actual: Text = PropertyTranslator.from_property_dict("dummy", input)
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
        actual: MultiSelect = PropertyTranslator.from_property_dict("dummy", input)
        assert actual.values[0].name == "タグA"
        assert actual.values[0].color == "orange"
        assert actual.values[1].name == "タグB"
        assert actual.values[1].color == "brown"

    def test_セレクトの変換(self):
        input = {
          "id": "dYYJ",
          "type": "select",
          "select": {
            "id": "6e65fbdd-6ffe-45f5-9a2d-5105e4a92547",
            "name": "選択肢A",
            "color": "gray"
          }
        }
        actual: Select = PropertyTranslator.from_property_dict("dummy", input)
        assert actual.selected_id == "6e65fbdd-6ffe-45f5-9a2d-5105e4a92547"
        assert actual.selected_name == "選択肢A"
        assert actual.selected_color == "gray"

    def test_数値の変換(self):
        input = {
          "id": "Np%5ES",
          "type": "number",
          "number": 1
        }
        actual: Number = PropertyTranslator.from_property_dict("dummy", input)
        assert actual.number == 1

    def test_日付の変換(self):
        input = {
          "id": "Yphg",
          "type": "date",
          "date": {
            "start": "2023-10-25",
            "end": None,
            "time_zone": None
          }
        }
        actual: Date = PropertyTranslator.from_property_dict("dummy", input)
        assert actual.start == "2023-10-25"
        assert actual.end == None

    def test_ステータスの変換(self):
        input = {
          "id": "m_%5DD",
          "type": "status",
          "status": {
            "id": "d67cabd0-34b3-4c98-8ab2-382b7b35480b",
            "name": "Not started",
            "color": "default"
          }
        }
        actual: Status = PropertyTranslator.from_property_dict("dummy", input)
        assert actual.status_name == "Not started"

    def test_チェックボックスの変換(self):
        input = {
          "id": "%7Ddn%7D",
          "type": "checkbox",
          "checkbox": True
        }
        actual: Checkbox = PropertyTranslator.from_property_dict("dummy", input)
        assert actual.checked == True

    def test_urlの変換(self):
        input = {
          "id": "zjfq",
          "type": "url",
          "url": "https://www.youtube.com/watch?v=cXYIvo6y1Os"
        }
        actual: Url = PropertyTranslator.from_property_dict("dummy", input)
        assert actual.url == "https://www.youtube.com/watch?v=cXYIvo6y1Os"

    def test_リレーションの変換(self):
        input = {
          "id": "lmws",
          "type": "relation",
          "relation": [
            {
              "id": "aa0f4973-c645-427c-bb69-b17eb47a3eaf"
            }
          ],
          "has_more": False
        }
        actual: Relation = PropertyTranslator.from_property_dict("dummy", input)
        assert actual.id_list[0] == "aa0f4973-c645-427c-bb69-b17eb47a3eaf"

    def test_Notion日時の変換(self):
        input = {
            'id': 'Af~u',
            'type': 'last_edited_time',
            'last_edited_time': '2023-10-25T01:23:00.000Z'
        }
        actual: NotionDatetime = PropertyTranslator.from_property_dict("dummy", input)
        assert actual.value.year == 2023
