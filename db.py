import redis

r = redis.Redis(host='127.0.0.1', port=6379, db=3)

# links = ['ya.ru', 'google.co', 'yandex.com']
# r.rpush(2341221, *links)
# r.lrange(2341221, 0, -1)

def add_visited_links_to_db(links: list, time: int):
    r.rpush(time, *links)


def get_visited_links_by_time(time: int) -> list[str] | None:
    return [x.decode('utf-8') for x in r.lrange(time, 0, -1)]


def get_visited_links_by_interval(start_time: int, end_time: int) -> list[str] | None:
    result = set()
    for time in range(start_time, end_time):
        time_list = [x.decode('utf-8') for x in r.lrange(time, 0, -1)]
        result.update(time_list)
    return list(result)
