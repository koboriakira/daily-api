from app.interface.notion_client import NotionClient
from datetime import date, datetime, timedelta


class AddUpdatedPagesToDailyLog:
    """ 直近24時間以内に更新されたページを、当日のデイリーログに追加する """

    def __init__(self):
        self.notion_client = NotionClient()

    def handle(self, date: str = None):
        self.notion_client.add_24hours_pages_in_daily_log(date)


if __name__ == '__main__':
    # python -m app.usecase.add_updated_pages_to_daily_log
    AddUpdatedPagesToDailyLog().handle(date="2023-08-11")
