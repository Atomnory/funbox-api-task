import pytest
from redis.exceptions import DataError
from db import RedisController


@pytest.fixture()
def redis_controller():
    r = RedisController('test')
    yield r
    r._r.flushdb()
        

class TestsRedisController:
    def test_tests_use_not_original_db(self, redis_controller: RedisController):
        r_o = RedisController()._r
        r = redis_controller._r
        if not r_o.exists('test_key'):
            r.rpush('test_key', 'test')
            assert r_o.lrange('test_key', 0, -1) == []
            assert [x.decode('utf-8') for x in r.lrange('test_key', 0, -1)] == ['test']
        else:
            pytest.fail('Cannot test RedisController because test_key is in original database')

    def test_add_visited_links_correct_arguments(self, redis_controller: RedisController):
        r = redis_controller
        r.add_visited_links(['test_link'], 1)
        assert r._r.lrange(1, 0, -1) == [b'test_link']

    def test_add_visited_links_non_iterable_links(self, redis_controller: RedisController):
        r = redis_controller
        with pytest.raises(TypeError):
            r.add_visited_links(2, 1)

    def test_add_visited_links_with_reshuffled_arguments(self, redis_controller: RedisController):
        r = redis_controller
        with pytest.raises(TypeError):
            r.add_visited_links(1, ['test_link'])

    def test_add_visited_links_string_instead_list_of_strings(self, redis_controller: RedisController):
        r = redis_controller
        r.add_visited_links('test_link', 1)
        assert r._r.lrange(1, 0, -1) == [b't', b'e', b's', b't', b'_', b'l', b'i', b'n', b'k']

    def test_add_visited_links_wrong_type_key(self, redis_controller: RedisController):
        r = redis_controller
        with pytest.raises(DataError):
            r.add_visited_links(['test_value'], ['test_key'])

    def test_add_visited_links_string_key(self, redis_controller: RedisController):
        r = redis_controller
        r.add_visited_links(['test_value'], 'test_key')
        assert r._r.lrange('test_key', 0, -1) == [b'test_value']

    def test_get_visited_links_by_time_correct_work(self, redis_controller: RedisController):
        r = redis_controller
        r._r.rpush(1, 'test_value')
        assert r.get_visited_links_by_time(1) == ['test_value']

    def test_get_visited_links_by_time_convert_from_bytes_to_utf8_always(self, redis_controller: RedisController):
        r = redis_controller
        r._r.rpush(1, b'test_value')
        assert r.get_visited_links_by_time(1) == ['test_value']

    def test_get_visited_links_by_time_key_not_exist(self, redis_controller: RedisController):
        r = redis_controller
        assert r.get_visited_links_by_time(1) == []

    def test_get_visited_links_by_time_wrong_type_key(self, redis_controller: RedisController):
        r = redis_controller
        with pytest.raises(DataError):
            r.get_visited_links_by_time([])

    def test_get_visited_links_by_interval_correct_work_one_key(self, redis_controller: RedisController):
        r = redis_controller
        r._r.rpush(1, 'test_value')
        assert r.get_visited_links_by_interval(0, 2) == ['test_value']

    def test_get_visited_links_by_interval_misinterval_one_key(self, redis_controller: RedisController):
        r = redis_controller
        r._r.rpush(1, 'test_value')
        assert r.get_visited_links_by_interval(0, 1) == []

    def test_get_visited_links_by_interval_interval_is_zero(self, redis_controller: RedisController):
        r = redis_controller
        r._r.rpush(1, 'test_value')
        assert r.get_visited_links_by_interval(1, 1) == []

    def test_get_visited_links_by_interval_reshuffled_arguments(self, redis_controller: RedisController):
        r = redis_controller
        r._r.rpush(1, 'test_value')
        assert r.get_visited_links_by_interval(2, 0) == []

    def test_get_visited_links_by_interval_correct_work_two_keys(self, redis_controller: RedisController):
        r = redis_controller
        r._r.rpush(1, 'test_value_1')
        r._r.rpush(0, 'test_value_0')
        response = r.get_visited_links_by_interval(0, 2)
        assert 'test_value_0' in response
        assert 'test_value_1' in response

    def test_get_visited_links_by_interval_request_one_of_two_keys(self, redis_controller: RedisController):
        r = redis_controller
        r._r.rpush(1, 'test_value_1')
        r._r.rpush(2, 'test_value_2')
        response = r.get_visited_links_by_interval(0, 2)
        assert 'test_value_1' in response
        assert 'test_value_2' not in response

    def test_get_visited_links_by_interval_keys_not_exist(self, redis_controller: RedisController):
        r = redis_controller
        assert r.get_visited_links_by_interval(0, 10) == []

    def test_get_visited_links_by_interval_start_time_str_type(self, redis_controller: RedisController):
        r = redis_controller
        with pytest.raises(TypeError):
            r.get_visited_links_by_interval('0', 10)

    def test_get_visited_links_by_interval_end_time_str_type(self, redis_controller: RedisController):
        r = redis_controller
        with pytest.raises(TypeError):
            r.get_visited_links_by_interval(0, '10')

    def test_get_visited_links_by_interval_both_arguments_str_type(self, redis_controller: RedisController):
        r = redis_controller
        with pytest.raises(TypeError):
            r.get_visited_links_by_interval('0', '10')

    def test_get_visited_links_by_interval_both_arguments_iterable_type(self, redis_controller: RedisController):
        r = redis_controller
        with pytest.raises(TypeError):
            r.get_visited_links_by_interval([0,1], [4,5,6])

    def test_get_visited_links_by_interval_three_similiar_values(self, redis_controller: RedisController):
        r = redis_controller
        r._r.rpush(0, 'test_value')
        r._r.rpush(1, 'test_value')
        r._r.rpush(2, 'test_value')
        assert r.get_visited_links_by_interval(0, 3) == ['test_value']

    def test_get_visited_links_by_interval_three_similiar_values_one_different(self, redis_controller: RedisController):
        r = redis_controller
        r._r.rpush(0, 'test_value')
        r._r.rpush(1, 'test_value')
        r._r.rpush(2, 'test_value')
        r._r.rpush(3, 'test_value_3')
        assert r.get_visited_links_by_interval(0, 4) == ['test_value', 'test_value_3'] or r.get_visited_links_by_interval(0, 4) == ['test_value_3', 'test_value']
