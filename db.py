import redis


class RedisController:
    def __init__(self, database_type: str = None) -> None:
        db = 4 if database_type == 'test' else 3
        self._r = redis.Redis(host='127.0.0.1', port=6379, db=db)

    def add_visited_links(self, links: list, time: int):
        self._r.rpush(time, *links)

    def get_visited_links_by_time(self, time: int) -> list[str] | None:
        return [x.decode('utf-8') for x in self._r.lrange(time, 0, -1)]

    def get_visited_links_by_interval(self, start_time: int, end_time: int) -> list[str] | None:
        result = set()
        for time in range(start_time, end_time):
            result.update(self.get_visited_links_by_time(time))
        return list(result)
