import os
import json
from app.util.cache import Cache


def test_write(tmpdir):
    # Given
    key = 'test_key'
    value = {'test_key': 'test_value'}
    is_test = True

    # When
    cache = Cache()
    cache.write(key, value, is_test=is_test)

    # Then
    expected_file_path = "/tmp/daily-api/test_key_test.json"
    assert os.path.exists(expected_file_path)

    with open(expected_file_path, 'r') as f:
        assert json.load(f) == value
