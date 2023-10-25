from notion_client import Client
import os
from notion_client_wrapper.block import BlockFactory, Block, Paragraph
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.base_operator import BaseOperator
from notion_client_wrapper.cover import Cover
from notion_client_wrapper.icon import Icon
from notion_client_wrapper.properties.properties import Properties
from notion_client_wrapper.properties.property import Property
from typing import Optional


class ClientWrapper:
    def __init__(self):
        # NOTION_API_TOKENがなければエラーを出す
        if not os.getenv("NOTION_API_TOKEN"):
            raise Exception("NOTION_API_TOKENが設定されていません")

        self.client = Client(auth=os.getenv("NOTION_API_TOKEN"))

    def retrieve_page(self, page_id: str) -> BasePage:
        """ 指定されたページを取得する """
        page_entity = self.__retrieve_page(page_id=page_id)
        return self.__convert_page_model(page_entity=page_entity, include_children=True)

    def retrieve_database(self, database_id: str, title: Optional[str] = None) -> list[BasePage]:
        """ 指定されたデータベースのページを取得する """
        data = self.client.databases.query(database_id=database_id)
        result: list[BasePage] = []
        for page_entity in data["results"]:
            page = self.__convert_page_model(page_entity=page_entity, include_children=False)
            result.append(page)
        if title is not None:
            result = list(filter(lambda p: p.properties.get_title().text == title, result))
        return result

    def list_blocks(self, block_id: str) -> dict:
        """ 指定されたブロックの子ブロックを取得する """
        return self.client.blocks.children.list(block_id=block_id)

    def append_blocks(self, block_id: str, blocks: list[Block]) -> dict:
        """ 指定されたブロックに子ブロックを追加する """
        return self.__append_block_children(
            block_id=block_id,
            children=list(map(lambda b: b.to_dict(), blocks))
        )

    def append_comment(self, page_id: str, text: str):
        """ 指定されたページにコメントを追加する """
        return self.client.comments.create(
            parent={ "page_id": page_id },
            rich_text=[{"text": {"content": text}}],
        )

    def __append_block_children(self, block_id: str, children=list[dict]) -> dict:
        return self.client.blocks.children.append(
            block_id=block_id, children=children)

    def __convert_page_model(self, page_entity: dict, include_children: bool = True) -> BasePage:
        id = page_entity["id"]
        created_time = page_entity["created_time"]
        last_edited_time = page_entity["last_edited_time"]
        created_by = BaseOperator.of(page_entity["created_by"])
        last_edited_by = BaseOperator.of(page_entity["last_edited_by"])
        cover = Cover.of(page_entity["cover"]) if page_entity["cover"] is not None else None
        icon = Icon.of(page_entity["icon"]) if page_entity["icon"] is not None else None
        archived = page_entity["archived"]
        properties=Properties.from_dict(page_entity["properties"])
        block_children = self.__get_block_children(page_id=id) if include_children else []
        return BasePage(id=id,
                        created_time=created_time,
                        last_edited_time=last_edited_time,
                        created_by=created_by,
                        last_edited_by=last_edited_by,
                        cover=cover,
                        icon=icon,
                        archived=archived,
                        properties=properties,
                        block_children=block_children)

    def __retrieve_page(self, page_id: str) -> dict:
        return self.client.pages.retrieve(page_id=page_id)

    def __get_block_children(self, page_id: str) -> list[Block]:
        block_entities = self.__list_blocks(block_id=page_id)[
            "results"]
        return list(map(lambda b: BlockFactory.create(b), block_entities))

    def __list_blocks(self, block_id: str) -> dict:
        return self.client.blocks.children.list(block_id=block_id)

if __name__ == "__main__":
    # python -m notion_client_wrapper.client_wrapper
    client = ClientWrapper()
    # page = client.retrieve_page(page_id="b7576fbdde9b476f913924c1bd90b250")
    # print(page)
    # pages = client.retrieve_database(database_id="986876c2e7f8457abd4437334835d0db", title="テストA")
    # print(pages)
    # blocks = client.list_blocks(block_id="b7576fbdde9b476f913924c1bd90b250")
    # print(blocks)
    result = client.append_blocks(block_id="b7576fbdde9b476f913924c1bd90b250", blocks=[Paragraph.from_plain_text("test")])
    # print(result)
