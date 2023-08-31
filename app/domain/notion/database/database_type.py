from enum import Enum


class DatabaseType(Enum):
    """
    各データベースのID
    """

    DAILY_LOG = "58da568b-4e63-4a46-9ffe-36adeb59ab30"
    MUSIC = "ef2d1550-3edb-4848-b236-229fb83d31e0"
    TAG = "8356ec79-ce5f-4aea-bad2-c8dc49098885"
    HABIT_TRACKER_ALLDAY = "752e93c9-9a9c-4bef-8d1f-7702439f658a"
    HABIT_TRACKER_MORNING = "df0ee11c-90a8-46d5-b8bf-aac52f8d8bcd"
    HABIT_TRACKER_NIGHT = "a759f224-ebb8-40c0-9047-6d7f88835e65"
    INGREDIENTS = "dba77be1-c1a6-40a2-858e-85878ee55b0d"
    WEEKLY_LOG = "3ae412cf-6c87-4119-a9c6-ffdb2eee2a1e"
    PROJECT = "458c69ce-4e1c-49fe-810c-f26c2291e294"
    ZETTLEKASTEN = "2dd39a65-3f14-45e1-a51e-2c3d857a8321"
    RECIPE = "64b6d5f1-2547-41a2-a74d-25f0c4df041e"

    @staticmethod
    def ignore_updated_at() -> list[str]:
        """
        更新日時を無視するデータベースのIDを返す
        """
        return [
            DatabaseType.DAILY_LOG.value,
            DatabaseType.TAG.value,
            DatabaseType.HABIT_TRACKER_ALLDAY.value,
            DatabaseType.HABIT_TRACKER_MORNING.value,
            DatabaseType.HABIT_TRACKER_NIGHT.value,
            DatabaseType.INGREDIENTS.value,
        ]
