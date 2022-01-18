from typing import Optional
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# TODO: add time of POST visited_links
# TODO: add Redis as data keeper

# visited_links = {
#     'links': [
#         "https://ya.ru",
#         "https://ya.ru?q=123",
#         "funbox.ru",
#         "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
#     ]
# }

# database = {
#     1: ['ya.ru', 'google.com', 'gmail.google.com', 'bbc.co.uk'],
#     2: ['google.com', 'bbc.co.uk'],
#     10: ['ya.ru']
# }

# domains = {
#     "domains": [
#         "ya.ru",
#         "funbox.ru",
#         "stackoverflow.com"
#     ],
#     "status": "ok"
# }

# curl -i -H "Content-Type: application/json" -X POST -d '{"links":["https://ya.ru", "https://ya.ru?q=123", "funbox.ru", "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"]}' http://127.0.0.1:5000/visited_links

@app.route('/visited_links', methods=['POST'])
def post_visited_links():
    if not request.json:
        abort(400)
    status = handle_links(request.json['links'])
    return jsonify({'status': status})

@app.route('/<string:search_string>', methods=['GET'])
def get_visited_domains(search_string: str):
    if search_string.startswith('visited_domains'):
        return jsonify({'domains':get_visited_links_from_db()})
    else:
        abort(400)


def handle_links(links: list) -> str:
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

    add_visited_links_to_db(handled_domains)
    if not status:
        status = 'ok'
    return status

def add_visited_links_to_db(links: list):
    # save in file
    with open('visited_links.txt', 'a') as f:
        for link in links:
            print(link, file=f)


def get_visited_links_by_time_from_db():
    # get links by time from file
    pass


def get_visited_links_from_db() -> Optional[list]:
    # get all links from db
    try:
        links = []
        with open('visited_links.txt', 'r') as f:
            for line in f.read().splitlines():
                links.append(line)
        return links
    except FileNotFoundError:
        return None


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
    
    
    
