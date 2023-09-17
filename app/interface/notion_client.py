import os
from notion_client import Client
from app.domain.spotify.track import Track
from app.domain.spotify.album import Album
from app.domain.notion.properties import Date, Title, Relation, Properties, Status, Property, Text, Url, MultiSelect, Select, Checkbox
from app.domain.notion import Cover, NotionDatetime, TimeKind
from app.domain.notion.database.database_type import DatabaseType
from app.domain.notion.block import BlockFactory, Block, ChildDatabase
from app.domain.notion.database import DatabaseType
from app.domain.notion.page import DailyLog, Recipe, Webclip, Book, ProwrestlingWatch, Music, Zettlekasten, Restaurant, GoOut, Arata
from datetime import datetime, timedelta, timezone, date
from datetime import date as DateObject
from typing import Optional


class NotionClient:
    def __init__(self):
        self.client = Client(auth=os.getenv("NOTION_API_TOKEN"))

    def get_daily_log(self, date: Optional[DateObject] = None) -> DailyLog:
        target_date = DateObject.today() if date is None else date
        daily_log = self.__find_daily_log(target_date)
        print(daily_log)
        if daily_log is None:
            raise Exception("Not found")
        properties = daily_log["properties"]

        # 日付
        date = Date.of("日付", properties["日付"])

        # 目標
        daily_goal_rich_text = properties["目標"]["rich_text"]
        daily_goal = daily_goal_rich_text[0]["text"]["content"] if len(
            daily_goal_rich_text) > 0 else ""

        # ふりかえり
        daily_retro_comment_rich_text = properties["ふりかえり"]["rich_text"]
        daily_retro_comment = daily_retro_comment_rich_text[0]["text"]["content"] if len(
            daily_retro_comment_rich_text) > 0 else ""

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
            url=daily_log["url"],
            created_time=daily_log["created_time"],
            last_edited_time=daily_log["last_edited_time"],
            parent=daily_log["parent"],
            archived=daily_log["archived"],
            date=date,
            daily_goal=daily_goal,
            daily_retro_comment=daily_retro_comment,
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

    def get_daily_log_id(self, date: DateObject) -> str:
        daily_log = self.__find_daily_log(date)
        if daily_log is None:
            raise Exception("Not found")
        return daily_log["id"]

    def append_blocks(self, block_id: str, block: Block | list[Block]) -> None:
        """ 指定されたブロックを末尾に追加する """
        if isinstance(block, Block):
            self.__append_block_children(
                block_id=block_id,
                children=[block.to_dict()]
            )
            return
        if isinstance(block, list):
            self.__append_block_children(
                block_id=block_id,
                children=list(map(lambda b: b.to_dict(), block))
            )
            return
        raise ValueError("block must be Block or list[Block]")

    def add_daily_log(self, block: Block, date: Optional[DateObject] = None) -> None:
        """ 指定されたテキストをデイリーログの末尾に追記する """
        daily_log = self.__find_daily_log(
            date=DateObject.today() if date is None else date)
        if daily_log is None:
            print("Daily Log is not found")
            return
        self.append_blocks(daily_log["id"], block)

    def add_track(self, name: str, artists: list[str], spotify_url: str, cover_url: str, daily_log_id: str) -> str:
        """ 指定されたトラックを音楽データベースに追加する """
        # すでに存在するか確認
        data = self.__query_with_title_filter(
            database_type=DatabaseType.MUSIC,
            title=name)
        if data is not None:
            print("Track is already registered")
            return data

        # タグを作成
        tag_page_ids = []
        for artist in artists:
            page_id = self.add_tag(name=artist)
            tag_page_ids.append(page_id)

        # 新しいページを作成
        artist_name = ",".join(artists)
        result = self.__create_page_in_database(
            database_type=DatabaseType.MUSIC,
            cover=Cover.from_external_url(cover_url),
            properties=[
                Title.from_plain_text(name="名前", text=name),
                Text.from_plain_text(name="Artist", text=artist_name),
                Relation.from_id_list(name="タグ", id_list=tag_page_ids),
                Relation.from_id(name="デイリーログ", id=daily_log_id),
                Url.from_url(name="Spotify", url=spotify_url)
            ]
        )

        print(result)
        return result

    def add_album(self, album: Album, daily_log_id: str) -> dict:
        """ 指定されたアルバムを音楽データベースに追加する """
        # すでに存在するか確認
        data = self.__query_with_title_filter(
            database_type=DatabaseType.MUSIC,
            title=album.name)
        if data is not None:
            return data

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
        return result

    def add_tag(self, name: str) -> str:
        """ 指定されたタグをタグデータベースに追加する """
        # すでに存在するか確認
        data = self.__query_with_title_filter(
            database_type=DatabaseType.TAG,
            title=name)
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
        weekly_log_entity = self.find_weekly_log(year, isoweeknum)
        if weekly_log_entity is None:
            weekly_log_entity = self.__create_weekly_log_page(year, isoweeknum)

        # 開始日から終了日までのデイリーログを作成
        # 指定さらた年とISO週から開始日、終了日を取得
        start_date = datetime.strptime(
            f"{year}-{isoweeknum}-1", "%G-%V-%u")
        # datetimeをdateに変換
        start_date = datetime.date(start_date)
        for i in range(7):
            daily_date = start_date + timedelta(days=i)
            if (_daily_log := self.__find_daily_log(daily_date)) is None:
                _created_daily_log = self.__create_daily_log_page(date=daily_date,
                                                                  weekly_log_id=weekly_log_entity["id"])
            if i == 5:
                # 週次レビューのプロジェクトを作成
                self.create_project(title=f"{year}-Week{isoweeknum}週次レビュー",
                                    goal="今週のふりかえり、目標達成の確認をして、来週の目標を立てる",
                                    start_date=daily_date,
                                    status="Scheduled",
                                    end_date=daily_date + timedelta(days=1),
                                    remind_date=daily_date,
                                    )

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

    def create_zettlekasten(self, title: str, url: str) -> None:
        daily_log_entity = self.__find_daily_log(DateObject.today())
        daily_log_id = daily_log_entity["id"]
        return self.__create_page_in_database(
            database_type=DatabaseType.ZETTLEKASTEN,
            properties=[
                Title.from_plain_text(name="名前", text=title),
                Url.from_url(name="記事", url=url),
                Relation.from_id(name="デイリーログ", id=daily_log_id)
            ]
        )

    def retrieve_projects(self,
                          status_list: list[Status] = [],
                          remind_date: Optional[DateObject] = None,
                          goal_id: Optional[str] = None,
                          get_detail: bool = True,
                          filter_thisweek: bool = False,) -> list[dict]:
        """ プロジェクトデータベースの全てのページを取得する """
        status_name_list = [
            status.status_name for status in status_list]

        # まずプロジェクトを検索する
        searched_projects = self.__query(
            database_type=DatabaseType.PROJECT)["results"]
        projects = []
        for project in searched_projects:
            properties = project["properties"]
            # 目標
            goal_id_list = self.__get_relation_ids(
                properties=properties, key="目標")
            if goal_id is not None and goal_id not in goal_id_list:
                continue
            # 今週やる
            is_thisweek = Checkbox.of(name="今週やる", param=properties["今週やる"])
            if filter_thisweek and not is_thisweek.checked:
                continue
            # ステータス
            status = Status.of(name="ステータス", param=properties["ステータス"])
            daily_log_id = self.__get_relation_ids(
                properties=properties, key="デイリーログ")
            if len(status_name_list) > 0 and status.status_name not in status_name_list:
                continue
            # リマインド日
            if remind_date is not None:
                project_remind_date = Date.of(
                    name="リマインド", param=properties["リマインド"])
                if project_remind_date.start != remind_date.isoformat():
                    continue
            title = Title.from_properties(properties)
            last_edited_time = NotionDatetime.from_page_block(
                kind=TimeKind.LAST_EDITED_TIME, block=project)
            created_time = NotionDatetime.from_page_block(
                kind=TimeKind.CREATED_TIME, block=project)
            projects.append({
                "id": project["id"],
                "url": project["url"],
                "daily_log_id": daily_log_id,
                "goal_id_list": goal_id_list,
                "status": status.status_name,
                "title": title.text,
                "is_thisweek": is_thisweek.checked,
                "created_at": created_time.value,
                "updated_at": last_edited_time.value,
            })

        if not get_detail:
            return projects

        # ヒットしたプロジェクトのタスクを取得する
        for project in projects:
            children = self.__get_block_children(page_id=project["id"])
            project["tasks"] = []
            for child in children:
                if isinstance(child, ChildDatabase):
                    database_id = child.id
                    response = self.__query(database_type=database_id)
                    for task in response["results"]:
                        task_title = Title.from_properties(task["properties"])
                        task_status = Status.of(
                            name="ステータス", param=task["properties"]["ステータス"])
                        task_date = Date.of(
                            name="予定日", param=task["properties"]["予定日"])
                        project["tasks"].append({
                            "id": task["id"],
                            "title": task_title.text,
                            "status": task_status.status_name,
                            "implementation_date": task_date.start
                        })

        return projects

    def create_project(self,
                       title: str,
                       start_date: DateObject,
                       goal: Optional[str] = None,
                       status: Optional[str] = None,
                       end_date: Optional[DateObject] = None,
                       remind_date: Optional[DateObject] = None,) -> None:
        """ プロジェクトデータベースに新しいプロジェクトを追加する """
        properties = [
            Title.from_plain_text(name="名前", text=title),
        ]
        if end_date is not None:
            properties.append(Date.from_range(
                name="期間", start=start_date, end=end_date))
        else:
            properties.append(Date.from_start_date(
                name="期間", start_date=start_date))
        if goal is not None:
            properties.append(Text.from_plain_text(name="ゴール", text=goal))
        if status is not None:
            properties.append(Status.from_status_name(
                name="ステータス", status_name=status))
        if remind_date is not None:
            properties.append(Date.from_start_date(
                name="リマインド", start_date=remind_date))

        return self.__create_page_in_database(
            database_type=DatabaseType.PROJECT,
            properties=properties
        )

    def update_project(self,
                       project_block_id: str,
                       status: Optional[str] = None) -> None:
        """ 指定されたプロジェクトのステータスを更新する """
        properties = []
        if status is not None:
            properties.append(Status.from_status_name(
                name="ステータス", status_name=status))
        self.__update_page(
            page_id=project_block_id,
            properties=properties
        )

    def retrieve_recipes(self, detail: bool = False) -> list[dict]:
        # 食材マスタ
        ingredient_list = self.__query(
            database_type=DatabaseType.INGREDIENTS)["results"]
        ingredients_map = {}
        for ingredient in ingredient_list:
            properties = ingredient["properties"]
            title = Title.from_properties(properties)
            ingredients_map[ingredient["id"]] = title.text

        # まずレシピを検索する
        searched_recipes = self.__query(
            database_type=DatabaseType.RECIPE)["results"]
        recipes = []
        for recipe in searched_recipes:
            properties = recipe["properties"]
            title = Title.from_properties(properties)
            ingredients_relation_id = self.__get_relation_ids(
                properties=recipe["properties"], key="Ingredients")
            ingredients = [ingredients_map[id]
                           for id in ingredients_relation_id]
            meal_categories = MultiSelect.of(
                name="種類", param=properties["種類"]) if "種類" in properties else None
            last_edited_time = NotionDatetime.from_page_block(
                kind=TimeKind.LAST_EDITED_TIME, block=recipe)
            created_time = NotionDatetime.from_page_block(
                kind=TimeKind.CREATED_TIME, block=recipe)
            daily_log_id = self.__get_relation_ids(
                properties=properties, key="デイリーログ")
            select = Select.of(
                name="状態", param=properties["状態"]) if "状態" in properties else None

            recipes.append({
                "id": recipe["id"],
                "url": recipe["url"],
                "title": title.text,
                "updated_at": last_edited_time.value,
                "created_at": created_time.value,
                "daily_log_id": daily_log_id,
                "ingredients": ingredients,
                "meal_categories": [c.name for c in meal_categories.values] if meal_categories is not None else [],
                "status": select.selected_name if select is not None else "",
            })
        if detail:
            # ヒットしたレシピの招待を取得する
            pass
        return recipes

    def retrieve_webclips(self) -> list[dict]:
        searched_prowrestlings = self.__query(
            database_type=DatabaseType.WEBCLIP)["results"]
        entities = []
        for page in searched_prowrestlings:
            properties = page["properties"]
            title = Title.from_properties(properties)
            last_edited_time = NotionDatetime.from_page_block(
                kind=TimeKind.LAST_EDITED_TIME, block=page)
            created_time = NotionDatetime.from_page_block(
                kind=TimeKind.CREATED_TIME, block=page)
            daily_log_id = self.__get_relation_ids(
                properties=properties, key="デイリーログ")
            clipped_url = Url.of(name="URL", param=properties["URL"])
            status = Status.of(name="ステータス", param=properties["ステータス"])
            entities.append({
                "id": page["id"],
                "url": page["url"],
                "title": title.text,
                "created_at": created_time.value,
                "updated_at": last_edited_time.value,
                "daily_log_id": daily_log_id,
                "clipped_url": clipped_url.url,
                "status": status.status_name
            })
        return entities

    def retrieve_musics(self) -> list[dict]:
        searched_musics = self.__query(
            database_type=DatabaseType.MUSIC)["results"]
        musics = []
        for searched_music in searched_musics:
            properties = searched_music["properties"]
            title = Title.from_properties(properties)
            spotify_url = Url.of(name="Spotify", param=properties["Spotify"])
            artist_text = Text.from_dict(
                name="Artist", param=properties["Artist"])
            last_edited_time = NotionDatetime.from_page_block(
                kind=TimeKind.LAST_EDITED_TIME, block=searched_music)
            created_time = NotionDatetime.from_page_block(
                kind=TimeKind.CREATED_TIME, block=searched_music)
            daily_log_id = self.__get_relation_ids(
                properties=properties, key="デイリーログ")
            musics.append({
                "id": searched_music["id"],
                "url": searched_music["url"],
                "artist": artist_text.text,
                "title": title.text,
                "spotify_url": spotify_url.url,
                "created_at": created_time.value,
                "updated_at": last_edited_time.value,
                "daily_log_id": daily_log_id
            })
        return musics

    def retrieve_prowrestlings(self) -> list[dict]:
        searched_prowrestlings = self.__query(
            database_type=DatabaseType.PROWRESTLING)["results"]
        entities = []
        for page in searched_prowrestlings:
            properties = page["properties"]
            title = Title.from_properties(properties)
            last_edited_time = NotionDatetime.from_page_block(
                kind=TimeKind.LAST_EDITED_TIME, block=page)
            created_time = NotionDatetime.from_page_block(
                kind=TimeKind.CREATED_TIME, block=page)
            daily_log_id = self.__get_relation_ids(
                properties=properties, key="デイリーログ")
            entities.append({
                "id": page["id"],
                "url": page["url"],
                "title": title.text,
                "created_at": created_time.value,
                "updated_at": last_edited_time.value,
                "daily_log_id": daily_log_id,
            })
        return entities

    def retrieve_books(self) -> list[dict]:
        searched_books = self.__query(
            database_type=DatabaseType.BOOK)["results"]
        entities = []
        for page in searched_books:
            properties = page["properties"]
            title = Title.from_properties(properties)
            last_edited_time = NotionDatetime.from_page_block(
                kind=TimeKind.LAST_EDITED_TIME, block=page)
            created_time = NotionDatetime.from_page_block(
                kind=TimeKind.CREATED_TIME, block=page)
            daily_log_id = self.__get_relation_ids(
                properties=properties, key="デイリーログ")
            status = Status.of(name="ステータス", param=properties["ステータス"])
            entities.append({
                "id": page["id"],
                "url": page["url"],
                "title": title.text,
                "created_at": created_time.value,
                "updated_at": last_edited_time.value,
                "daily_log_id": daily_log_id,
                "status": status.status_name
            })
        return entities

    def retrieve_zettlekastens(self) -> list[dict]:
        searched_zettlekastens = self.__query(
            database_type=DatabaseType.ZETTLEKASTEN)["results"]
        entities = []
        for page in searched_zettlekastens:
            properties = page["properties"]
            title = Title.from_properties(properties)
            last_edited_time = NotionDatetime.from_page_block(
                kind=TimeKind.LAST_EDITED_TIME, block=page)
            created_time = NotionDatetime.from_page_block(
                kind=TimeKind.CREATED_TIME, block=page)
            daily_log_id = self.__get_relation_ids(
                properties=properties, key="デイリーログ")
            entities.append({
                "id": page["id"],
                "url": page["url"],
                "title": title.text,
                "created_at": created_time.value,
                "updated_at": last_edited_time.value,
                "daily_log_id": daily_log_id,
            })
        return entities

    def append_comment(self, page_id: str, text: str):
        """ 指定されたページにコメントを追加する """
        return self.client.comments.create(
            parent={
                "page_id": page_id
            },
            rich_text=[
                {
                    "text": {
                        "content": text
                    }
                }
            ],
        )

    def retrieve_comments(self, page_id: str) -> list[dict]:
        """ 指定されたページのコメントを取得する """
        comments = self.client.comments.list(
            block_id=page_id
        )
        return comments["results"]

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

    def __find_daily_log(self, date: DateObject) -> Optional[dict]:
        return self.__query_with_title_filter(
            database_type=DatabaseType.DAILY_LOG,
            title=date.isoformat()
        )

    def __create_daily_log_page(self, date: date, weekly_log_id: str) -> dict:
        return self.__create_page_in_database(
            database_type=DatabaseType.DAILY_LOG,
            properties=[
                Date.from_start_date(name="日付", start_date=date),
                Title.from_plain_text(name="名前", text=date.isoformat()),
                Relation.from_id_list(name="💭 ウィークリーログ", id_list=[weekly_log_id])]
        )

    def find_weekly_log(self, year: int, isoweeknum: int) -> Optional[dict]:
        weekly_log = self.__query_with_title_filter(
            database_type=DatabaseType.WEEKLY_LOG,
            title=f"{year}-Week{isoweeknum}"
        )
        if weekly_log is None:
            return None

        properties = weekly_log["properties"]
        title = Title.from_properties(properties)
        goal = Text.from_dict(name="目標", param=properties["目標"])

        return {
            "id": weekly_log["id"],
            "url": weekly_log["url"],
            "title": title.text,
            "goal": goal.text,
        }

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
                Date.from_range(name="期間", start=start_date, end=end_date),
            ]
        )

    def __query_with_title_filter(self, database_type: DatabaseType, title: str) -> Optional[dict]:
        data = self.__query(database_type=database_type)
        for page in data["results"]:
            title_field = Title.from_properties(page["properties"])
            if title_field.text == title:
                return page
        return None

    def __query(self, database_type: DatabaseType | str) -> dict:
        database_id = database_type.value if isinstance(
            database_type, DatabaseType) else database_type
        return self.client.databases.query(
            database_id=database_id
        )

    def __retrieve_page(self, page_id: str) -> dict:
        return self.client.pages.retrieve(page_id=page_id)

    def __find_recipe(self, page_id: str) -> Recipe:
        result = self.__retrieve_page(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return Recipe.of(result, blocks)

    def __find_webclip(self, page_id: str) -> Webclip:
        result = self.__retrieve_page(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return Webclip.of(result, blocks)

    def __find_book(self, page_id: str) -> Book:
        result = self.__retrieve_page(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return Book.of(result, blocks)

    def __find_prowrestling_watch(self, page_id: str) -> ProwrestlingWatch:
        result = self.__retrieve_page(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return ProwrestlingWatch.of(result, blocks)

    def __find_music(self, page_id: str) -> Music:
        result = self.__retrieve_page(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return Music.of(result, blocks)

    def __find_zettlekasten(self, page_id: str) -> Zettlekasten:
        result = self.__retrieve_page(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return Zettlekasten.of(result, blocks)

    def __find_restaurant(self, page_id: str) -> Restaurant:
        result = self.__retrieve_page(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return Restaurant.of(result, blocks)

    def __find_go_out(self, page_id: str) -> GoOut:
        result = self.__retrieve_page(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return GoOut.of(result, blocks)

    def __find_arata(self, page_id: str) -> Arata:
        result = self.__retrieve_page(page_id=page_id)
        blocks = self.__get_block_children(page_id)
        return Arata.of(result, blocks)

    def __get_relation_ids(self, properties: dict, key: str) -> list[str]:
        return list(map(
            lambda r: r["id"], properties[key]["relation"]))

    def __get_block_children(self, page_id: str) -> list:
        block_entities = self.__list_blocks(block_id=page_id)[
            "results"]
        return list(map(lambda b: BlockFactory.create(b), block_entities))

    def __append_block_children(self, block_id: str, children=list[dict]) -> list:
        print(children)
        self.client.blocks.children.append(
            block_id=block_id, children=children)

    def __list_blocks(self, block_id: str) -> dict:
        return self.client.blocks.children.list(block_id=block_id)

    def add_24hours_pages_in_daily_log(self, date: str) -> None:
        """ 直近24時間以内に更新されたページを、当日のデイリーログに追加する"""
        now = DateObject.fromisoformat('2023-08-11')
        daily_log_id = self.__find_daily_log(date=now)["id"]
        from_date = now - timedelta(hours=9)
        to_date = now + timedelta(hours=15)

        # 更新のあったページのID一覧を取得
        now = datetime.now(tz=timezone(timedelta(hours=0)))
        result = list(self.get_pages(from_date=from_date, to_date=to_date))
        page_id_list = list(map(lambda page: page["id"], result))

        # デイリーログをに追加
        mention_bulleted_list_items = list(
            map(lambda page_id: create_mention_bulleted_list_item(page_id=page_id), page_id_list))
        self.__append_block_children(
            block_id=daily_log_id,
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

    def test(self):
        data = self.__retrieve_page(page_id="fef84ea45b7d494c843fb426eb5606ac")
        print(data)
        pass


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
    notion_client.test()
