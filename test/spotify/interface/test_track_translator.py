from unittest import TestCase
import json
import pathlib
from app.spotify.interface.track_translator import TrackTranslator


class TestTrackTranslator(TestCase):
    def test_from_entity(self):
        # examples/track.jsonを開く
        current_dir = pathlib.Path(__file__).resolve().parent
        with open(f'{current_dir}/examples/track.json') as f:
            track_entity = json.load(f)
            track = TrackTranslator.from_entity(track_entity)
            assert track.id == '5Ee2RlDLl8JctEb7iUzdHk'
