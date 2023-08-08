import os
from notion_client import Client
from app.domain.spotify.track import Track
from app.domain.spotify.album import Album
from app.domain.notion.properties import Date
from app.domain.notion.block import BlockFactory, Block
from app.domain.notion.database import DatabaseType
from app.domain.notion.page import DailyLog, Recipe, Webclip, Book, ProwrestlingWatch, Music, Zettlekasten, Restaurant, GoOut, Arata
from datetime import datetime
from typing import Optional


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

    def get_daily_log(self, date: Optional[datetime] = None) -> DailyLog:
        date = datetime.now() if date is None else date
        daily_log = self.__find_daily_log(date)
        properties = daily_log["properties"]
        print(properties)

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

    def add_text_daily_log(self, date: datetime, text: str) -> None:
        """ 指定されたテキストをデイリーログの末尾に追記する """

    def add_track(self, track: Track, daily_log_id: str) -> str:
        """ 指定されたトラックを音楽データベースに追加する """
        data = self.client.databases.query(
            database_id=DatabaseType.TAG.value)
        # すでに存在するか確認
        for result in data["results"]:
            title = result["properties"]["名前"]["title"][0]["text"]["content"]
            if title == track.name:
                return result["url"]

        # タグを作成
        tag_page_ids = []
        for artist in track.artists:
            page_id = self.add_tag(name=artist["name"])
            tag_page_ids.append(page_id)
        tag_page_ids = list(map(lambda t: {"id": t}, list(set(tag_page_ids))))

        # 新しいページを作成
        result = self.client.pages.create(
            parent={"type": "database_id",
                    "database_id": DatabaseType.MUSIC.value},
            cover={
                "type": "external",
                "external": {
                        "url": track.album["images"][0]["url"]
                }
            },
            properties={
                "名前": {
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": track.name
                            }
                        }
                    ]
                },
                "Artist": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": ",".join(list(map(lambda a: a["name"], track.artists)))
                            }
                        }
                    ]
                },
                "タグ": {
                    "type": "relation",
                    "relation": tag_page_ids,
                    "has_more": False
                },
                "デイリーログ": {
                    "type": "relation",
                    "relation": [
                        {
                            "id": daily_log_id
                        }
                    ],
                    "has_more": False
                },
                "Spotify": {
                    "type": "url",
                    "url": track.external_urls["spotify"]
                },
            }
        )
        return result["url"]

    def add_album(self, album: Album, daily_log_id: str) -> str:
        """ 指定されたアルバムを音楽データベースに追加する """
        data = self.client.databases.query(
            database_id=DatabaseType.TAG.value)
        # すでに存在するか確認
        for result in data["results"]:
            title = result["properties"]["名前"]["title"][0]["text"]["content"]
            if title == album.name:
                return result["url"]

        # タグを作成
        tag_page_ids = []
        for artist in album.artists:
            page_id = self.add_tag(name=artist["name"])
            tag_page_ids.append(page_id)
        for genre in album.genres:
            page_id = self.add_tag(name=genre["name"])
            tag_page_ids.append(page_id)
        tag_page_ids = list(map(lambda t: {"id": t}, list(set(tag_page_ids))))

        # 新しいページを作成
        result = self.client.pages.create(
            parent={"type": "database_id",
                    "database_id": DatabaseType.MUSIC.value},
            cover={
                "type": "external",
                "external": {
                        "url": album.images[0]["url"]
                }
            },
            properties={
                "名前": {
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": album.name
                            }
                        }
                    ]
                },
                "Artist": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": ",".join(list(map(lambda a: a["name"], album.artists)))
                            }
                        }
                    ]
                },
                "タグ": {
                    "type": "relation",
                    "relation": tag_page_ids,
                    "has_more": False
                },
                "デイリーログ": {
                    "type": "relation",
                    "relation": [
                        {
                            "id": daily_log_id
                        }
                    ],
                    "has_more": False
                },
                "Spotify": {
                    "type": "url",
                    "url": album.external_urls["spotify"]
                },
            }
        )
        return result["url"]

    def add_tag(self, name: str) -> str:
        """ 指定されたタグをタグデータベースに追加する """
        data = self.client.databases.query(
            database_id=DatabaseType.TAG.value)
        # すでに存在するか確認
        for result in data["results"]:
            title = result["properties"]["名前"]["title"][0]["text"]["content"]
            if title == name:
                print(result)
                return result["id"]
        # 作成
        result = self.client.pages.create(
            parent={
                "type": "database_id",
                "database_id": DatabaseType.TAG.value
            },
            properties={
                "名前": {
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": name
                            }
                        }
                    ]
                }
            }
        )
        return result["id"]

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


if __name__ == "__main__":
    # python -m app.interface.notion_client
    notion_client = NotionClient()
    # daily_log = notion_client.get_daily_log(date=datetime(2023, 8, 5))
    # print(daily_log)
    # print(notion_client.client.blocks.children.list(
    #     block_id="f2c43e16b09745b19ca599fafd429429"))
    # print(notion_client.client.pages.retrieve(
    #     page_id="f2c43e16b09745b19ca599fafd429429"))
