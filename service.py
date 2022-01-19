import time
from typing import Dict
from db import add_visited_links_to_db, get_visited_links_by_time, get_visited_links_by_interval

def handle_links(links: list, time_post: int) -> str:
    print('Time_post', time_post)
    status = []
    handled_domains = []
    for i, link in enumerate(links):
        try:
            parsed_link = parse_link(link)
        except Exception as e:
            status.append(f'ERROR: line {i}: "{link}" : {e}')
        else:
            if parsed_link not in handled_domains:
                handled_domains.append(parsed_link)

    if not status:
        status = 'ok'
    if handled_domains:
        add_visited_links_to_db(handled_domains, time_post)
    else:
        status = 'error'
    return status


def parse_link(link: str) -> str:
    if not isinstance(link, str):
        raise Exception('parse_link accepts only string')

    if link.startswith('http://'):
        link = link.removeprefix('http://')
    elif link.startswith('https://'):
        link = link.removeprefix('https://')
    elif link.startswith('.') or link.endswith('.'):
        raise Exception('link starts or ends with dot')

    domain = link.split('/', maxsplit=1)[0]
    link = domain.split('?', maxsplit=1)[0]
    
    if len(link) < 1:
        raise Exception('domain is empty')
    
    if link.find(' ') != -1:
        raise Exception('domain should not have spaces')

    if link.find('.') != -1:
        domains = link.split('.')
        for i in domains:
            if len(i) == 0:
                raise Exception('a part of domain is empty')
    else:
        raise Exception('too small domain')

    return link


def handle_interval(from_time: int, to_time: int) -> Dict:
    print('From_time:', from_time, ' To_Time:', to_time)
    if from_time is None:
        return {'status': 'error: from time is None'}
    elif from_time > to_time:
        return {'status': 'error: from more than to'}
    
    if to_time is None or from_time == to_time:
        domains = get_visited_links_by_time(from_time)
    else:
        domains = get_visited_links_by_interval(from_time, to_time)
    
    if domains:
        return {'domains': domains,
                  'status': 'ok'}
    else:
        return {'status': 'domains are not found'}
