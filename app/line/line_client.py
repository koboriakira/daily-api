import json
import requests
import os


class LineClientFactory:
    @staticmethod
    def get_instance():
        channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
        talk_id = os.getenv("LINE_TALK_ID")
        return LineClient(channel_access_token, talk_id)


class LineClient:
    MESSAGE_PUSH_API = "https://api.line.me/v2/bot/message/push"

    channel_access_token: str
    talk_id: str  # rood_id or user_id or group_id

    def __init__(self, channel_access_token: str, talk_id: str):
        self.channel_access_token = channel_access_token
        self.talk_id = talk_id

    def push_message(self, text: str) -> dict:
        payload = json.dumps({
            "to": self.talk_id,
            "messages": [
                {
                    "type": "text",
                    "text": text
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.channel_access_token}'
        }
        response = requests.request(
            "POST", self.MESSAGE_PUSH_API, headers=headers, data=payload)
        return response.json()


if __name__ == "__main__":
    # python -m app.line.line_client
    line_client = LineClientFactory.get_instance()
    line_client.push_message("hello")
