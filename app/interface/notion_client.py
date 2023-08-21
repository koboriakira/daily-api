import os
from notion_client import Client
from app.domain.spotify.track import Track
from app.domain.spotify.album import Album
from app.domain.notion.properties import Date, Title, Relation, Properties, Status, Property, Text, Url
from app.domain.notion.cover import Cover
from app.domain.notion.database.database_type import DatabaseType
from app.domain.notion.block import BlockFactory, Block, Paragraph
from app.domain.notion.block.rich_text import RichText, RichTextBuilder
from app.domain.notion.database import DatabaseType
from app.domain.notion.page import DailyLog, Recipe, Webclip, Book, ProwrestlingWatch, Music, Zettlekasten, Restaurant, GoOut, Arata
from datetime import datetime, timedelta, timezone, date
from typing import Optional


class NotionClient:
    def __init__(self):
        self.client = Client(auth=os.getenv("NOTION_API_TOKEN"))

    def _search(self, query: str) -> list:
        response = self.client.search(query=query)
        return response["results"]

    def get_daily_log(self, date: Optional[datetime] = None) -> DailyLog:
        date = datetime.now() if date is None else date
        daily_log = self.__find_daily_log(date)
        if daily_log is None:
            raise Exception("Not found")
        properties = daily_log["properties"]

        # 日付
        date = Date.of("日付", properties["日付"])

        # 一言
        summary_rich_text = properties["一言"]["rich_text"]
        summary = summary_rich_text[0]["text"]["content"] if len(
            summary_rich_text) > 0 else ""

        # レシピ
        recipe_ids = self.__get_relation_ids(properties, "レシピ")
        recipes = list(map(lambda r_id: self.__find_recipe(r_id), recipe_ids))

        # Webクリップ
        webclip_ids = self.__get_relation_ids(properties, "📎 Webclip")
        webclips = list(
            map(lambda w_id: self.__find_webclip(w_id), webclip_ids))

        # 書籍
        book_ids = self.__get_relation_ids(properties, "📚 書籍")
        books = list(map(lambda b_id: self.__find_book(b_id), book_ids))

        # プロレス観戦記録
        prowrestling_watch_ids = self.__get_relation_ids(
            properties, "観戦記録")
        prowrestling_watches = list(
            map(lambda p_id: self.__find_prowrestling_watch(p_id), prowrestling_watch_ids))

        # 音楽
        music_ids = self.__get_relation_ids(properties, "🎧 ミュージック")
        musics = list(map(lambda m_id: self.__find_music(m_id), music_ids))

        # Zettlekasten
        zettlekasten_ids = self.__get_relation_ids(
            properties, "📝 Zettlekasten")
        zettlekasten = list(
            map(lambda z_id: self.__find_zettlekasten(z_id), zettlekasten_ids))

        # 外食
        restaurant_ids = self.__get_relation_ids(properties, "🥘 外食・お持たせ")
        restaurants = list(
            map(lambda r_id: self.__find_restaurant(r_id), restaurant_ids))

        # おでかけ
        go_out_ids = self.__get_relation_ids(properties, "おでかけ")
        go_outs = list(
            map(lambda g_id: self.__find_go_out(g_id), go_out_ids))

        # あらた
        arata_ids = self.__get_relation_ids(properties, "あらた")
        aratas = list(
            map(lambda a_id: self.__find_arata(a_id), arata_ids))

        return DailyLog(
            id=daily_log["id"],
            created_time=daily_log["created_time"],
            last_edited_time=daily_log["last_edited_time"],
            parent=daily_log["parent"],
            archived=daily_log["archived"],
            date=date,
            summary=summary,
            recipes=recipes,
            webclips=webclips,
            books=books,
            prowrestling_watches=prowrestling_watches,
            musics=musics,
            zettlekasten=zettlekasten,
            restaurants=restaurants,
            go_outs=go_outs,
            aratas=aratas
        )

    def add_daily_log(self, block: Block, date: Optional[datetime] = None) -> None:
        """ 指定されたテキストをデイリーログの末尾に追記する """
        date = datetime.now() if date is None else date
        daily_log = self.__find_daily_log(date)
        child_element = block.to_dict()
        print(child_element)
        self.client.blocks.children.append(
            block_id=daily_log["id"],
            children=[child_element]
        )

    def add_track(self, track: Track, daily_log_id: str) -> str:
        """ 指定されたトラックを音楽データベースに追加する """
        # すでに存在するか確認
        data = self.__query_with_title_filter(
            database_type=DatabaseType.MUSIC,
            title_filter=track.name)
        if data is not None:
            return data["url"]

        # タグを作成
        tag_page_ids = []
        for artist in track.artists:
            page_id = self.add_tag(name=artist["name"])
            tag_page_ids.append(page_id)

        # 新しいページを作成
        artist_name = ",".join(list(map(lambda a: a["name"], track.artists)))
        spotify_url = track.external_urls["spotify"]
        result = self.__create_page_in_database(
            database_type=DatabaseType.MUSIC,
            cover=Cover.from_external_url(track.album["images"][0]["url"]),
            properties=[
                Title.from_plain_text(name="名前", text=track.name),
                Text.from_plain_text(name="Artist", text=artist_name),
                Relation.from_id_list(name="タグ", id_list=tag_page_ids),
                Relation.from_id(name="デイリーログ", id=daily_log_id),
                Url.from_url(name="Spotify", url=spotify_url)
            ]
        )

        # URLを返す
        return result["url"]

    def add_album(self, album: Album, daily_log_id: str) -> str:
        """ 指定されたアルバムを音楽データベースに追加する """
        # すでに存在するか確認
        data = self.__query_with_title_filter(
            database_type=DatabaseType.MUSIC,
            title_filter=album.name)
        if data is not None:
            return result["url"]

        # タグを作成
        tag_page_ids = []
        for artist in album.artists:
            page_id = self.add_tag(name=artist["name"])
            tag_page_ids.append(page_id)
        for genre in album.genres:
            page_id = self.add_tag(name=genre["name"])
            tag_page_ids.append(page_id)

        # 新しいページを作成
        artist_name = ",".join(list(map(lambda a: a["name"], album.artists)))
        result = self.__create_page_in_database(
            database_type=DatabaseType.MUSIC,
            cover=Cover.from_external_url(album.images[0]["url"]),
            properties=[
                Title.from_plain_text(name="名前", text=album.name),
                Text.from_plain_text(name="Artist", text=artist_name),
                Relation.from_id_list(name="タグ", id_list=tag_page_ids),
                Relation.from_id(name="デイリーログ", id=daily_log_id),
                Url.from_url(name="Spotify",
                             url=album.external_urls["spotify"])
            ]
        )

        # URLを返す
        return result["url"]

    def add_tag(self, name: str) -> str:
        """ 指定されたタグをタグデータベースに追加する """
        # すでに存在するか確認
        data = self.__query_with_title_filter(
            database_type=DatabaseType.TAG,
            title_filter=name)
        if data is not None:
            return data["id"]

        # 作成
        result = self.__create_page_in_database(
            database_type=DatabaseType.TAG,
            properties=[
                Title.from_plain_text(name="名前", text=name)
            ]
        )
        return result["id"]

    def create_weekly_log(self, year: int, isoweeknum: int) -> None:
        """ 指定された年と週から週報ページを作成する """
        # ウィークリーログを作成
        weekly_log_entity = self.__find_weekly_log(year, isoweeknum)
        if weekly_log_entity is None:
            weekly_log_entity = self.__create_weekly_log_page(year, isoweeknum)
        print(weekly_log_entity)

        # 開始日から終了日までのデイリーログを作成
        # 指定さらた年とISO週から開始日、終了日を取得
        start_date = datetime.strptime(
            f"{year}-{isoweeknum}-1", "%G-%V-%u")
        # datetimeをdateに変換
        start_date = datetime.date(start_date)
        for i in range(7):
            date = start_date + timedelta(days=i)
            daily_log = self.__find_daily_log(date)
            if daily_log is None:
                daily_log = self.__create_daily_log_page(
                    date=date, weekly_log_id=weekly_log_entity["id"])

    def set_today_to_inprogress(self) -> None:
        """
        「プロジェクト」データベースの"Today"ステータスを"In progress"にする。
        明日の計画を練るときのための準備として利用される。
        """
        data = self.client.databases.query(
            database_id=DatabaseType.PROJECT.value)
        for result in data["results"]:
            status = Status.of("ステータス", result["properties"]["ステータス"])
            if status.is_today():
                updated_status = Status.from_status_name(
                    name="ステータス", status_name="In progress")
                self.__update_page(page_id=result["id"],
                                   properties=[updated_status])

    def __create_page_in_database(self, database_type: DatabaseType, cover: Optional[Cover] = None, properties: list[Property] = []) -> dict:
        """ データベース上にページを新規作成する """
        return self.client.pages.create(
            parent={
                "type": "database_id",
                "database_id": database_type.value
            },
            cover=cover.__dict__() if cover is not None else None,
            properties=Properties(values=properties).__dict__() if len(
                properties) > 0 else None
        )

    def __update_page(self, page_id: str, properties: list[Property] = []) -> None:
        """ 指定されたページを更新する """
        self.client.pages.update(
            page_id=page_id,
            properties=Properties(values=properties).__dict__()
        )

    def __find_daily_log(self, date: datetime) -> Optional[dict]:
        return self.__query_with_title_filter(
            database_type=DatabaseType.DAILY_LOG,
            title_filter=datetime.strftime(date, "%Y-%m-%d")
        )

    def __create_daily_log_page(self, date: date, weekly_log_id: str) -> dict:
        return self.__create_page_in_database(
            database_type=DatabaseType.DAILY_LOG,
            properties=[
                Date.from_start_date(name="日付", start_date=date),
                Title.from_plain_text(name="名前", text=date.isoformat()),
                Relation.from_id_list(name="💭 ウィークリーログ", id_list=[weekly_log_id])]
        )

    def __find_weekly_log(self, year: int, isoweeknum: int) -> Optional[dict]:
        return self.__query_with_title_filter(
            database_type=DatabaseType.WEEKLY_LOG,
            title_filter=f"{year}-Week{isoweeknum}"
        )

    def __create_weekly_log_page(self, year: int, isoweeknum: int) -> dict:
        title_text = f"{year}-Week{isoweeknum}"
        start_date = datetime.strptime(
            f"{year}-{isoweeknum}-1", "%G-%V-%u")
        start_date = datetime.date(start_date)
        end_date = start_date + timedelta(days=6)

        return self.__create_page_in_database(
            database_type=DatabaseType.WEEKLY_LOG,
            properties=[
                Title.from_plain_text(
                    name="名前", text=title_text),
                Date.from_range(name="日付", start=start_date, end=end_date),
            ]
        )

    def __query_with_status_filter(self, database_type: DatabaseType, status: list[str]) -> list[dict]:
        data = self.__query(database_type=database_type)
        for page in data["results"]:
            title = Title.from_properties(page["properties"])
            if title.text == title_filter:
                return page
        return None

    def __query(self, database_type: DatabaseType) -> dict:
        return self.client.databases.query(
            database_id=database_type.value
        )

    def __find_recipe(self, page_id: str) -> Recipe:
        result = self.client.pages.retrieve(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return Recipe.of(result, blocks)

    def __find_webclip(self, page_id: str) -> Webclip:
        result = self.client.pages.retrieve(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return Webclip.of(result, blocks)

    def __find_book(self, page_id: str) -> Book:
        result = self.client.pages.retrieve(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return Book.of(result, blocks)

    def __find_prowrestling_watch(self, page_id: str) -> ProwrestlingWatch:
        result = self.client.pages.retrieve(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return ProwrestlingWatch.of(result, blocks)

    def __find_music(self, page_id: str) -> Music:
        result = self.client.pages.retrieve(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return Music.of(result, blocks)

    def __find_zettlekasten(self, page_id: str) -> Zettlekasten:
        result = self.client.pages.retrieve(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return Zettlekasten.of(result, blocks)

    def __find_restaurant(self, page_id: str) -> Restaurant:
        result = self.client.pages.retrieve(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return Restaurant.of(result, blocks)

    def __find_go_out(self, page_id: str) -> GoOut:
        result = self.client.pages.retrieve(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return GoOut.of(result, blocks)

    def __find_arata(self, page_id: str) -> Arata:
        result = self.client.pages.retrieve(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return Arata.of(result, blocks)

    def __get_relation_ids(self, properties: dict, key: str) -> list[str]:
        return list(map(
            lambda r: r["id"], properties[key]["relation"]))

    def __get_block_children(self, page_id: str) -> list:
        block_entities = self.client.blocks.children.list(block_id=page_id)[
            "results"]
        return list(map(lambda b: BlockFactory.create(b), block_entities))

    def add_24hours_pages_in_daily_log(self, date: str) -> None:
        """ 直近24時間以内に更新されたページを、当日のデイリーログに追加する"""
        now = datetime.fromisoformat('2023-08-11')
        daily_log = self.get_daily_log(now)
        from_date = now - timedelta(hours=9)
        to_date = now + timedelta(hours=15)

        # 更新のあったページのID一覧を取得
        now = datetime.now(tz=timezone(timedelta(hours=0)))
        result = list(self.get_pages(from_date=from_date, to_date=to_date))
        page_id_list = list(map(lambda page: page["id"], result))

        # デイリーログをに追加
        mention_bulleted_list_items = list(
            map(lambda page_id: create_mention_bulleted_list_item(page_id=page_id), page_id_list))
        self.client.blocks.children.append(
            block_id=daily_log.id,
            children=mention_bulleted_list_items
        )

    def get_pages(self, from_date: datetime, to_date: datetime):
        """ 直近24時間以内に更新されたページを取得する """
        result = []
        while True:
            start_cursor = search_result["next_cursor"] if len(
                result) > 0 and "next_cursor" in search_result else None
            search_result = self.client.search(
                filter={
                    "value": "page",
                    "property": "object"
                },
                sort={
                    "direction": "descending",
                    "timestamp": "last_edited_time"
                },
                start_cursor=start_cursor
            )
            last_page = search_result["results"][-1]
            last_page_last_edited_time = datetime.fromisoformat(
                last_page["last_edited_time"])
            if last_page_last_edited_time.timestamp() < from_date:
                filtered_results = list(filter(lambda r: valid_datetime(datetime.fromisoformat(
                    r["last_edited_time"]), from_date, to_date), search_result["results"]))
                result.extend(filtered_results)
                break
            else:
                filtered_results = list(filter(lambda r: valid_datetime(datetime.fromisoformat(
                    r["last_edited_time"]), from_date, to_date), search_result["results"]))
                result.extend(filtered_results)
        for page in result:
            parent = page["parent"]
            if parent["type"] == "database_id" and parent["database_id"] in DatabaseType.ignore_updated_at():
                continue
            yield page


def valid_datetime(target: datetime, from_date: datetime, to_date: datetime) -> bool:
    return from_date.timestamp() <= target.timestamp() and target.timestamp() <= to_date.timestamp()


def create_mention_bulleted_list_item(page_id: str) -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [
                {
                    "type": "mention",
                    "mention": {
                        "type": "page",
                        "page": {
                            "id": page_id
                        }
                    },
                },
            ]
        }
    }


if __name__ == "__main__":
    # python -m app.interface.notion_client
    notion_client = NotionClient()
    # notion_client.create_weekly_log(year=2023, isoweeknum=34)
    # print(daily_log)
    # print(notion_client.client.blocks.children.list(
    #     block_id="f2c43e16b09745b19ca599fafd429429"))
    # print(notion_client.client.pages.retrieve(
    #     page_id="f2c43e16b09745b19ca599fafd429429"))
    # すでに存在するか確認

    notion_client.set_today_to_inprogress()
