from notion_client import Client
import os
from notion_client_wrapper.block import BlockFactory, Block
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.base_operator import BaseOperator
from notion_client_wrapper.cover import Cover
from notion_client_wrapper.icon import Icon
from notion_client_wrapper.properties import Properties, Property


class ClientWrapper:
      def __init__(self):
          # NOTION_API_TOKENがなければエラーを出す
          if not os.getenv("NOTION_API_TOKEN"):
              raise Exception("NOTION_API_TOKENが設定されていません")

          self.client = Client(auth=os.getenv("NOTION_API_TOKEN"))

      def retrieve_page(self, page_id: str) -> BasePage:
          page_entity = self.__retrieve_page(page_id=page_id)
          id = page_entity["id"]
          created_time = page_entity["created_time"]
          last_edited_time = page_entity["last_edited_time"]
          created_by = BaseOperator.of(page_entity["created_by"])
          last_edited_by = BaseOperator.of(page_entity["last_edited_by"])
          cover = Cover.of(page_entity["cover"]) if page_entity["cover"] is not None else None
          icon = Icon.of(page_entity["icon"]) if page_entity["icon"] is not None else None
          archived = page_entity["archived"]
          properties=Properties.from_dict(page_entity["properties"])
          # block_children = self.__get_block_children(page_id=page_id)
          return BasePage(id=id,
                                created_time=created_time,
                                last_edited_time=last_edited_time,
                                created_by=created_by,
                                last_edited_by=last_edited_by,
                                cover=cover,
                                icon=icon,
                                archived=archived,
                                properties=properties)

      def __retrieve_page(self, page_id: str) -> dict:
          return self.client.pages.retrieve(page_id=page_id)

      def __get_block_children(self, page_id: str) -> list[Block]:
          block_entities = self.__list_blocks(block_id=page_id)[
              "results"]
          return list(map(lambda b: BlockFactory.create(b), block_entities))

      def __append_block_children(self, block_id: str, children=list[dict]) -> list:
          print(children)
          self.client.blocks.children.append(
              block_id=block_id, children=children)

      def __list_blocks(self, block_id: str) -> dict:
          return self.client.blocks.children.list(block_id=block_id)

if __name__ == "__main__":
    # python -m notion_client_wrapper.client_wrapper
    client = ClientWrapper()
    page = client.retrieve_page(page_id="454a446facc94daf9343f1b56905d2b7")
    print(page)
