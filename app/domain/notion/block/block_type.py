from enum import Enum


class BlockType(Enum):
    VIDEO = "video"
    QUOTE = "quote"
    PARAGRAPH = "paragraph"
    HEADING_1 = "heading_1"
    # 以下、Copilotによる自動生成
    HEADING_2 = "heading_2"
    HEADING_3 = "heading_3"
    BULLETED_LIST_ITEM = "bulleted_list_item"
    NUMBERED_LIST_ITEM = "numbered_list_item"
    TO_DO = "to_do"
    TOGGLE = "toggle"
    CHILD_PAGE = "child_page"
    EMBED = "embed"
    IMAGE = "image"
    COLUMN_LIST = "column_list"
    COLUMN = "column"
    DIVIDER = "divider"
    TABLE_OF_CONTENTS = "table_of_contents"
    BREADCRUMB = "breadcrumb"
    FACTOID = "factoid"
    CALLOUT = "callout"
    CODE = "code"
    COLLECTION_VIEW = "collection_view"
    COLLECTION_VIEW_PAGE = "collection_view_page"
    EQUATION = "equation"
    FILE = "file"
    GALLERY = "gallery"
    LINK_TO_PAGE = "link_to_page"
    PAGE = "page"
    PDF = "pdf"
    SUB_SUB_HEADER = "sub_sub_header"
    SUB_HEADER = "sub_header"
    TWEET = "tweet"
    VIDEO_FILE = "video_file"
    AUDIO = "audio"
    BOOKMARK = "bookmark"
    CODE_BLOCK = "code_block"
    EMBED_BLOCK = "embed_block"
    FILE_BLOCK = "file_block"
    IMAGE_BLOCK = "image_block"
    PDF_BLOCK = "pdf_block"
    VIDEO_BLOCK = "video_block"
    AUDIO_BLOCK = "audio_block"
    BULLETED_LIST = "bulleted_list"