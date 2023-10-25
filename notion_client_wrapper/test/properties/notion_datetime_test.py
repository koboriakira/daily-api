from unittest import TestCase
from notion_client_wrapper.properties.notion_datetime import NotionDatetime


class NotionDatetimeTest(TestCase):
    def test_変換(self):
        actual = NotionDatetime.created_time(value="2023-10-25T01:23:00.000Z")
        assert actual.value.year == 2023
        assert actual.value.month == 10
        assert actual.value.day == 25
        assert actual.value.hour == 10
        assert actual.value.minute == 23
        assert actual.value.second == 0
        assert actual.value.microsecond == 0
