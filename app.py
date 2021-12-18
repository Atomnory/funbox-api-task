from typing import Optional
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

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

@app.route('/visited_links', methods=['POST'])
def post_visited_links():
    if not request.json:
        abort(400)
    add_visited_links_to_db(request.json['links'])
    return jsonify({'status': 'ok'})

@app.route('/<string:search_string>', methods=['GET'])
def get_visited_domains(search_string: str):
    if search_string.startswith('visited_domains'):
        return jsonify({'domains':get_visited_links_from_db()})
    else:
        abort(400)


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
