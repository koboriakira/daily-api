from app.domain.notion.database_type import DatabaseType
from app.domain.notion.prowrestling_organization import ProwrestlingOrganization
from app.util.get_logger import get_logger
from datetime import datetime, timedelta
from datetime import date as DateObject
from typing import Optional
from notion_client_wrapper.client_wrapper import ClientWrapper, BasePage
from notion_client_wrapper.properties import Property, Date, Title, Text, Relation, Status, Url, Cover, Select
from notion_client_wrapper.block import Block, ChildDatabase


logger = get_logger(__name__)

DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

class NotionClient:
    def __init__(self):
        self.client = ClientWrapper()

    def get_daily_log(self, date: Optional[DateObject] = None) -> dict:
        """
        指定された日付のデイリーログを取得する
        date: 指定されない場合は今日の日付
        detail: Trueの場合はレシピ、Webクリップ、書籍、プロレス観戦記録、音楽、Zettlekasten、外食、おでかけ、あらたも取得する
        """
        target_date = DateObject.today() if date is None else date
        daily_log = self.__find_daily_log(target_date)
        if daily_log is None:
            raise Exception("Not found")

        daily_log_date = daily_log.get_date(name="日付")
        daily_goal = daily_log.get_text(name="目標")
        daily_retro_comment = daily_log.get_text(name="ふりかえり")
        return {
            "id": daily_log.id,
            "url": daily_log.url,
            "created_time": daily_log.created_time.value,
            "last_edited_time": daily_log.last_edited_time.value,
            "date": daily_log_date.start,
            "daily_goal": daily_goal.text,
            "daily_retro_comment": daily_retro_comment.text,
        }

    def get_daily_log_id(self, date: DateObject) -> str:
        daily_log = self.__find_daily_log(date)
        if daily_log is None:
            raise Exception("Not found")
        return daily_log.id

    def append_block(self, block_id: str, block: Block) -> None:
        """ 指定されたブロックを末尾に追加する """
        self.client.append_block(block_id=block_id, block=block)

    def append_blocks(self, block_id: str, blocks: list[Block]) -> None:
        """ 指定されたブロックを末尾に追加する """
        self.client.append_blocks(block_id=block_id, blocks=blocks)

    def add_daily_log(self, block: Block, date: Optional[DateObject] = None) -> None:
        """ 指定されたテキストをデイリーログの末尾に追記する """
        daily_log = self.__find_daily_log(
            date=DateObject.today() if date is None else date)
        if daily_log is None:
            print("Daily Log is not found")
            return
        self.client.append_block(block_id=daily_log["id"], block=block)

    def add_track(self, name: str, artists: list[str], spotify_url: str, cover_url: str, release_date: DateObject, daily_log_id: str = "") -> dict:
        """ 指定されたトラックを音楽データベースに追加する """
        # すでに存在するか確認
        musics = self.client.retrieve_database(
            database_id=DatabaseType.MUSIC.value,
            title=name)
        if len(musics) > 0:
            print("Track is already registered")
            music = musics[0]
            return {
                "id": music.id,
                "url": music.url
            }

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
                Date.from_start_date(name="リリース日", start_date=release_date),
                Url.from_url(name="Spotify", url=spotify_url)
            ]
        )

        return result

    def update_daily_log(self, date: DateObject, daily_goal: Optional[str] = None, daily_retro_comment: Optional[str] = None) -> None:
        daily_log_id = self.get_daily_log_id(date)

        properties = []
        if daily_goal is not None:
            properties.append(Text.from_plain_text(
                name="目標", text=daily_goal))
        if daily_retro_comment is not None:
            properties.append(Text.from_plain_text(
                name="ふりかえり", text=daily_retro_comment))

        self.client.update_page(page_id=daily_log_id, properties=properties)

    def add_tag(self, name: str) -> str:
        """ 指定されたタグをタグデータベースに追加する """
        # すでに存在するか確認
        tags = self.client.retrieve_database(
            database_id=DatabaseType.TAG.value,
            title=name)
        if len(tags) > 0:
            return tags[0].id

        # 作成
        result = self.client.create_page_in_database(
            database_id=DatabaseType.TAG.value,
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

    def create_monthly_log(self, year: int, month: int) -> None:
        """ マンスリーログを作成する """
        monthly_log_entity = self.find_monthly_log(year, month)
        if monthly_log_entity is None:
            monthly_log_entity = self.__create_monthly_log_page(year, month)

    def find_monthly_log(self, year: int, month: int) -> dict:
        """ 指定された年と月のマンスリーログを取得する """
        title=f"{year}-{month:02}"
        data = self.client.retrieve_database(
            database_type=DatabaseType.MONTHLY_LOG.value,
            title=title
        )
        return data

    def __create_monthly_log_page(self, year: int, month: int) -> dict:
        """ 指定された年と月のマンスリーログを作成する """
        title = Title.from_plain_text(name="名前", text=f"{year}-{month:02}")
        return self.client.create_page_in_database(
            database_id=DatabaseType.MONTHLY_LOG.value,
            properties=[title]
        )

    def set_today_to_inprogress(self) -> None:
        """
        「プロジェクト」データベースの"Today"ステータスを"In progress"にする。
        明日の計画を練るときのための準備として利用される。
        """
        data = self.client.retrieve_database(database_id=DatabaseType.PROJECT.value)
        for page in data:
            status = page.get_status(name="ステータス")
            if status.is_today():
                updated_status = Status.from_status_name(
                    name="ステータス", status_name="In progress")
                self.client.update_page(page_id=page.id, properties=[updated_status])

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
                          filter_thisweek: bool = False,
                          completed_at: Optional[DateObject] = None) -> list[dict]:
        """ プロジェクトデータベースの全てのページを取得する """
        status_name_list = [
            status.status_name for status in status_list]

        # まずプロジェクトを検索する
        searched_projects = self.client.retrieve_database(database_id=DatabaseType.PROJECT.value)
        projects = []
        for searched_project in searched_projects:
            project = self._convert_project(searched_project)
            # バリデーション: 目標
            if goal_id is not None and goal_id not in project["goal_id_list"]:
                continue
            # バリデーション: 今週やる
            if filter_thisweek and not project["is_thisweek"]:
                continue
            # バリデーション: ステータス
            if len(status_name_list) > 0 and project["status"] not in status_name_list:
                continue
            # バリデーション: リマインド日
            if remind_date is not None:
                if project["remind_date"] != remind_date.isoformat():
                    continue
            # バリデーション: 終了日
            if completed_at is not None:
                completed_date = searched_project.get_date(name="終了日")
                if completed_date.start != completed_at.isoformat():
                    continue

            # プロジェクトの詳細を取得する設定がある場合はタスクを取得する
            if get_detail:
                project["tasks"] = self._find_tasks(project_id=project["id"])
            projects.append(project)

        return projects

    def _find_tasks(self, project_id: str) -> list[dict]:
        children = self.client.list_blocks(block_id=project_id)
        tasks = []
        for child in children:
            if isinstance(child, ChildDatabase):
                database_id = child.id
                pages = self.client.retrieve_database(database_id=database_id)
                for page in pages:
                    task_title = page.get_title()
                    task_status = page.get_status(name="ステータス")
                    task_date = page.get_date(name="予定日")
                    minutes = page.get_number(name="時間(分)")
                    tasks.append({
                        "id": page.id,
                        "title": task_title.text,
                        "status": task_status.status_name,
                        "implementation_date": task_date.start,
                        "minutes": minutes.number
                    })
        return tasks

    def _convert_project(self, project: BasePage) -> dict:
        goal_relation = project.get_relation(name="目標")
        is_thisweek = project.get_checkbox(name="今週やる")
        status = project.get_status(name="ステータス")
        daily_log_relation = project.get_relation(name="デイリーログ")
        project_remind_date = project.get_date(name="リマインド")
        completed_at = project.get_date(name="終了日")
        recursive_conf = project.get_text(name="繰り返し設定")
        title = project.get_title()
        return {
            "id": project.id,
            "url": project.url,
            "daily_log_id": daily_log_relation.id_list,
            "goal_id_list": goal_relation.id_list,
            "status": status.status_name,
            "completed_at": completed_at.start,
            "recursive_conf": recursive_conf.text,
            "title": title.text,
            "remind_date": project_remind_date.start,
            "is_thisweek": is_thisweek.checked,
            "created_at": project.created_time.value,
            "updated_at": project.last_edited_time.value,
        }

    def create_project(self,
                       title: str,
                       start_date: DateObject,
                       goal: Optional[str] = None,
                       status: Optional[str] = None,
                       end_date: Optional[DateObject] = None,
                       remind_date: Optional[DateObject] = None,
                       recursive_conf: Optional[str] = None,) -> dict:
        """ プロジェクトデータベースに新しいプロジェクトを追加する """
        projects = self.client.retrieve_database(database_id=DatabaseType.PROJECT.value, title=title)
        if len(projects) > 0:
            return {
                "url": projects[0].url
            }

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
        if recursive_conf is not None:
            properties.append(Text.from_plain_text(
                name="繰り返し設定", text=recursive_conf))

        return self.__create_page_in_database(
            database_type=DatabaseType.PROJECT,
            properties=properties
        )

    def find_project_by_id(self,
                           project_block_id: str) -> dict:
        """ 指定されたプロジェクトを取得する """
        project_page = self.client.retrieve_page(page_id=project_block_id)
        project = self._convert_project(project_page)
        project["tasks"] = self._find_tasks(project_id=project["id"])
        return project

    def update_project(self,
                       project_block_id: str,
                       status: Optional[str] = None) -> None:
        """ 指定されたプロジェクトのステータスを更新する """
        properties = []
        if status is not None:
            properties.append(Status.from_status_name(
                name="ステータス", status_name=status))
        self.client.update_page(
            page_id=project_block_id,
            properties=properties
        )

    def update_recursive_project(self, date: DateObject) -> None:
        """ 繰り返しプロジェクトを更新する """
        # 指定された日付に完了したプロジェクトを取得する
        projects = self.retrieve_projects(completed_at=date)
        for project in projects:
            recursive_conf: Optional[str] = project["recursive_conf"]
            if recursive_conf is None or recursive_conf == "":
                continue
            logger.info(f"recursive_conf: {project['title']} {recursive_conf}")
            target_date = None
            if recursive_conf.lower().startswith("next"):
                # "next"系
                next_recursive_conf  = recursive_conf.lower().replace("next", "").strip()
                # next_recursive_confが数値だった場合
                if next_recursive_conf.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").isdecimal():
                   # 次の月のn日
                   n = next_recursive_conf.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "")
                   target_date = DateObject(year=date.year, month=date.month + 1, day=int(n))
                # next_recursive_confが曜日だった場合
                elif next_recursive_conf in DAYS:
                    # 次のn曜日
                    target_date = self.__get_next_weekday(date, next_recursive_conf)
            self.create_project(title=project["title"],
                                start_date=target_date,
                                status=Status.from_status_name(name="ステータス", status_name="Scheduled").status_name,
                                remind_date=target_date,
                                recursive_conf=recursive_conf,
                                )



    def retrieve_recipes(self, detail: bool = False) -> list[dict]:
        # 食材マスタ
        ingredient_list = self.client.retrieve_database(database_id=DatabaseType.INGREDIENTS.value)
        ingredients_map = {}
        for ingredient in ingredient_list:
            title = ingredient.get_title()
            ingredients_map[ingredient.id] = title.text

        # まずレシピを検索する
        searched_recipes = self.client.retrieve_database(database_id=DatabaseType.RECIPE.value)
        recipes = []
        for recipe in searched_recipes:
            title = recipe.get_title()
            ingredients_relation = recipe.get_relation(name="Ingredients")
            ingredients = [ingredients_map[id] for id in ingredients_relation.id_list]
            meal_categories = recipe.get_multi_select(name="種類")
            daily_log_relation = recipe.get_relation(name="デイリーログ")
            select = recipe.get_select(name="状態")

            recipes.append({
                "id": recipe.id,
                "url": recipe.url,
                "title": title.text,
                "updated_at": recipe.last_edited_time.value,
                "created_at": recipe.created_time.value,
                "daily_log_id": daily_log_relation.id_list,
                "ingredients": ingredients,
                "meal_categories": [c.name for c in meal_categories.values] if meal_categories is not None else [],
                "status": select.selected_name if select is not None else "",
            })
        if detail:
            # ヒットしたレシピの招待を取得する
            pass
        return recipes

    def retrieve_webclips(self) -> list[dict]:
        webclips = self.client.retrieve_database(database_id=DatabaseType.WEBCLIP.value)
        entities = []
        for page in webclips:
            title = page.get_title()
            daily_log_relation = page.get_relation(name="デイリーログ")
            clipped_url = page.get_url(name="URL")
            status = page.get_status(name="ステータス")
            entities.append({
                "id": page.id,
                "url": page.url,
                "title": title.text,
                "created_at": page.created_time.value,
                "updated_at": page.last_edited_time.value,
                "daily_log_id": daily_log_relation.id_list,
                "clipped_url": clipped_url.url,
                "status": status.status_name
            })
        return entities

    def retrieve_musics(self) -> list[dict]:
        searched_musics = self.client.retrieve_database(database_id=DatabaseType.MUSIC.value)
        musics = []
        for searched_music in searched_musics:
            title = searched_music.get_title()
            spotify_url = searched_music.get_url(name="Spotify")
            artist_text = searched_music.get_text(name="Artist")
            last_edited_time = searched_music.last_edited_time
            created_time = searched_music.created_time
            daily_log_relation = searched_music.get_relation(name="デイリーログ")
            musics.append({
                "id": searched_music.id,
                "url": searched_music.url,
                "artist": artist_text.text,
                "title": title.text,
                "spotify_url": spotify_url.url,
                "created_at": created_time.value,
                "updated_at": last_edited_time.value,
                "daily_log_id": daily_log_relation.id_list,
            })
        return musics

    def retrieve_prowrestlings(self) -> list[dict]:
        searched_prowrestlings = self.client.retrieve_database(database_id=DatabaseType.PROWRESTLING.value)
        entities = []
        for page in searched_prowrestlings:
            title = page.get_title()
            daily_log_relation = page.get_relation(name="デイリーログ")
            entities.append({
                "id": page.id,
                "url": page.url,
                "title": title.text,
                "created_at": page.created_time.value,
                "updated_at": page.last_edited_time.value,
                "daily_log_id": daily_log_relation.id_list,
            })
        return entities

    def create_prowrestling(self, title: str, date: DateObject, organization: str, url: Optional[str] = None) -> dict:
        """ プロレス観戦記録を作成する """
        pages = self.client.retrieve_database(database_id=DatabaseType.PROWRESTLING.value,
                                             title=title)

        if len(pages) > 0:
            page = pages[0]
        if len(pages) == 0:
            # 新規作成する
            prowrestling_organization = ProwrestlingOrganization.from_name(name=organization)
            properties = [
                Title.from_plain_text(name="名前", text=title),
                Date.from_start_date(name="日付", start_date=date),
                prowrestling_organization.to_select(),
            ]
            if url is not None:
                properties.append(Url.from_url(name="URL", url=url))

            created_page = self.client.create_page_in_database(
                database_id=DatabaseType.PROWRESTLING.value,
                properties=properties
            )
            page = self.client.retrieve_page(page_id=created_page["id"])
        return {
            "id": page.id,
            "url": page.url,
            "title": title,
            "created_at": page.created_time.value,
            "updated_at": page.last_edited_time.value,
            "daily_log_id": [],
        }

    def retrieve_books(self) -> list[dict]:
        searched_books = self.client.retrieve_database(database_id=DatabaseType.BOOK.value)
        entities = []
        for page in searched_books:
            title = page.get_title()
            daily_log_relation = page.get_relation(name="デイリーログ")
            status = page.get_status(name="ステータス")
            entities.append({
                "id": page.id,
                "url": page.url,
                "title": title.text,
                "created_at": page.created_time.value,
                "updated_at": page.last_edited_time.value,
                "daily_log_id": daily_log_relation.id_list,
                "status": status.status_name
            })
        return entities

    def retrieve_zettlekastens(self) -> list[dict]:
        searched_zettlekastens = self.client.retrieve_database(database_id=DatabaseType.ZETTLEKASTEN.value)
        entities = []
        for page in searched_zettlekastens:
            title = page.get_title()
            daily_log_relation = page.get_relation(name="デイリーログ")
            entities.append({
                "id": page.id,
                "url": page.url,
                "title": title.text,
                "created_at": page.created_time.value,
                "updated_at": page.last_edited_time.value,
                "daily_log_id": daily_log_relation.id_list,
            })
        return entities


    def retrieve_comments(self, page_id: str) -> list[dict]:
        """ 指定されたページのコメントを取得する """
        return self.client.retrieve_comments(page_id=page_id)

    def __create_page_in_database(self, database_type: DatabaseType, cover: Optional[Cover] = None, properties: list[Property] = []) -> dict:
        """ データベース上にページを新規作成する """
        return self.client.create_page_in_database(
            database_id=database_type.value,
            cover=cover,
            properties=properties,
        )

    def __find_daily_log(self, date: DateObject) -> Optional[BasePage]:
        daily_logs = self.client.retrieve_database(
            database_id=DatabaseType.DAILY_LOG.value,
            title=date.isoformat()
        )
        if len(daily_logs) == 0:
            return None
        return daily_logs[0]

    def __create_daily_log_page(self, date: DateObject, weekly_log_id: str) -> dict:
        return self.__create_page_in_database(
            database_type=DatabaseType.DAILY_LOG,
            properties=[
                Date.from_start_date(name="日付", start_date=date),
                Title.from_plain_text(name="名前", text=date.isoformat()),
                Relation.from_id_list(name="💭 ウィークリーログ", id_list=[weekly_log_id])]
        )

    def find_weekly_log(self, year: int, isoweeknum: int) -> Optional[dict]:
        title=f"{year}-Week{isoweeknum}"
        weekly_logs = self.client.retrieve_database(
            database_id=DatabaseType.WEEKLY_LOG.value,
            title=title
        )
        if len(weekly_logs) == 0:
            return None

        weekly_log = weekly_logs[0]
        title = weekly_log.get_title()
        goal = weekly_log.get_text(name="目標")

        return {
            "id": weekly_log.id,
            "url": weekly_log.url,
            "title": title.text,
            "goal": goal.text,
        }

    def append_comment(self, page_id: str, text: str) -> None:
        """ 指定されたページにコメントを追加する """
        self.client.append_comment(page_id=page_id, text=text)

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

    def __get_next_weekday(date: DateObject, day: str) -> DateObject:
        """ 指定された日付以降の、指定された曜日に該当する最も近い日付を計算する """
        day_index = DAYS.index(day)
        target_date = date
        while True:
            target_date = target_date + timedelta(days=1)
            if target_date.weekday() == day_index:
                return target_date
        # ↓ ありえないけど一応
        return None


if __name__ == "__main__":
    # python -m app.interface.notion_client
    notion_client = NotionClient()
    # notion_client.test_select_types(
    #     page_id="2ed9aff4b8724539b4b030c433eddc8e", column_name="団体")
    notion_client.update_recursive_project(date=DateObject.today())
