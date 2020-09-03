import kydb
from kydb.impl.redis import RedisDB
from datetime import datetime
import os
import pytest
from kydb.impl.tests.test_utils import is_automated_test


@pytest.fixture
def db():
    return kydb.connect('redis://{}:6379'.format(
        os.environ['KINYU_UNITTEST_REDIS_HOST']))


@pytest.mark.skipif(is_automated_test(), reason="Do not run on automated test")
def test_redis_basic(db):
    key = '/unittests/foo'
    db[key] = 123
    assert db[key] == 123
    assert db.read(key, reload=True) == 123
    assert db.exists(key)
    db.delete(key)
    assert not db.exists(key)


@pytest.mark.skipif(is_automated_test(), reason="Do not run on automated test")
def test_redis_dict(db):
    key = '/unittests/dynamodb/bar'
    val = {
        'my_int': 123,
        'my_float': 123.456,
        'my_str': 'hello',
        'my_list': [1, 2, 3],
        'my_datetime': datetime.now()
    }
    db[key] = val
    assert db[key] == val
    assert db.read(key, reload=True) == val


def test_default_port():
    assert RedisDB._get_connection_kwargs(
        'my-host:1234') == {'host': 'my-host', 'port': 1234}
    assert RedisDB._get_connection_kwargs('my-host2') == {'host': 'my-host2'}
