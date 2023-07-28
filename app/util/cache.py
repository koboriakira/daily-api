import json
import os


class Cache:
    DIR = "/tmp/daily-api"

    @classmethod
    def write(cls, key: str, value: str | int | dict | list, is_test: bool = False) -> None:
        if not os.path.exists(cls.DIR):
            os.makedirs(cls.DIR)

        file_path = cls.__get_file_path(key, is_test)
        with open(file_path, 'w') as f:
            json.dump(value, f, indent=4)

    @classmethod
    def read(cls, key: str) -> str | int | dict | list:
        file_path = cls.__get_file_path(key)
        with open(file_path, 'r') as f:
            result = json.load(f)
            return result

    @classmethod
    def __get_file_path(cls, key: str, is_test: bool = False) -> str:
        fine_name = f'/{key}_test' if is_test else key
        return f'{Cache.DIR}/{fine_name}.json'
