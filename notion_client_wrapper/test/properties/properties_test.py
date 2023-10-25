from unittest import TestCase
from notion_client_wrapper.properties import Properties, Property


class PropertiesTest(TestCase):
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
        actual = Properties.from_dict(input)

        title = actual.get_title(key="title")
        self.assertEqual(title.name, "title")
        self.assertEqual(title.text, "テスト用ページ")
