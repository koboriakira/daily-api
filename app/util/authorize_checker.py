import os
from typing import Optional


class AuthorizeChecker:
    @staticmethod
    def validate(access_token: Optional[str]) -> None:
        if access_token is None:
            raise Exception('access_token is None')
        if access_token != os.environ.get('ACCESS_TOKEN'):
            raise Exception('access_token is invalid')
