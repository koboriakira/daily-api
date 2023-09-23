from unittest import TestCase
import json
import pathlib
from app.spotify.controller.track_response_translator import TrackResponseTranslator
from app.spotify.interface.track_translator import TrackTranslator


class TestTrackResponseTranslator(TestCase):
    def test_from_entity(self):
        # examples/track.jsonを開く
        # NOTE: ドメインモデルの準備が面倒だったので、 TrackTranslator で代用
        current_dir = pathlib.Path(__file__).resolve().parent
        with open(f'{current_dir}/examples/track.json') as f:
            track_entity = json.load(f)
            track = TrackTranslator.from_entity(track_entity)
            # NOTE: テスト対象はここから
            track_response = TrackResponseTranslator.to_entity(track)
            assert track_response.id == '5Ee2RlDLl8JctEb7iUzdHk'
