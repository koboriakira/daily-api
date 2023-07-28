import requests


class GlobalIpAddress:
    @staticmethod
    def get() -> str:
        return requests.get('https://api.ipify.org').text
