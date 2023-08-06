from dataclasses import dataclass
from app.domain.notion.page.base_page import BasePage
from app.domain.notion.page.recipe import Recipe
from app.domain.notion.page.webclip import Webclip
from app.domain.notion.page.book import Book
from app.domain.notion.page.music import Music
from app.domain.notion.page.zettlekasten import Zettlekasten
from app.domain.notion.page.prowrestling_watch import ProwrestlingWatch
from app.domain.notion.page.restaurant import Restaurant
from app.domain.notion.page.go_out import GoOut
from app.domain.notion.page.arata import Arata
from app.domain.notion.properties import Date
from datetime import datetime


@dataclass
class DailyLog(BasePage):
    date: Date  # 日付
    summary: str  # 一言
    recipes: list[Recipe]  # レシピ
    webclips: list[Webclip]  # Webクリップ
    books: list[Book]  # 書籍
    prowrestling_watches: list[ProwrestlingWatch]  # プロレス観戦記録
    musics: list[Music]  # 音楽
    zettlekasten: list[Zettlekasten]  # Zettlekasten
    restaurants: list[Restaurant]  # 外食
    go_outs: list[GoOut]  # おでかけ
    aratas: list[Arata]  # あらた

    def __init__(self, id: str,
                 created_time: datetime,
                 last_edited_time: datetime,
                 parent: dict,
                 archived: bool,
                 date: Date,
                 summary: str,
                 recipes: list[str],
                 webclips: list[Webclip],
                 books: list[Book],
                 prowrestling_watches: list[ProwrestlingWatch],
                 musics: list[Music],
                 zettlekasten: list[Zettlekasten],
                 restaurants: list[Restaurant],
                 go_outs: list[GoOut],
                 aratas: list[Arata]):
        self.id = id
        self.created_time = created_time
        self.last_edited_time = last_edited_time
        self.parent = parent
        self.archived = archived
        self.date = date
        self.summary = summary
        self.recipes = recipes
        self.webclips = webclips
        self.books = books
        self.prowrestling_watches = prowrestling_watches
        self.musics = musics
        self.zettlekasten = zettlekasten
        self.restaurants = restaurants
        self.go_outs = go_outs
        self.aratas = aratas
