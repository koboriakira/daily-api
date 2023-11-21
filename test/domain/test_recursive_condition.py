from unittest import TestCase
import json
import pathlib
from app.spotify.interface.track_translator import TrackTranslator
from datetime import date as DateObject
from app.domain.recursive_condition import RecursiveCondition, RecursiveConditionNextDate

class TestRecursiveCondition(TestCase):
    def test_次の任意の日付を指定(self):
        date = DateObject(year=2023, month=11, day=21)
        test_cases = [
            ("Next 1st", DateObject(year=2023, month=12, day=1)),
            ("Next 2nd", DateObject(year=2023, month=12, day=2)),
            ("Next 3rd", DateObject(year=2023, month=12, day=3)),
            ("Next 4th", DateObject(year=2023, month=12, day=4)),
            ("Next 5th", DateObject(year=2023, month=12, day=5)),
            ("Next 10th", DateObject(year=2023, month=12, day=10)),
            ("Next 31st", DateObject(year=2023, month=12, day=31)),
        ]

        for given, expected in test_cases:
            with self.subTest(given=given):
                actual = RecursiveCondition.of(given, date)
                self.assertEqual(actual.get_next_date(), expected)
                self.assertEqual(actual.cond_text, given.lower())

    def test_次の曜日(self):
        date = DateObject(year=2023, month=11, day=21)
        test_cases = [
            ("Next Sun", DateObject(year=2023, month=11, day=26)),
            ("Next Mon", DateObject(year=2023, month=11, day=27)),
            ("Next Tue", DateObject(year=2023, month=11, day=28)),
            ("Next Wed", DateObject(year=2023, month=11, day=22)),
            ("Next Thu", DateObject(year=2023, month=11, day=23)),
            ("Next Fri", DateObject(year=2023, month=11, day=24)),
            ("Next Sat", DateObject(year=2023, month=11, day=25)),
        ]

        for given, expected in test_cases:
            with self.subTest(given=given):
                actual = RecursiveCondition.of(given, date)
                self.assertEqual(actual.get_next_date(), expected)
                self.assertEqual(actual.cond_text, given.lower())

    def test_n日後(self):
        date = DateObject(year=2023, month=11, day=21)
        test_cases = [
            ("2 days", DateObject(year=2023, month=11, day=23)),
            ("2days", DateObject(year=2023, month=11, day=23)),
            ("8 days", DateObject(year=2023, month=11, day=29)),
            ("15 days", DateObject(year=2023, month=12, day=6)),
        ]

        for given, expected in test_cases:
            with self.subTest(given=given):
                actual = RecursiveCondition.of(given, date)
                self.assertEqual(actual.get_next_date(), expected)
                self.assertEqual(actual.cond_text, given.lower())
